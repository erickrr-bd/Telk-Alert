import time
import pycurl
from urllib.parse import urlencode
from modules.LoggerClass import Logger

"""
Class that allows you to manage the sending of alerts through Telegram.
"""
class Telegram:
	"""
	Property that stores an object of type Logger.
	"""
	logger = None

	"""
	Constructor for the Telegram class.

	Parameters:
	self -- An instantiated object of the Telegram class.
	"""
	def __init__(self):
		self.logger = Logger()

	"""
	Method that sends the alert with the status of the service to Telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.
	telegram_chat_id -- Telegram channel identifier to which the letter will be sent.
	telegram_bot_token -- Token of the Telegram bot that is the administrator of the Telegram channel to which the alerts will be sent.
	message -- Message to be sent to the Telegram channel.

	Return:
	HTTP code.
	"""
	def sendTelegramAgent(self, telegram_chat_id, telegram_bot_token, message):
		c = pycurl.Curl()
		url = 'https://api.telegram.org/bot' + str(telegram_bot_token) + '/sendMessage'
		c.setopt(c.URL, url)
		data = { 'chat_id' : telegram_chat_id, 'text' : message }
		pf = urlencode(data)
		c.setopt(c.POSTFIELDS, pf)
		c.perform_rs()
		status_code = c.getinfo(pycurl.HTTP_CODE)
		c.close()
		return int(status_code)

	"""
	Method that generates the message that will be sent to Telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.
	status_s -- Current status of the Telk-Alert service.

	Return:
	message -- Message that will be sent via Telegram.
	"""
	def getTelegramMessage(self, status_s):
		message = "" + u'\u26A0\uFE0F' + "Telk-Alert Service " + u'\u26A0\uFE0F' + '\n\n' + u'\u23F0' + "Service Status Validation Time: " + time.strftime("%c") + "\n\n\n"
		if status_s == "Not running":
			message += "Service Telk-Alert Status: " + u'\U0001f534' + "\n\n"
		if status_s == "Running":
			message += "Service Telk-Alert Status: " + u'\U0001f7e2' + "\n\n"
		message += "" + u'\U0001f4cb' + " " + "Note 1: The green circle indicates that the Telk-Alert service is working without problems." + "\n\n"
		message += "" + u'\U0001f4cb' + " " + "Note 2: The red circle indicates that the Telk-Alert service is not working. Report to an administrator." + "\n\n"
		return message

	"""
	Method that prints the status of the alert delivery based on the response HTTP code.

	Parameters:
	self -- An instantiated object of the Telegram class.
	telegram_code -- HTTP code in response to the request made to Telegram.
	status_s -- Status of the Telk-Alert service.
	"""
	def getStatusByTelegramCode(self, telegram_code, status_s):
		if telegram_code == 200:
			self.logger.createLogAgent("Alert sent. Telk-Alert Service Status: " + str(status_s), 2)
			print("\nAlert sent. Telk-Alert Service Status: " + str(status_s))	
		if telegram_code == 400:
			self.logger.createLogAgent("Alert not sent. Bad request.", 4)
			print("\nAlert not sent. Bad request.")
		if telegram_code == 401:
			self.logger.createLogAgent("Alert not sent. Unauthorized.", 4)
			print("\nAlert not sent. Unauthorized.")
		if telegram_code == 404:
			self.logger.createLogAgent("Alert not sent. Not found.", 4)
			print("\nAlert not sent. Not found.")
			