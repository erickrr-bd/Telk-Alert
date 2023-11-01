from os import path
from time import sleep
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from .Telegram_Messages_Class import TelegramMessages

"""
Class that manages Telk-Alert-Agent actions.
"""
class TelkAlertAgent:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.telegram = libPyTelegram()
		self.telegram_messages = TelegramMessages()


	def start_telk_alert_agent(self):
		"""
		Method that starts Telk-Alert-Agent.
		"""
		try:
			self.logger.generateApplicationLog("Copyright@2023 Tekium. All rights reserved.", 1, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog("Author: Erick Roberto Rodríguez Rodríguez", 1, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 1, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog("Github: https://github.com/erickrr-bd/Telk-Alert", 1, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog("Telk-Alert-Agent v3.3 - November 2023", 1, "__start", use_stream_handler = True)
			if path.exists(self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH):
				self.logger.generateApplicationLog("Reading configuration file in: " + self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH, 1, "__readConfigurationFile", use_stream_handler = True)
				telk_alert_agent_data = self.utils.readYamlFile(self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH)
				alert_rules_folder = self.utils.readYamlFile(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)["alert_rules_folder"]
				search_unit_time = list(telk_alert_agent_data["service_validation_time"].keys())[0]
				service_validation_time = self.utils.convertTimeToSeconds(search_unit_time, telk_alert_agent_data["service_validation_time"][search_unit_time])
				passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
				telegram_bot_token = self.utils.decryptDataWithAES(telk_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")
				telegram_chat_id = self.utils.decryptDataWithAES(telk_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")
				while True:
					telk_alert_service_status = self.utils.getStatusbyService("telk-alert.service")
					self.logger.generateApplicationLog("Telk-Alert service status: " + telk_alert_service_status, 1, "__serviceStatus", use_stream_handler = True)
					if telk_alert_service_status == "Not running":
						telegram_message = self.telegram_messages.generate_telegram_message(telk_alert_service_status)
						response_http_code = self.telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, telegram_message)
						self.telegram_messages.create_log_by_telegram_code(response_http_code)
					else:
						telk_alert_service_pid = self.utils.getPidbyDaemon("telk-alert")
						threads_number = self.utils.getThreadsNumberbyPid(telk_alert_service_pid)
						total_alert_rules = len(self.utils.getListYamlFilesInFolder(self.constants.TELK_ALERT_PATH + '/' + alert_rules_folder))
						if not (threads_number - 1) == total_alert_rules:
							telegram_message = self.telegram_messages.generate_telegram_message_threads(threads_number, total_alert_rules)
							response_http_code == self.telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, telegram_message)
							self.telegram_messages.create_log_by_telegram_code(response_http_code)
						self.logger.generateApplicationLog("Threads: " + str((threads_number - 1)) + ", Alert rules: " + str(total_alert_rules), 1, "__numberThreads", use_stream_handler = True)
					sleep(service_validation_time)
			else:
				self.logger.generateApplicationLog("Configuration file not found", 3, "__readConfigurationFile", use_stream_handler = True)
		except Exception as exception:
			self.logger.generateApplicationLog("Error starting Telk-Alert-Agent. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)