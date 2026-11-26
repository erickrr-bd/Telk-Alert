"""
Class that manages everything related to Telk-Alert.
"""
from os import path, getpid
from time import monotonic, strftime, time
import heapq
from itertools import count
from collections import OrderedDict
from threading import Thread, Event, Lock, Condition
from dataclasses import dataclass, field
from libPyLog import libPyLog
from libPyElk import libPyElk
from libPyUtils import libPyUtils
from libPyTelegram import libPyTelegram
from libPyConfiguration import libPyConfiguration
from .Constants_Class import Constants

# Keys every alert rule must have.
REQUIRED_KEYS = ("name", "level", "index_pattern", "timestamp_field", "total_events", "search_time", "range_time", "query", "use_fields", "telegram_bot_token", "telegram_chat_id")

# Log entry for each HTTP code returned by the Telegram API: (level, message).
TELEGRAM_CODES = {
	200: (2, "Telegram message sent"),
	400: (4, "Telegram message not sent. Bad request."),
	401: (4, "Telegram message not sent. Unauthorized."),
	403: (4, "Telegram message not sent. Forbidden (is the bot in the chat?)."),
	404: (4, "Telegram message not sent. Not found."),
	429: (3, "Telegram message not sent. Rate limited.")
}

WARNING_ICON = "⚠️"
LEVEL_ICON = "\U0001f6a6"
CLOCK_ICON = "⏰"

# Priority of the messages in the sending queue (lower is sent first).
LEVEL_PRIORITY = {"High": 0, "Medium": 1, "Low": 2}


def telegram_length(text: str) -> int:
	"""
	Function that returns the length of a text as Telegram counts it (UTF-16 code units: most emojis count 2).
	"""
	return len(text.encode("utf-16-le")) // 2


class TelegramSender(Thread):
	"""
	Thread that sends the messages of one Telegram chat at a controlled pace. Every alert rule that uses the same
	bot and chat puts its messages in this queue, so the chat's limit is respected and the rules never wait for Telegram.
	The queue is bounded: when it is full, a new message replaces a queued one of lower priority, or it is dropped.
	"""

	def __init__(self, bot_token: str, chat_id: str, stop: Event, log, log_result, interval: float, max_size: int) -> None:
		super().__init__(name = "telegram-sender", daemon = True)
		self._bot_token = bot_token
		self._chat_id = chat_id
		self._stop_event = stop
		self._log = log
		self._log_result = log_result
		self._interval = interval
		self._max_size = max_size
		self._queue = []
		self._sequence = count()
		self._condition = Condition()
		self._dropped = 0


	def put(self, priority: int, message: str, rule_name: str) -> bool:
		"""
		Method that adds a message to the queue.

		Returns:
			queued (bool): False if the message was dropped because the queue is full of messages of equal or higher priority.
		"""
		with self._condition:
			if len(self._queue) >= self._max_size:
				worst = max(self._queue)
				self._dropped += 1
				if priority >= worst[0]:
					return False
				self._queue.remove(worst)
				heapq.heapify(self._queue)
			heapq.heappush(self._queue, (priority, next(self._sequence), message, rule_name))
			self._condition.notify()
			return True


	def pending(self) -> int:
		with self._condition:
			return len(self._queue)


	def run(self) -> None:
		# libPyTelegram is NOT thread-safe: this thread owns its instance.
		with libPyTelegram() as telegram:
			while not self._stop_event.is_set():
				with self._condition:
					while not self._queue and not self._stop_event.is_set():
						self._condition.wait(1)
					if self._stop_event.is_set():
						break
					_, _, message, rule_name = heapq.heappop(self._queue)
					dropped = 0
					if not self._queue and self._dropped:
						dropped, self._dropped = self._dropped, 0
				try:
					self._log_result(telegram.send_telegram_message(self._bot_token, self._chat_id, message), rule_name)
					if dropped:
						self._stop_event.wait(self._interval)
						self._log(f"{dropped} Telegram message(s) dropped: the sending queue was full", 3, "_telegramQueue", True)
						self._log_result(telegram.send_telegram_message(self._bot_token, self._chat_id, f"{WARNING_ICON} Telk-Alert: {dropped} alert message(s) were dropped because too many alerts were generated at the same time. Check Kibana."), "telegramQueue")
				except Exception as exception:
					self._log(f"Error sending Telegram message ({rule_name}): {exception}", 4, "_telegramQueue", True)
				self._stop_event.wait(self._interval)
		if self.pending():
			self._log(f"Telk-Alert stopped with {self.pending()} Telegram message(s) not sent", 3, "_telegramQueue", True)


