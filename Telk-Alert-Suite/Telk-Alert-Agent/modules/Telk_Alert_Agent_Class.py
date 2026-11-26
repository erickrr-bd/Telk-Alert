"""
Class that manages everything related to Telk-Alert-Agent.
"""
from os import path
from time import time, strftime
from threading import Event
from dataclasses import dataclass, field
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyTelegram import libPyTelegram
from .Constants_Class import Constants

# Maximum total accepted for each unit of time (same limits as Telk-Alert-Tool).
MAX_TOTAL_BY_UNIT = {"minutes": 1440, "hours": 720, "days": 365}

# Log entry for each HTTP code returned by the Telegram API: (level, message).
TELEGRAM_CODES = {
	200: (2, "Telegram message sent"),
	400: (4, "Telegram message not sent. Bad request."),
	401: (4, "Telegram message not sent. Unauthorized."),
	403: (4, "Telegram message not sent. Forbidden (is the bot in the chat?)."),
	404: (4, "Telegram message not sent. Not found."),
	429: (3, "Telegram message not sent. Rate limited.")
}

# Telk-Alert's status: (icon, note).
STATUS = {
	"ok": ("🟢", "Telk-Alert service is working."),
	"down": ("🔴", "Telk-Alert service isn't working. systemd restarts it automatically after a failure; if it doesn't recover, report to an administrator (journalctl -u telk-alert)."),
	"stale": ("🟡", "Some alert rules stopped running."),
	"failed": ("🔴", "Some alert rules stopped running and Telk-Alert service couldn't be restarted. Report to an administrator.")
}

WARNING_ICON = "⚠️"
CLOCK_ICON = "⏰"
NOTE_ICON = "\U0001f4cb"


