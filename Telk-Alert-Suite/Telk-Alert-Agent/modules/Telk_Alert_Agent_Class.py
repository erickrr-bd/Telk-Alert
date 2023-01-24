from os import popen
from datetime import datetime
from libPyLog import libPyLog
from time import sleep,strftime
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram

"""
Class that manages the operation of Telk-Alert-Agent.
"""
class TelkAlertAgent:

	def __init__(self):
		"""
		Method that corresponds to the constructor of the class.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__telegram = libPyTelegram()


	def startTelkAlertAgent(self):
		"""
		Method that starts the Telk-Alert-Agent application.
		"""
		try:
			telk_alert_agent_data = self.__utils.readYamlFile(self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE)
			first_execution = telk_alert_agent_data["first_execution"].split(':')
			second_execution = telk_alert_agent_data["second_execution"].split(':')
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			telegram_bot_token = self.__utils.decryptDataWithAES(telk_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")
			telegram_chat_id = self.__utils.decryptDataWithAES(telk_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")
			self.__logger.generateApplicationLog("Telk-Alert-Agent v3.3", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("@2023 Tekium. All rights reserved.", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("Author: Erick Rodriguez", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("License: GPLv3", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("Telk-Alert-Agent started", 1, "__start", use_stream_handler = True)
			while True:
				telk_alert_service_command = popen('(systemctl is-active --quiet telk-alert.service && echo "Running" || echo "Not running")')
				result_command_lines = telk_alert_service_command.readlines()
				for line in result_command_lines:
					telk_alert_service_status = line.rstrip('\n')
				if telk_alert_service_status == "Not running":
					message_telegram = self.__generateTelegramMessage(telk_alert_service_status)
					response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
					self.__createLogByTelegramCode(response_http_code)
					self.__logger.generateApplicationLog("Status: " + telk_alert_service_status, 2, "__serviceStatus", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
				else:
					now = datetime.now()
					if(now.hour == int(first_execution[0]) and now.minute == int(first_execution[1])) or (now.hour == int(second_execution[0]) and now.minute == int(second_execution[1])):
						message_telegram = self.__generateTelegramMessage(telk_alert_service_status)
						response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
						self.__createLogByTelegramCode(response_http_code)
				self.__logger.generateApplicationLog("Status: " + telk_alert_service_status, 1, "__serviceStatus", use_stream_handler = True)
				sleep(60)
		except KeyError as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__start", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (OSError, FileNotFoundError) as exception:
			self.__logger.generateApplicationLog("File Not Found or OS Error. For more information, see the logs.", 3, "__readConfiguration", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__start", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)


	def __generateTelegramMessage(self, telk_alert_service_status):
		"""
		Method that generates the Telegram message based on Telk-Alert service's status.

		Returns the Telegram message.

		:arg telk_alert_service_status (string): Current status of Telk-Alert service.
		"""
		message_telegram = "" + u'\u26A0\uFE0F' + " Telk-Alert Service " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + "Service Status Validation Time: " + strftime("%c") + "\n\n\n"
		if telk_alert_service_status == "Not running":
			message_telegram += "Telk-Alert Service Status: " + u'\U0001f534' + "\n\n"
		elif telk_alert_service_status == "Running":
			message_telegram += "Telk-Alert Service Status: " + u'\U0001f7e2' + "\n\n"
		message_telegram += "" + u'\U0001f4cb' + " " + "Note 1: The green circle indicates that Telk-Alert service is working without problems." + "\n\n"
		message_telegram += "" + u'\U0001f4cb' + " " + "Note 2: The red circle indicates that Telk-Alert service isn't working. Report to an administrator." + "\n\n"
		return message_telegram


	def __createLogByTelegramCode(self, response_http_code):
		"""
		Method that creates a log based on the response's HTTP code.

		:arg response_http_code (integer): Telegram response's HTTP code.
		"""
		if response_http_code == 200:
			self.__logger.generateApplicationLog("Telegram message sent (200).", 1, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 400:
			self.__logger.generateApplicationLog("Telegram message not sent. Bad request (400).", 3, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 401:
			self.__logger.generateApplicationLog("Telegram message not sent. Unauthorized (401).", 3, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 404:
			self.__logger.generateApplicationLog("Telegram message not sent. Not found (404).", 3, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)