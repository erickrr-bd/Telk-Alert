import pycurl
import time
from urllib.parse import urlencode

"""
Class that allows you to manage the sending of alerts through Telegram.
"""
class Telegram:

	"""
	Method that allows sending the alert to the Telegram channel.

	Parameters:
	self -- Instance object.
	telegram_chat_id -- Telegram channel identifier to which the letter will be sent.
	telegram_bot_token -- Token of the Telegram bot that is the administrator of the Telegram channel to which the alerts will be sent.
	message -- Message to be sent to the Telegram channel.
	"""
	def sendTelegramAgent(self, telegram_chat_id, telegram_bot_token, message):
		c = pycurl.Curl()
		url = 'https://api.telegram.org/bot' + str(telegram_bot_token) + '/sendMessage'
		c.setopt(c.URL, url)
		data = { 'chat_id' : telegram_chat_id, 'text' : message }
		pf = urlencode(data)
		c.setopt(c.POSTFIELDS, pf)
		c.perform()
		status_code = c.getinfo(pycurl.HTTP_CODE)
		c.close()
		return int(status_code)

	"""
	Method that allows generating the message that will be sent to the Telegram channel.

	Parameters:
	self -- Instance object.
	status_s -- Current status of the Telk-Alert service.
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