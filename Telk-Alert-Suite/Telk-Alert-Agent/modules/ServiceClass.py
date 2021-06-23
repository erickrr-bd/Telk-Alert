import os
import time
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
		agent_conf_data = self.utils.readFileYaml(self.utils.getPathTagent('conf') + '/agent_conf.yaml')
		time_agent_one = agent_conf_data['time_agent_one'].split(':')
		time_agent_two = agent_conf_data['time_agent_two'].split(':')
		telegram_bot_token = self.utils.decryptAES(agent_conf_data['telegram_bot_token']).decode('utf-8')
		telegram_chat_id = self.utils.decryptAES(agent_conf_data['telegram_chat_id']).decode('utf-8')
		while True:
			now = datetime.now()
			if(now.hour == int(time_agent_one[0]) and now.minute == int(time_agent_one[1])) or (now.hour == int(time_agent_two[0]) and now.minute == int(time_agent_two[1])):
				status_service = os.popen('(systemctl is-active --quiet telk-alert.service && echo "Running" || echo "Not running")')
				status_telk_alert = status_service.readlines()
				for status in status_telk_alert:
					status_s = status.rstrip('\n')
				message = self.telegram.getTelegramMessage(status_s)
				status_telegram = self.telegram.sendTelegramAgent(telegram_chat_id, telegram_bot_token, message)
				self.telegram.getStatusByTelegramCode(status_telegram, status_s)
			time.sleep(60)

		