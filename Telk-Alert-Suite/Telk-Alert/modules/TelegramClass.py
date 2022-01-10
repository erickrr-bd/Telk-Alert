from sys import exit
from time import strftime
from pycurl import Curl, HTTP_CODE
from urllib.parse import urlencode
from elasticsearch_dsl import utils
from modules.UtilsClass import Utils

"""
Class that allows you to manage the sending of alerts through Telegram.
"""
class Telegram:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = Utils()

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
	Method that generates the header of the message that will be sent by telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.
	alert_rule_data -- Object with the data corresponding to the alert rule.

	Return: 
	header -- String corresponding to the header of the alert.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def getTelegramHeader(self, alert_rule_data):
		try:
			header = u'\u26A0\uFE0F' + " " + alert_rule_data['name_rule'] +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\U0001f6a6' +  " Alert level: " + alert_rule_data['alert_level'] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
			header += "At least " + str(alert_rule_data['num_events']) + " event(s) were found." + "\n\n"
			return header
		except KeyError as exception:
			self.utils.createTelkAlertLog("Error creating alert header. For more information, see the logs.", 3)
			self.utils.createTelkAlertLog("Key Error: " + str(exception), 3)
			exit(1)

	"""
	Method that generates the body of the message that will be sent by telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.
	hit -- Object that contains the data referring to the event found.

	Return: 
	message -- Message with the parsed data, which will be sent to Telegram.
	"""
	def getTelegramMessage(self, hit):
		message = "FOUND EVENT: " + '\n\n'
		for hits in hit:
			if not (type(hit[str(hits)]) is utils.AttrDict):
				message += u'\u2611\uFE0F' + " " + hits + " = " + str(hit[str(hits)]) + '\n'
			else:
				for hits_two in hit[str(hits)]:
					if not (type(hit[str(hits)][str(hits_two)]) is utils.AttrDict):
						message += u'\u2611\uFE0F' + " " + hits + "." + hits_two + " = " + str(hit[str(hits)][str(hits_two)]) + '\n'
					else:
						for hits_three in hit[str(hits)][str(hits_two)]:
							if not (type(hit[str(hits)][str(hits_two)][str(hits_three)]) is utils.AttrDict):
								message += u'\u2611\uFE0F' + " " + hits + "." + hits_two + "." + hits_three + " = " + str(hit[str(hits)][str(hits_two)][str(hits_three)]) + '\n'
							else:
								for hits_four in hit[str(hits)][str(hits_two)][str(hits_three)]:
									if not (type(hit[str(hits)][str(hits_two)][str(hits_three)][str(hits_four)]) is utils.AttrDict):
										message += u'\u2611\uFE0F' + " " + hits + "." + hits_two + "." + hits_three + "." + hits_four + " = " + str(hit[str(hits)][str(hits_two)][str(hits_three)]) + '\n'
		message += "\n\n"
		return message								

	"""
	Method that generates the message with the total of events found.

	Parameters:
	self -- An instantiated object of the Telegram class.
	total_events -- Total events found in the search.

	Return: 
	message_total_events -- Message with the total of events.
	"""
	def getTotalEventsFound(self, total_events):
		message_total_events = "TOTAL EVENTS FOUND: " + str(total_events)
		return message_total_events

	"""
	Method that prints the status of the alert delivery based on the response HTTP code.

	Parameters:
	self -- An instantiated object of the Telegram class.
	telegram_code -- HTTP code in response to the request made to Telegram.
	"""
	def getStatusByTelegramCode(self, telegram_code):
		if telegram_code == 200:
			self.utils.createTelkAlertLog("Telegram message sent.", 1)
		elif telegram_code == 400:
			self.utils.createTelkAlertLog("Telegram message not sent. Status: Bad request.", 3)
		elif telegram_code == 401:
			self.utils.createTelkAlertLog("Telegram message not sent. Status: Unauthorized.", 3)
		elif telegram_code == 404:
			self.utils.createTelkAlertLog("Telegram message not sent. Status: Not found.", 3)