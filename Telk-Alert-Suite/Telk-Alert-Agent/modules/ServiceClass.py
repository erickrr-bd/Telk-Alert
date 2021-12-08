from os import popen
from time import sleep
from datetime import datetime
from modules.UtilsClass import Utils
from modules.TelegramClass import Telegram

"""
Class that allows to manage the operation of Telk-Alert-Agent.
"""
class Service:
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores an object of type Telegram.
	"""
	telegram = None

	"""
	Constructor for the Service class.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def __init__(self):
		self.utils = Utils()
		self.telegram = Telegram()

	"""
	Method that validates the status of the Telk-Alert service and sends a message to Telegram with the result.

	Parameters:
	self -- An instantiated object of the Services class.
	"""
	def sendStatusTelkAlertService(self):
		data_agent_configuration = self.utils.readYamlFile(self.utils.getPathTelkAlertAgent('conf') + '/telk_alert_agent_conf.yaml', 'r')
		time_execution_one = data_agent_configuration['time_execution_one'].split(':')
		time_execution_two = data_agent_configuration['time_execution_two'].split(':')
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
			sleep(60)