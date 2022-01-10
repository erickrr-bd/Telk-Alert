from os import popen
from time import sleep
from datetime import datetime
from modules.UtilsClass import Utils
from modules.TelegramClass import Telegram

"""
Class that allows to manage the operation of Telk-Alert-Agent.
"""
class TelkAlertAgent:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Property that stores an object of the Telegram class.
	"""
	telegram = None

	"""
	Constructor for the TelkAlertAgent class.

	Parameters:
	self -- An instantiated object of the TelkAlertAgent class.
	"""
	def __init__(self):
		self.utils = Utils()
		self.telegram = Telegram()

	"""
	Method that starts the Telk-Alert-Agent operation.

	Parameters:
	self -- An instantiated object of the TelkAlertAgent class.
	"""
	def startTelkAlertAgent(self):
		data_agent_configuration = self.utils.readYamlFile(self.utils.getPathTelkAlertAgent('conf') + '/telk_alert_agent_conf.yaml', 'r')
		time_execution_one = data_agent_configuration['time_execution_one'].split(':')
		time_execution_two = data_agent_configuration['time_execution_two'].split(':')
		self.utils.createTelkAlertAgentLog("Telk-Alert-Agent v3.1", 1)
		self.utils.createTelkAlertAgentLog("@2022 Tekium. All rights reserved.", 1)
		self.utils.createTelkAlertAgentLog("Author: Erick Rodriguez", 1)
		self.utils.createTelkAlertAgentLog("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com", 1)
		self.utils.createTelkAlertAgentLog("License: GPLv3", 1)
		self.utils.createTelkAlertAgentLog("Telk-Alert-Agent started...", 1)
		while True:
			result_status_service_telk_alert = popen('(systemctl is-active --quiet telk-alert.service && echo "Running" || echo "Not running")')
			status_service_telk_alert_aux = result_status_service_telk_alert.readlines()
			for status in status_service_telk_alert_aux:
				status_service_telk_alert = status.rstrip('\n')
			if status_service_telk_alert == "Not running":
				message_telegram = self.telegram.getTelegramMessage(status_service_telk_alert)
				self.telegram.sendTelegramAlert(self.utils.decryptAES(data_agent_configuration['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(data_agent_configuration['telegram_bot_token']).decode('utf-8'), message_telegram)
			else:
				now = datetime.now()
				if(now.hour == int(time_execution_one[0]) and now.minute == int(time_execution_one[1])) or (now.hour == int(time_execution_two[0]) and now.minute == int(time_execution_two[1])):
					message_telegram = self.telegram.getTelegramMessage(status_service_telk_alert)
					self.telegram.sendTelegramAlert(self.utils.decryptAES(data_agent_configuration['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(data_agent_configuration['telegram_bot_token']).decode('utf-8'), message_telegram)
			self.utils.createTelkAlertAgentLog("Telk-Alert service status: " + status_service_telk_alert, 1)
			sleep(60)