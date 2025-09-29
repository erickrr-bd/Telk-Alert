"""
Class that manages everything related to Telk-Alert.
"""
from os import path
from threading import Thread
from libPyLog import libPyLog
from libPyElk import libPyElk
from time import sleep, strftime
from libPyUtils import libPyUtils
from dataclasses import dataclass
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from libPyConfiguration import libPyConfiguration
from apscheduler.schedulers.background import BackgroundScheduler

@dataclass
class TelkAlert:
	
	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.elasticsearch = libPyElk()
		self.telegram = libPyTelegram()
		self.scheduler = BackgroundScheduler()
		self.configuration = libPyConfiguration()
		self.scheduler.start()


	def run_as_daemon(self) -> None:
		"""
		Method that runs the application as a daemon.
		"""
		try:
			self.start_telk_alert()
			while True:
				sleep(60)
		except (KeyboardInterrupt, SystemExit)  as exception:
			self.scheduler.shutdown()
			self.logger.create_log("Telk-Alert daemon stopped", 2, "_daemon", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_telk_alert(self) -> None:
		"""
		Method that starts Telk-Alert.
		"""
		try:
			self.logger.create_log("Author: Erick Roberto Rodríguez Rodríguez", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Github: https://github.com/erickrr-bd/Telk-Alert", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Telk-Alert v4.1 - September 2025", 2, "_start", use_stream_handler = True)
			if path.exists(self.constants.TELK_ALERT_CONFIGURATION):
				self.logger.create_log(f"Configuration found: {self.constants.TELK_ALERT_CONFIGURATION}", 2, "_readConfiguration", use_stream_handler = True)
				configuration = libPyConfiguration()
				data = self.utils.read_yaml_file(self.constants.TELK_ALERT_CONFIGURATION)
				configuration.convert_dict_to_object(data)
				if configuration.use_authentication:
					if configuration.authentication_method == "HTTP Authentication":
						conn_es = self.elasticsearch.create_connection_http_auth(configuration, self.constants.KEY_FILE)
					elif configuration.authentication_method == "API Key":
						conn_es = self.elasticsearch.create_connection_api_key(configuration, self.constants.KEY_FILE)
				else:
					conn_es = self.elasticsearch.create_connection_without_auth(configuration)
				self.logger.create_log(f"Connection established: {','.join(configuration.es_host)}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Cluster Name: {conn_es.info()["cluster_name"]}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Cluster UUID: {conn_es.info()["cluster_uuid"]}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Version: {conn_es.info()["version"]["number"]}", 2, "_clusterConnection", use_stream_handler = True)
				if configuration.use_authentication:
					self.logger.create_log("Authentication enabled", 2, "_clusterConnection", use_stream_handler = True)
					self.logger.create_log("Authentication Method: HTTP Authentication", 2, "_clusterConnection", use_stream_handler = True) if configuration.authentication_method == "HTTP Authentication" else self.logger.create_log("Authentication Method: API Key", 2, "_clusterConnection", use_stream_handler = True)
				else:
					self.logger.create_log("Authentication disabled. Not recommended for security reasons.", 3, "_clusterConnection", use_stream_handler = True)
				if configuration.verificate_certificate_ssl:
					self.logger.create_log("SSL Certificate verification enabled", 2, "_clusterConnection", use_stream_handler = True)
					self.logger.create_log(f"SSL Certificate: {configuration.certificate_file}", 2, "_clusterConnection", use_stream_handler = True)
				else:
					self.logger.create_log("Certificate verification disabled. Not recommended for security reasons.", 3, "_clusterConnection", use_stream_handler = True)
				alert_rules = self.utils.get_yaml_files_in_folder(self.constants.ALERT_RULES_FOLDER)
				if alert_rules:
					self.logger.create_log(f"{str(len(alert_rules))} alert rule(s) in: {self.constants.ALERT_RULES_FOLDER}", 2 , "_readAlertRules", use_stream_handler = True)
					for alert_rule in alert_rules:
						alert_rule_data = self.utils.read_yaml_file(f"{self.constants.ALERT_RULES_FOLDER}/{alert_rule}")
						self.logger.create_log(f"Alert rule: {alert_rule_data["name"]}", 2, "_loadAlertRule", use_stream_handler = True)
						self.start_alert_rule(conn_es, alert_rule_data)
				else:
					self.logger.create_log(f"No alert rules in: {self.constants.ALERT_RULES_FOLDER}", 3, "_readAlertRules", use_stream_handler = True)
			else:
				self.logger.create_log("Configuration not found.", 4, "_readConfiguration", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log("Error starting Telk-Alert. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_start", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_alert_rule(self, conn_es, alert_rule_data: dict) -> None:
		"""
		Method that executes a task in a defined time interval.

		Parameters:
			conn_es (ElasticSearch): A straightforward mapping from Python to ES REST endpoints.
			alert_rule_data (dict): Object that contains the alert rule's configuration data.
		"""
		unit_time = list(alert_rule_data["search_time"].keys())[0]
		search_time = alert_rule_data["search_time"][unit_time]
		interval_args = {unit_time : search_time}
		self.scheduler.add_job(self.alert_rule_search, "interval", **interval_args, args = [conn_es, alert_rule_data], id = alert_rule_data["name"], replace_existing = True)


	def alert_rule_search(self, conn_es, alert_rule_data: dict) -> None:
		"""
		Method that executes an alert rule.

		Parameters:
			conn_es (ElasticSearch): A straightforward mapping from Python to ES REST endpoints.
			alert_rule_data (dict): Object that contains the alert rule's configuration data.
		"""
		try:
			unit_time = list(alert_rule_data["range_time"].keys())[0]
			gte_date = self.utils.get_gte_date(unit_time, alert_rule_data["range_time"][unit_time])
			lte_date = self.utils.get_lte_date(unit_time)
			query_type = list(alert_rule_data["query"]["query_type"][0].keys())[0]
			if not alert_rule_data["is_custom_rule"]:
				match query_type:
					case "query_string":
						query_string = alert_rule_data["query"]["query_type"][0]["query_string"]["query"]
						if alert_rule_data["use_fields"]:
							result = self.elasticsearch.search_query_string(conn_es, alert_rule_data["index_pattern"], query_string, alert_rule_data["timestamp_field"], gte_date, lte_date, alert_rule_data["use_fields"], fields = alert_rule_data["fields"])
						else:
							result = self.elasticsearch.search_query_string(conn_es, alert_rule_data["index_pattern"], query_string, alert_rule_data["timestamp_field"], gte_date, lte_date, alert_rule_data["use_fields"])
						if result:
							if len(result) >= alert_rule_data["total_events"]:
								self.logger.create_log(f"Events found: {str(len(result))}", 2, f"_{alert_rule_data["name"]}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
								self.send_telegram_alert(result, alert_rule_data)
						else:
							self.logger.create_log("No events", 2, f"_{alert_rule_data["name"]}", use_stream_handler = True)
			else:
				match alert_rule_data["custom_rule_type"]:
					case "Brute Force":
						query_string = alert_rule_data["query"]["query_type"][0]["query_string"]["query"]
						result = self.elasticsearch.search_query_string_aggregation(conn_es, alert_rule_data["index_pattern"], query_string, alert_rule_data["timestamp_field"], gte_date, lte_date, alert_rule_data["hostname_field"], False)
						if result:
							for tag in result.aggregations.events.buckets:
								if tag.doc_count >= alert_rule_data["total_events"]:
									query_string += f" AND {alert_rule_data["hostname_field"]} : {tag.key}"
									result = self.elasticsearch.search_query_string_aggregation(conn_es, alert_rule_data["index_pattern"], query_string, alert_rule_data["timestamp_field"], gte_date, lte_date, alert_rule_data["username_field"], False)
									for tag in result.aggregations.events.buckets:
										if tag.doc_count >= alert_rule_data["total_events"]:
											query_string += f" AND {alert_rule_data["username_field"]} : {tag.key}"
											if alert_rule_data["use_fields"]:
												result = self.elasticsearch.search_query_string(conn_es, alert_rule_data["index_pattern"], query_string, alert_rule_data["timestamp_field"], gte_date, lte_date, alert_rule_data["use_fields"], fields = alert_rule_data["fields"])
											else:
												result = self.elasticsearch.search_query_string(conn_es, alert_rule_data["index_pattern"], query_string, alert_rule_data["timestamp_field"], gte_date, lte_date, alert_rule_data["use_fields"])
											self.logger.create_log(f"Events found: {str(len(result))}", 2, f"_{alert_rule_data["name"]}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
											self.send_telegram_alert(result, alert_rule_data)
						else:
							self.logger.create_log("No events", 2, f"_{alert_rule_data["name"]}", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log(f"Error running the alert rule: {alert_rule_data["name"]}. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, f"_{alert_rule_data["name"]}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def generate_telegram_message(self, hit: dict, alert_rule_data: dict) -> str:
		"""
		Method that generates the message to be sent via Telegram based on the data obtained from the search in ElasticSearch.

		Parameters:
			hit (dict): Event's data.
			alert_rule_data (dict): Object that contains the alert rule's configuration data.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{u'\u26A0\uFE0F'} {alert_rule_data["name"]} {u'\u26A0\uFE0F'}\n\n{u'\U0001f6a6'} Alert level: {alert_rule_data["level"]}\n\n{u'\u23F0'} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"At least {str(alert_rule_data["total_events"])} event(s) were found.\n\nFOUND EVENT:\n\n"
		telegram_message += self.elasticsearch.convert_data_to_str(hit)
		return telegram_message


	def send_telegram_alert(self, result, alert_rule_data: dict) -> None:
		"""
		Method that sends the found events to a Telegram channel.

		Parameters:
			result: Search's result.
			alert_rule_data (dict): Object that contains the alert rule's configuration data.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		telegram_bot_token = self.utils.decrypt_data(alert_rule_data["telegram_bot_token"], passphrase).decode("utf-8")
		telegram_chat_id = self.utils.decrypt_data(alert_rule_data["telegram_chat_id"], passphrase).decode("utf-8")
		for hit in result:
			telegram_message = self.generate_telegram_message(hit, alert_rule_data)
			if len(telegram_message) > 4096:
				telegram_message = f"{u'\u26A0\uFE0F'} {alert_rule_data["name"]} {u'\u26A0\uFE0F'}\n\n{u'\u270F\uFE0F'} The size of the message in Telegram (4096) has been exceeded. Overall size: {str(len(telegram_message))}"
			response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
			self.create_log_by_telegram_code(response_http_code, alert_rule_data["name"])


	def create_log_by_telegram_code(self, response_http_code: int, name: str) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
			name (str): Alert rule's name.
		"""
		match response_http_code:
			case 200:
				self.logger.create_log("Telegram message sent", 2, f"_{name}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 400:
				self.logger.create_log("Telegram message not sent. Bad request.", 4, f"_{name}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 401:
				self.logger.create_log("Telegram message not sent. Unauthorized.", 4, f"_{name}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 404:
				self.logger.create_log("Telegram message not sent. Not found.", 4, f"_{name}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