@dataclass
class TelkAlertAgent:

	logger: libPyLog = field(default_factory = libPyLog)
	utils: libPyUtils = field(default_factory = libPyUtils)
	stop: Event = field(default_factory = Event)
	interval: int = 0
	# repr = False: the secrets never appear if the object is printed or logged.
	telegram_bot_token: str = field(default = None, repr = False)
	telegram_chat_id: str = field(default = None, repr = False)
	last_status: str = None
	last_skipped: tuple = ()
	stale_checks: int = 0


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


	def _read_configuration(self) -> None:
		"""
		Method that reads and validates the configuration and decrypts the Telegram credentials once
		(the passphrase is wiped afterwards). Raises ValueError/IOError if something is wrong.
		"""
		data = self.utils.read_yaml_file(Constants.TELK_ALERT_AGENT_CONFIGURATION)
		frequency = data.get("frequency_time")
		if not isinstance(frequency, dict) or len(frequency) != 1:
			raise ValueError("Invalid frequency_time in the configuration file.")
		unit, total = next(iter(frequency.items()))
		if unit not in MAX_TOTAL_BY_UNIT or isinstance(total, bool) or not isinstance(total, int) or not 1 <= total <= MAX_TOTAL_BY_UNIT[unit]:
			raise ValueError("Invalid frequency_time in the configuration file.")
		self.interval = self.utils.convert_time_to_seconds(unit, total)
		passphrase = self.utils.get_passphrase(Constants.KEY_FILE, owner = Constants.USER)
		try:
			# allow_legacy: configurations created by the previous version. Remove it once they are saved again with Telk-Alert-Tool.
			self.telegram_bot_token, self.telegram_chat_id = (self.utils.decrypt_data(data[key], passphrase, allow_legacy = True, context = f"{Constants.CTX_AGENT}:{key}")
				for key in ("telegram_bot_token", "telegram_chat_id"))
		finally:
			self.utils.zeroize(passphrase)


	def _check_heartbeat(self) -> tuple:
		"""
		Method that reads the heartbeat written by Telk-Alert.

		Returns:
			(stale, skipped) (tuple): Alert rules that didn't run in 2 intervals + 1 minute (or the heartbeat itself
			                          if it isn't updated) and alert rules that couldn't start.
		"""
		heartbeat = self.utils.read_yaml_file(Constants.HEARTBEAT_FILE)
		now = time()
		skipped = tuple(heartbeat.get("skipped") or ())
		if now - heartbeat.get("updated", 0) > Constants.HEARTBEAT_MAX_AGE:
			return (["<heartbeat not updated>"], skipped)
		stale = [name for name, data in (heartbeat.get("rules") or {}).items() if now - data["last_run"] > data["interval"] * 2 + 60]
		return (stale, skipped)


	def _send(self, telegram: libPyTelegram, message: str) -> None:
		self.create_log_by_telegram_code(telegram.send_telegram_message(self.telegram_bot_token, self.telegram_chat_id, message))


	def _notify(self, telegram: libPyTelegram, status: str, detail: str = "") -> None:
		"""
		Method that sends Telk-Alert's status via Telegram only when it changes (including the recovery).
		"""
		if status == self.last_status:
			return
		first_check = self.last_status is None
		self.last_status = status
		if first_check and status == "ok":
			return
		icon, note = STATUS[status]
		message = (f"{WARNING_ICON} Telk-Alert Service {WARNING_ICON}\n\n{CLOCK_ICON} Service Status Validation Time: {strftime('%c')}\n\n\n"
			f"Telk-Alert Service Status: {icon}\n\n{NOTE_ICON} NOTE: {note}{detail}\n\n")
		self._send(telegram, message)


	def _notify_skipped(self, telegram: libPyTelegram, skipped: tuple) -> None:
		"""
		Method that reports the alert rules that couldn't start (only when the list changes). Restarting doesn't fix them.
		"""
		if skipped == self.last_skipped:
			return
		self.last_skipped = skipped
		if not skipped:
			return
		self._log(f"Alert rule(s) not started: {'; '.join(skipped)}", 3, "_statusService", to_file = True)
		self._send(telegram, f"{WARNING_ICON} Telk-Alert Service {WARNING_ICON}\n\n🟠 Alert rule(s) not started (fix them with Telk-Alert-Tool):\n\n" + "\n".join(f"- {item}" for item in skipped)[:3500])


	# --- Start ---------------------------------------------------------------------------------
	def start_telk_alert_agent(self) -> bool:
		"""
		Method that starts Telk-Alert-Agent.

		Returns:
			started (bool): True if the configuration is valid and the credentials could be decrypted.
		"""
		try:
			for line in ("Author: Erick Roberto Rodríguez Rodríguez", "Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", "Github: https://github.com/erickrr-bd/Telk-Alert", f"Telk-Alert-Agent v{Constants.VERSION} - {Constants.RELEASE_DATE}"):
				self._log(line, 2, "_start")
			if not path.exists(Constants.TELK_ALERT_AGENT_CONFIGURATION):
				self._log(f"Configuration not found: {Constants.TELK_ALERT_AGENT_CONFIGURATION}", 4, "_readConfiguration", to_file = True)
				return False
			self._log(f"Configuration found: {Constants.TELK_ALERT_AGENT_CONFIGURATION}", 2, "_readConfiguration")
			self._read_configuration()
			self._log(f"Validation interval: {self.interval} seconds", 2, "_readConfiguration")
			return True
		except Exception as exception:
			self._log("Error starting Telk-Alert-Agent. For more information, see the logs.", 4, "_start")
			self._log(exception, 4, "_start", to_file = True)
			return False


	def run(self) -> None:
		"""
		Method that validates Telk-Alert every interval until the agent is stopped (SIGTERM/SIGINT).
		"""
		with libPyTelegram() as telegram:
			while True:
				self.daemon_validator(telegram)
				if self.stop.wait(self.interval):
					break
		self._log("Telk-Alert-Agent daemon stopped", 2, "_daemon", to_file = True)


	# --- Validation ----------------------------------------------------------------------------
	def daemon_validator(self, telegram: libPyTelegram) -> None:
		"""
		Method that validates the status of the Telk-Alert's daemon and its alert rules.
		- Service down: notify (systemd restarts it with Restart=on-failure; a manual stop is respected).
		- Alert rules not running: restart the service after STALE_CHECKS_BEFORE_RESTART consecutive checks.
		- Alert rules that couldn't start: notify only.

		Parameters:
			telegram (libPyTelegram): Telegram client.
		"""
		try:
			status = self.utils.get_status_by_daemon(Constants.TELK_ALERT_SERVICE)
			self._log(f"Telk-Alert service status: {status}", 2, "_statusService")
			if status != "Running":
				self.stale_checks = 0
				self._notify(telegram, "down")
				return
			try:
				stale, skipped = self._check_heartbeat()
			except Exception as exception:
				stale, skipped = [f"<heartbeat not available: {exception}>"], self.last_skipped
			self._notify_skipped(telegram, skipped)
			if not stale:
				self.stale_checks = 0
				self._notify(telegram, "ok")
				return
			self.stale_checks += 1
			self._log(f"Alert rule(s) not running: {', '.join(stale)} (check {self.stale_checks}/{Constants.STALE_CHECKS_BEFORE_RESTART})", 3, "_statusService", to_file = True)
			if self.stale_checks < Constants.STALE_CHECKS_BEFORE_RESTART:
				return
			self.stale_checks = 0
			if self.utils.manage_daemon(Constants.TELK_ALERT_SERVICE, 2) == 0:
				self._log("Telk-Alert service has been restarted because some alert rules stopped running", 3, "_statusService", to_file = True)
				detail = f" Telk-Alert service has been restarted.\n\nAlert rule(s): {', '.join(stale)}"
			else:
				error = self.utils.last_error or "Unknown error."
				self._log(f"Telk-Alert service couldn't be restarted: {error}", 4, "_statusService", to_file = True)
				self._notify(telegram, "failed", f"\n\nError: {error[:300]}\n\nAlert rule(s): {', '.join(stale)}")
				return
			self._notify(telegram, "stale", detail)
		except Exception as exception:
			self._log("Error validating Telk-Alert status. For more information, see the logs.", 4, "_statusService")
			self._log(exception, 4, "_statusService", to_file = True)


	def create_log_by_telegram_code(self, response_http_code: int) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
		"""
		level, message = TELEGRAM_CODES.get(response_http_code, (4, f"Telegram message not sent. HTTP {response_http_code}."))
		self._log(message, level, "_sendTelegramMessage", to_file = True)