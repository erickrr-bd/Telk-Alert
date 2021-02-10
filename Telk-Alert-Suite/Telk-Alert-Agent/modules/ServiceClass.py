import os
import time
import sys
from datetime import datetime
sys.path.append('./modules')
from UtilsClass import Utils
from LoggerClass import Logger
from TelegramClass import Telegram

"""
Class that allows to manage the operation of Telk-Alert-Agent.
"""
class Service:

	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Telegram type object.
	"""
	telegram = Telegram()

	"""
	Method that allows validating the status of the Telk-Alert service and sending an alert to Telegram.

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
				status_service = os.popen('(systemctl is-active --quiet telk_alert.service && echo "Running" || echo "Not running")')
				status_telk_alert = status_service.readlines()
				for status in status_telk_alert:
					status_s = status.rstrip('\n')
				message = self.telegram.getTelegramMessage(status_s)
				status_telegram = self.telegram.sendTelegramAgent(telegram_chat_id, telegram_bot_token, message)
				if status_telegram == 200:
					print("Telegram alert sent. Telk-Alert Service Status: " + str(status_s))
					self.logger.createLogAgent("Telegram alert sent. Telk-Alert Service Status: " + str(status_s), 2)
				if status_telegram == 400:
					print("Telegram alert not sent. Bad request.")
					self.logger.createLogAgent("Telegram alert not sent. Bad request.", 4)
				if status_telegram == 401:
					print("Telegram alert not sent. Unauthorized.")
					self.logger.createLogAgent("Telegram alert not sent. Unauthorized.", 4)
				if status_telegram == 404:
					print("Telegram alert not sent. Not found.")
					self.logger.createLogAgent("Telegram alert not sent. Not found.", 4)
			time.sleep(60)

		