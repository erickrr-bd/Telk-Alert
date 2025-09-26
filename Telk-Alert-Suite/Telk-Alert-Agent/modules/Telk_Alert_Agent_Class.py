"""
Class that manages everything related to Telk-Alert-Tool.
"""
from os import path
from libPyLog import libPyLog
from time import sleep, strftime
from dataclasses import dataclass
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from apscheduler.schedulers.background import BackgroundScheduler

@dataclass
class TelkAlertAgent:

	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.telegram = libPyTelegram()
		self.scheduler = BackgroundScheduler()
		self.scheduler.start()


	def run_as_daemon(self) -> None:
		"""
		Method that runs the application as a daemon.
		"""
		try:
			self.start_telk_alert_agent()
			while True:
				sleep(60)
		except (KeyboardInterrupt, SystemExit) as exception:
			self.scheduler.shutdown()
			self.logger.create_log("Telk-Alert-Agent daemon stopped", 2, "_daemon", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_telk_alert_agent(self) -> None:
		"""
		Method that starts Telk-Alert-Agent.
		"""
		try:
			self.logger.create_log("Author: Erick Roberto Rodríguez Rodríguez", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Github: https://github.com/erickrr-bd/Telk-Alert", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Telk-Alert-Agent v4.1 - September 2025", 2, "_start", use_stream_handler = True)
			if path.exists(self.constants.TELK_ALERT_AGENT_CONFIGURATION):
				self.logger.create_log(f"Configuration found: {self.constants.TELK_ALERT_AGENT_CONFIGURATION}", 2, "_readConfiguration", use_stream_handler = True)
				telk_alert_agent_data = self.utils.read_yaml_file(self.constants.TELK_ALERT_AGENT_CONFIGURATION)
				self.start_daemon_validation(telk_alert_agent_data)
			else:
				self.logger.create_log("Configuration not found.", 4, "_readConfiguration", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log("Error starting Telk-Alert-Agent. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_start", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_daemon_validation(self, telk_alert_agent_data: dict) -> None:
		"""
		Method that executes a task in a defined time interval.

		Parameters:
			di_alert_agent_data (dict): Object that contains the Telk-Alert-Agent's configuration data.
		"""
		unit_time = list(telk_alert_agent_data["frequency_time"].keys())[0]
		frequency_time = telk_alert_agent_data["frequency_time"][unit_time]
		interval_args = {unit_time : frequency_time}
		self.scheduler.add_job(self.daemon_validator, "interval", **interval_args, args = [telk_alert_agent_data], id = "daemon_validation", replace_existing = True)


	def daemon_validator(self, telk_alert_agent_data: dict) -> None:
		"""
		Method that validates the status of the Telk-Alert's daemon.

		Parameters:
			di_alert_agent_data (dict): Object that contains the Telk-Alert-Agent's configuration data.
		"""
		try:
			telk_alert_status = self.utils.get_status_by_daemon("telk-alert.service")
			self.logger.create_log(f"Telk-Alert service status: {telk_alert_status}", 2, "_statusService", use_stream_handler = True)
			if telk_alert_status == "Not running":
				passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
				telegram_bot_token = self.utils.decrypt_data(telk_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")
				telegram_chat_id = self.utils.decrypt_data(telk_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")
				telegram_message = self.generate_telegram_message()
				response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
				self.create_log_by_telegram_code(response_http_code)
				result = self.utils.manage_daemon("telk-alert.service", 1)
				if result == 0:
					self.logger.create_log("Telk-Alert service has been started", 3, "_statusService", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			else:
				telk_alert_pid = self.utils.get_pid_by_daemon("telk-alert.service")
				telk_alert_threads = self.utils.get_threads_by_pid(telk_alert_pid)
				alert_rules = len(self.utils.get_yaml_files_in_folder(self.constants.ALERT_RULES_FOLDER))
				if (telk_alert_threads - 1) < alert_rules:
					passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
					telegram_bot_token = self.utils.decrypt_data(telk_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")
					telegram_chat_id = self.utils.decrypt_data(telk_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")
					telegram_message = self.generate_telegram_message_threads(telk_alert_threads, alert_rules)
					response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
					self.create_log_by_telegram_code(response_http_code)
					result = self.utils.manage_daemon("telk-alert.service", 2)
					if result == 0:
						self.logger.create_log(f"Telk-Alert service has been restarted because there are {str(telk_alert_threads - 1)}/{alert_rules} alert rules running", 3, "_statusService", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				self.logger.create_log(f"Threads: {telk_alert_threads - 1}, Alert Rules: {alert_rules}", 2, "_statusService", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log("Error validating Telk-Alert status. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_statusService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def generate_telegram_message(self) -> str:
		"""
		Method that generates the message to be sent via Telegram when the service isn't working.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{u'\u26A0\uFE0F'} Telk-Alert Service {u'\u26A0\uFE0F'}\n\n{u'\u23F0'} Service Status Validation Time: {strftime("%c")}\n\n\n"
		telegram_message += "Telk-Alert Service Status: 🔴\n\n"
		telegram_message += f"{u'\U0001f4cb'} NOTE: The red circle indicates that Telk-Alert service isn't working. Report to an administrator.\n\n"
		return telegram_message


	def generate_telegram_message_threads(self, total_threads: int, alert_rules: int) -> str:
		"""
		Method that generates the message to be sent via Telegram when the number of threads is less than the number of alert rules.

		Parameters:
			total_threads (int): Number of threads running.
			alert_rules (int): Alert rules number.

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