@dataclass
class TelkAlert:

	logger: libPyLog = field(default_factory = libPyLog)
	utils: libPyUtils = field(default_factory = libPyUtils)
	elasticsearch: libPyElk = field(default_factory = libPyElk)
	stop: Event = field(default_factory = Event)
	# Heartbeat shared with Telk-Alert-Agent: last run of each alert rule and the rules that couldn't start.
	heartbeats: dict = field(default_factory = dict)
	skipped: list = field(default_factory = list)
	lock: Lock = field(default_factory = Lock)
	# One sending queue (thread) per Telegram bot + chat.
	senders: dict = field(default_factory = dict)


	# --- Internal helpers ----------------------------------------------------------------------
	def _log(self, message, level: int, tag: str, to_file: bool = False) -> None:
		"""
		Method that writes an entry on the terminal (journald) and, optionally, in the log file.
		"""
		if to_file:
			try:
				self.logger.create_log(message, level, tag, use_stream_handler = True, use_file_handler = True, file_name = Constants.LOG_FILE, user = Constants.USER, group = Constants.GROUP)
				return
			except OSError as exception:
				# The log file can't be written (missing folder, permissions): the entry still reaches journald.
				self.logger.create_log(f"Log file not available ({exception})", 3, "_log", use_stream_handler = True)
		self.logger.create_log(message, level, tag, use_stream_handler = True)


	def _load_configuration(self) -> libPyConfiguration:
		"""
		Method that reads and validates the configuration. The object is created without its constructor,
		so the service doesn't need libPyDialog/pythondialog (convert_dict_to_object doesn't use them).
		"""
		configuration = libPyConfiguration.__new__(libPyConfiguration)
		configuration.convert_dict_to_object(self.utils.read_yaml_file(Constants.TELK_ALERT_CONFIGURATION))
		return configuration


	def _load_rule(self, file_name: str) -> dict:
		"""
		Method that reads and validates an alert rule (raises ValueError if it is invalid).
		"""
		rule = self.utils.read_yaml_file(path.join(Constants.ALERT_RULES_FOLDER, file_name))
		missing = [key for key in REQUIRED_KEYS if key not in rule]
		if missing:
			raise ValueError(f"missing keys: {', '.join(missing)}")
		if not isinstance(rule["name"], str) or not rule["name"].strip():
			raise ValueError("invalid name")
		if isinstance(rule["total_events"], bool) or not isinstance(rule["total_events"], int) or rule["total_events"] < 1:
			raise ValueError("invalid total_events")
		if not isinstance(rule["use_fields"], bool) or (rule["use_fields"] and not isinstance(rule.get("fields"), list)):
			raise ValueError("invalid fields")
		for key in ("search_time", "range_time"):
			if not isinstance(rule[key], dict) or len(rule[key]) != 1:
				raise ValueError(f"invalid {key}")
			self.utils.convert_time_to_seconds(*next(iter(rule[key].items())))
		try:
			query_string = rule["query"]["query_type"][0]["query_string"]["query"]
		except (KeyError, IndexError, TypeError) as exception:
			raise ValueError("invalid query") from exception
		if not isinstance(query_string, str) or not query_string.strip():
			raise ValueError("invalid query")
		return rule


	def _decrypt_telegram(self, rule: dict) -> tuple:
		"""
		Method that decrypts the Telegram Bot Token and Chat ID once per alert rule (the passphrase is wiped afterwards).
		allow_legacy: rules modified with Telk-Alert-Tool may mix new and old encrypted values. Remove it once every
		rule has been re-encrypted, because the old format doesn't bind each secret to its field.
		"""
		passphrase = self.utils.get_passphrase(Constants.KEY_FILE, owner = Constants.USER)
		try:
			return tuple(self.utils.decrypt_data(rule[field], passphrase, allow_legacy = True, context = f"{Constants.CTX_ALERT_RULE}:{field}")
				for field in ("telegram_bot_token", "telegram_chat_id"))
		finally:
			self.utils.zeroize(passphrase)


	def _skip(self, alert_rule: str, reason) -> None:
		"""
		Method that registers an alert rule that couldn't start (reported by Telk-Alert-Agent, which doesn't restart for it).
		"""
		with self.lock:
			self.skipped.append(f"{alert_rule}: {reason}")


	def _write_heartbeat(self) -> None:
		"""
		Method that writes the heartbeat every HEARTBEAT_INTERVAL seconds until the service is stopped.
		"""
		failed = False
		while True:
			try:
				with self.lock:
					data = {"pid": getpid(), "updated": time(), "rules": dict(self.heartbeats), "skipped": list(self.skipped)}
				self.utils.create_yaml_file(data, Constants.HEARTBEAT_FILE)
				failed = False
			except Exception as exception:
				if not failed:
					self._log(f"Heartbeat not written: {exception}", 3, "_heartbeat", to_file = True)
				failed = True
			if self.stop.wait(Constants.HEARTBEAT_INTERVAL):
				break


	# --- Start ---------------------------------------------------------------------------------
	def start_telk_alert(self) -> bool:
		"""
		Method that starts Telk-Alert.

		Returns:
			running (bool): True if at least one alert rule was started.
		"""
		try:
			for line in ("Author: Erick Roberto Rodríguez Rodríguez", "Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", "Github: https://github.com/erickrr-bd/Telk-Alert", f"Telk-Alert v{Constants.VERSION} - {Constants.RELEASE_DATE}"):
				self._log(line, 2, "_start")
			if not path.exists(Constants.TELK_ALERT_CONFIGURATION):
				self._log(f"Configuration not found: {Constants.TELK_ALERT_CONFIGURATION}", 4, "_readConfiguration", to_file = True)
				return False
			self._log(f"Configuration found: {Constants.TELK_ALERT_CONFIGURATION}", 2, "_readConfiguration")
			configuration = self._load_configuration()
			conn_es = self.elasticsearch.create_connection(configuration, Constants.KEY_FILE, Constants.CTX_TELK_ALERT, owner = Constants.USER, relax_x509_strict = Constants.RELAX_X509_STRICT)
			info = conn_es.info()
			self._log(f"Connection established: {','.join(configuration.es_host)}", 2, "_clusterConnection")
			self._log(f"ElasticSearch Cluster Name: {info['cluster_name']}", 2, "_clusterConnection")
			self._log(f"ElasticSearch Cluster UUID: {info['cluster_uuid']}", 2, "_clusterConnection")
			self._log(f"ElasticSearch Version: {info['version']['number']}", 2, "_clusterConnection")
			if configuration.use_authentication:
				self._log(f"Authentication enabled. Method: {configuration.authentication_method}", 2, "_clusterConnection")
			else:
				self._log("Authentication disabled. Not recommended for security reasons.", 3, "_clusterConnection")
			if configuration.verificate_certificate_ssl and configuration.certificate_file:
				self._log(f"SSL certificate verified with: {configuration.certificate_file}", 2, "_clusterConnection")
				if Constants.RELAX_X509_STRICT:
					self._log("Strict X.509 check (RFC 5280) disabled for the cluster's CA. Chain of trust and hostname are still verified.", 3, "_clusterConnection")
			else:
				self._log("SSL certificate verified with the public CA certificates (certifi)", 2, "_clusterConnection")
			started = self._start_alert_rules(conn_es)
			Thread(name = "heartbeat", target = self._write_heartbeat, daemon = True).start()
			return started > 0
		except Exception as exception:
			self._log("Error starting Telk-Alert. For more information, see the logs.", 4, "_start")
			self._log(exception, 4, "_start", to_file = True)
			return False


	def _start_alert_rules(self, conn_es) -> int:
		"""
		Method that validates the alert rules and starts one thread per valid rule (invalid rules are skipped).

		Returns:
			started (int): Number of alert rules started.
		"""
		alert_rules = sorted(self.utils.get_yaml_files_in_folder(Constants.ALERT_RULES_FOLDER))
		if not alert_rules:
			self._log(f"No alert rules in: {Constants.ALERT_RULES_FOLDER}", 3, "_readAlertRules", to_file = True)
			return 0
		self._log(f"{len(alert_rules)} alert rule(s) in: {Constants.ALERT_RULES_FOLDER}", 2, "_readAlertRules")
		started = 0
		for alert_rule in alert_rules:
			try:
				rule = self._load_rule(alert_rule)
			except Exception as exception:
				self._log(f"Alert rule skipped ({alert_rule}): {exception}", 4, "_loadAlertRule", to_file = True)
				self._skip(alert_rule, exception)
				continue
			self._log(f"Alert rule: {rule['name']}", 2, "_loadAlertRule")
			Thread(name = alert_rule.removesuffix(".yaml"), target = self.start_alert_rule, args = (conn_es, rule), daemon = True).start()
			started += 1
		return started


	# --- Alert rules ---------------------------------------------------------------------------
	def start_alert_rule(self, conn_es, rule: dict) -> None:
		"""
		Method that executes an alert rule until the service is stopped. An error in one execution
		is logged and the rule keeps running.

		Parameters:
			conn_es (ElasticSearch): A straightforward mapping from Python to ES REST endpoints (shared, thread-safe).
			rule (dict): Object that contains the alert rule's configuration data.
		"""
		tag = f"_{rule['name']}"
		try:
			search_seconds = self.utils.convert_time_to_seconds(*next(iter(rule["search_time"].items())))
			range_unit, range_total = next(iter(rule["range_time"].items()))
			gte_date = self.utils.get_gte_date(range_unit, range_total)
			lte_date = self.utils.get_lte_date(range_unit)
			query_string = rule["query"]["query_type"][0]["query_string"]["query"]
			fields = rule["fields"] if rule["use_fields"] else None
			telegram_bot_token, telegram_chat_id = self._decrypt_telegram(rule)
		except Exception as exception:
			self._log(f"Alert rule not started: {exception}", 4, tag, to_file = True)
			self._skip(f"{rule['name']}.yaml", exception)
			return

		priority = LEVEL_PRIORITY.get(rule["level"], 1)
		sender = self._sender(telegram_bot_token, telegram_chat_id)
		sent_ids = OrderedDict()
		while not self.stop.is_set():
			started = monotonic()
			try:
				result = self.elasticsearch.search_query_string(conn_es, rule["index_pattern"], query_string, rule["timestamp_field"], gte_date, lte_date, rule["use_fields"], size = Constants.MAX_EVENTS_PER_ALERT, fields = fields)
				total = result.hits.total.value
				if total == 0:
					self._log("No events", 2, tag)
				elif total < rule["total_events"]:
					self._log(f"Events found: {total} (threshold: {rule['total_events']}). No alert sent.", 2, tag)
				else:
					self._log(f"Events found: {total}", 2, tag, to_file = True)
					new_hits = [hit for hit in result if hit.meta.id not in sent_ids]
					if not new_hits:
						self._log("Events already sent. No alert sent.", 2, tag)
					else:
						for hit in new_hits:
							sent_ids[hit.meta.id] = None
						while len(sent_ids) > Constants.MAX_SENT_IDS:
							sent_ids.popitem(last = False)
						messages = self.generate_telegram_messages(new_hits, rule, total, total - len(result))
						queued = sum(sender.put(priority, message, rule["name"]) for message in messages)
						self._log(f"Alert queued: {len(new_hits)} event(s) in {queued}/{len(messages)} message(s)", 2, tag, to_file = True)
			except Exception as exception:
				self._log(f"Error running the alert rule: {exception}", 4, tag, to_file = True)
			with self.lock:
				self.heartbeats[rule["name"]] = {"last_run": time(), "interval": search_seconds}
			self.stop.wait(max(0.0, search_seconds - (monotonic() - started)))


	def _sender(self, telegram_bot_token: str, telegram_chat_id: str) -> TelegramSender:
		"""
		Method that returns the sending queue of a bot + chat (created and started the first time).
		"""
		with self.lock:
			key = (telegram_bot_token, telegram_chat_id)
			if key not in self.senders:
				sender = TelegramSender(telegram_bot_token, telegram_chat_id, self.stop, self._log, self.create_log_by_telegram_code, Constants.TELEGRAM_SEND_INTERVAL, Constants.MAX_QUEUE_SIZE)
				sender.start()
				self.senders[key] = sender
			return self.senders[key]


	def generate_telegram_messages(self, hits: list, rule: dict, total: int, omitted: int) -> list:
		"""
		Method that groups the events in as few Telegram messages as possible (each one under TELEGRAM_MAX_LENGTH).
		The first message has the full header; the next ones a short one. An event that doesn't fit alone is truncated.

		Parameters:
			hits (list): New events to send (newest first).
			rule (dict): Object that contains the alert rule's configuration data.
			total (int): Total number of events found.
			omitted (int): Events found but not retrieved (over MAX_EVENTS_PER_ALERT).

		Returns:
			messages (list): Messages to send.
		"""
		limit = Constants.TELEGRAM_MAX_LENGTH
		name = rule["name"]
		header = (f"{WARNING_ICON} {name} {WARNING_ICON}\n\n{LEVEL_ICON} Alert level: {rule['level']}\n\n{CLOCK_ICON} Alert sent: {strftime('%c')}\n\n"
			f"{total} event(s) were found (threshold: {rule['total_events']}). New event(s) sent: {len(hits)}.\n\n")
		footer = f"{WARNING_ICON} {omitted} more event(s) were found but not sent. Check them in Kibana." if omitted > 0 else ""
		# Space reserved for the label "EVENTS 1-7 OF 50 (1/9):" / the short header of the next messages.
		label_room = 40
		short_header_room = telegram_length(f"{WARNING_ICON} {name} — ") + label_room

		groups = []
		current, current_length, capacity = [], 0, limit - telegram_length(header) - label_room
		for number, hit in enumerate(hits, start = 1):
			text = f"━━━━ Event {number} ━━━━\n" + self.elasticsearch.convert_data_to_str(hit).rstrip("\n") + "\n\n"
			length = telegram_length(text)
			if current and current_length + length > capacity:
				groups.append(current)
				current, current_length, capacity = [], 0, limit - short_header_room
			if length > capacity:
				while text and telegram_length(text) > capacity - 15:
					text = text[:-max(1, (telegram_length(text) - capacity + 15))]
				text += "\n(truncated)\n\n"
				length = telegram_length(text)
			current.append((number, text))
			current_length += length
		if current:
			groups.append(current)

		messages = []
		for index, group in enumerate(groups, start = 1):
			label = f"EVENTS {group[0][0]}-{group[-1][0]} OF {len(hits)} ({index}/{len(groups)})"
			first = header + label + ":\n\n" if index == 1 else f"{WARNING_ICON} {name} — {label}\n\n"
			messages.append(first + "".join(text for _, text in group))
		if footer:
			if telegram_length(messages[-1] + footer) <= limit:
				messages[-1] += footer
			else:
				messages.append(f"{WARNING_ICON} {name} {WARNING_ICON}\n\n" + footer)
		return [message.rstrip("\n") for message in messages]


	def create_log_by_telegram_code(self, response_http_code: int, name: str) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
			name (str): Alert rule's name.
		"""
		level, message = TELEGRAM_CODES.get(response_http_code, (4, f"Telegram message not sent. HTTP {response_http_code}."))
		self._log(message, level, f"_{name}", to_file = True)