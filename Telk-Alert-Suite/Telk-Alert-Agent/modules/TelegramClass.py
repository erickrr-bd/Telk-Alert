from time import strftime
from pycurl import Curl, HTTP_CODE
from urllib.parse import urlencode
from modules.UtilsClass import Utils

"""
Class that allows you to manage the sending of alerts through Telegram.
"""
class Telegram:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Constructor for the Telegram class.

	Parameters:
	self -- An instantiated object of the Telegram class.
	"""
	def __init__(self):
		self.utils = Utils()

	"""
	Method that sends the alert to the telegram channel.

	Parameters:
	self -- An instantiated object of the Telegram class.
	telegram_chat_id -- Telegram channel identifier to which the letter will be sent.
	telegram_bot_token -- Token of the Telegram bot that is the administrator of the Telegram channel to which the alerts will be sent.
	message -- Message to be sent to the Telegram channel.
	"""
	def sendTelegramAlert(self, telegram_chat_id, telegram_bot_token, message):
		if len(message) > 4096:
			message = "The size of the message in Telegram (4096) has been exceeded. Overall size: " + str(len(message))
		c = Curl()
		url = 'https://api.telegram.org/bot' + str(telegram_bot_token) + '/sendMessage'
		c.setopt(c.URL, url)
		data = { 'chat_id' : telegram_chat_id, 'text' : message }
		pf = urlencode(data)
		c.setopt(c.POSTFIELDS, pf)
		c.perform_rs()
		status_code = c.getinfo(HTTP_CODE)
		c.close()
		self.getStatusByTelegramCode(status_code)

	"""
	Method that generates the message that will be sent to Telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.
	status_service_telk_alert -- Current status of the Telk-Alert service.

	Return:
	message -- Message that will be sent via Telegram.
	"""
	def getTelegramMessage(self, status_service_telk_alert):
		message = "" + u'\u26A0\uFE0F' + "Telk-Alert Service " + u'\u26A0\uFE0F' + '\n\n' + u'\u23F0' + "Service Status Validation Time: " + strftime("%c") + "\n\n\n"
		if status_service_telk_alert == "Not running":
			message += "Service Telk-Alert Status: " + u'\U0001f534' + "\n\n"
		elif status_service_telk_alert == "Running":
			message += "Service Telk-Alert Status: " + u'\U0001f7e2' + "\n\n"
		message += "" + u'\U0001f4cb' + " " + "Note 1: The green circle indicates that the Telk-Alert service is working without problems." + "\n\n"
		message += "" + u'\U0001f4cb' + " " + "Note 2: The red circle indicates that the Telk-Alert service is not working. Report to an administrator." + "\n\n"
		return message

	"""
	Method that prints the status of the alert delivery based on the response HTTP code.

	Parameters:
	self -- An instantiated object of the Telegram class.
	telegram_code -- HTTP code in response to the request made to Telegram.
	"""
	def getStatusByTelegramCode(self, telegram_code):
		if telegram_code == 200:
			self.utils.createTelkAlertAgentLog("Telegram message sent.", 1)
		elif telegram_code == 400:
			self.utils.createTelkAlertAgentLog("Telegram message not sent. Status: Bad request.", 3)
		elif telegram_code == 401:
			self.utils.createTelkAlertAgentLog("Telegram message not sent. Status: Unauthorized.", 3)
		elif telegram_code == 404:
			self.utils.createTelkAlertAgentLog("Telegram message not sent. Status: Not found.", 3)