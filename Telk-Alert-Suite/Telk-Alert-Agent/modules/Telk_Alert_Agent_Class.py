from os import path
from libPyLog import libPyLog
from time import sleep, strftime
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from dataclasses import dataclass, field

@dataclass
class TelkAlertAgent:
	"""
	Class that manages the operation of Telk-Alert-Agent.
	"""

	logger: libPyLog = field(default_factory = libPyLog)
	utils: libPyUtils = field(default_factory = libPyUtils)
	constants: Constants = field(default_factory = Constants)
	telegram: libPyTelegram = field(default_factory = libPyTelegram)


	def start_telk_alert_agent(self) -> None:
		"""
		Method that starts Telk-Alert-Agent.
		"""
		try:
			self.logger.create_log("Author: Erick Roberto Rodríguez Rodríguez", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Github: https://github.com/erickrr-bd/Telk-Alert", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Telk-Alert-Agent v4.0 - April 2025", 2, "_start", use_stream_handler = True)
			if path.exists(self.constants.TELK_ALERT_AGENT_CONFIGURATION):
				self.logger.create_log(f"Configuration found: {self.constants.TELK_ALERT_AGENT_CONFIGURATION}", 2, "_readConfiguration", use_stream_handler = True)
				telk_alert_agent_data = self.utils.read_yaml_file(self.constants.TELK_ALERT_AGENT_CONFIGURATION)
				unit_time = list(telk_alert_agent_data["frequency_time"].keys())[0]
				frequency_time = self.utils.convert_time_to_seconds(unit_time, telk_alert_agent_data["frequency_time"][unit_time])
				passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
				telegram_bot_token = self.utils.decrypt_data(telk_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")
				telegram_chat_id = self.utils.decrypt_data(telk_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")
				while True:
					telk_alert_status = self.utils.get_status_by_daemon("telk-alert.service")
					self.logger.create_log(f"Telk-Alert service status: {telk_alert_status}", 2, "_statusService", use_stream_handler = True)
					if telk_alert_status == "Not running":
						telegram_message = self.generate_telegram_message(telk_alert_status)
						response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
						self.create_log_by_telegram_code(response_http_code)
						result = self.utils.manage_daemon("telk-alert.service", 1)
						if result == 0:
							self.logger.create_log("Telk-Alert service has been started", 3, "_statusService", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
					else:
						telk_alert_pid = self.utils.get_pid_by_daemon("telk-alert.service")
						telk_alert_threads = self.utils.get_threads_by_pid(telk_alert_pid)
						alert_rules = len(self.utils.get_yaml_files_in_folder(self.constants.ALERT_RULES_FOLDER))
						if not (telk_alert_threads - 1) == alert_rules:	
							telegram_message = self.generate_telegram_message_threads(telk_alert_threads, alert_rules)
							response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
							self.create_log_by_telegram_code(response_http_code)
							result = self.utils.manage_daemon("telk-alert.service", 2)
							if result == 0:
								self.logger.create_log(f"Telk-Alert service has been restarted because there are {str(telk_alert_threads - 1)}/{alert_rules} alert rules running", 3, "_statusService", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
						self.logger.create_log(f"Threads: {telk_alert_threads - 1}, Alert Rules: {alert_rules}", 2, "_statusService", use_stream_handler = True)
					sleep(frequency_time)
			else:
				self.logger.create_log("Configuration not found.", 4, "_readConfiguration", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log("Error starting Telk-Alert-Agent. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_start", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def generate_telegram_message(self, telk_alert_status: str) -> str:
		"""
		Method that generates the message to be sent via Telegram based on the current status of the Telk-Alert daemon.

		Parameters:
			telk_alert_status (str): Status of the Telk-Alert demon.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{u'\u26A0\uFE0F'} Telk-Alert Service {u'\u26A0\uFE0F'}\n\n{u'\u23F0'} Service Status Validation Time: {strftime("%c")}\n\n\n"
		telegram_message += "Telk-Alert Service Status: 🔴\n\n"
		telegram_message += f"{u'\U0001f4cb'} NOTE: The red circle indicates that Telk-Alert service isn't working. Report to an administrator.\n\n"
		return telegram_message


	def generate_telegram_message_threads(self, total_threads: int, alert_rules: int) -> str:
		"""
		Method that generates the message to be sent via Telegram based on the number of threads and alert rules in use.

		Parameters:
			total_threads (int): Total number of threads running.
			alert_rules (int): Total alert rules created.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{u'\u26A0\uFE0F'} Telk-Alert Service {u'\u26A0\uFE0F'}\n\n{u'\u23F0'} Service Status Validation Time: {strftime("%c")}\n\n\n"
		telegram_message += "Telk-Alert Service Status: 🟡\n\n"
		telegram_message += f"{u'\U0001f4cb'} NOTE: Telk-Alert service has been restarted because there are {str(total_threads - 1)}/{alert_rules} alert rules running.\n\n"
		return telegram_message


	def create_log_by_telegram_code(self, response_http_code: int) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
		"""
		match response_http_code:
			case 200:
				self.logger.create_log("Telegram message sent", 2, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 400:
				self.logger.create_log("Telegram message not sent. Bad request.", 4, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 401:
				self.logger.create_log("Telegram message not sent. Unauthorized.", 4, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 404:
				self.logger.create_log("Telegram message not sent. Not found.", 4, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
