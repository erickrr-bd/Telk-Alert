import sys
import time
import pycurl
from datetime import datetime
from urllib.parse import urlencode
from elasticsearch_dsl import utils
from modules.LoggerClass import Logger
from modules.UtilsClass import Utils

"""
Class that allows you to manage the sending of alerts through Telegram.
"""
class Telegram:

	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Method that allows sending the alert to the Telegram channel.

	Parameters:
	self -- Instance object.
	telegram_chat_id -- Telegram channel identifier to which the letter will be sent.
	telegram_bot_token -- Token of the Telegram bot that is the administrator of the Telegram channel to which the alerts will be sent.
	message -- Message to be sent to the Telegram channel.

	Return:
	HTTP code of the request to Telegram.
	"""
	def sendTelegramAlert(self, telegram_chat_id, telegram_bot_token, message):
		if len(message) > 4096:
			message = "The size of the message in Telegram (4096) has been exceeded. Overall size: " + str(len(message))
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
	Method that allows creating the header of the alert to be sent to Telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.
	rule_yaml -- List with all the data of the alert rule.
	time_back -- Backward time in milliseconds of the alert rule.

	Return: 
	header -- Alert header in string.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def getTelegramHeader(self, rule_yaml, time_back):
		try:
			header = u'\u26A0\uFE0F' + " " + rule_yaml['name_rule'] +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\U0001f6a6' +  " Alert level: " + rule_yaml['alert_level'] + "\n\n" +  u'\u23F0' + " Alert sent: " + time.strftime("%c") + "\n\n\n"
			header += "At least " + str(rule_yaml['num_events']) + " event(s) ocurred between " + self.utils.convertMillisecondsToDate(self.utils.convertDateToMilliseconds(datetime.now()) - time_back) + " and " + self.utils.convertMillisecondsToDate(self.utils.convertDateToMilliseconds(datetime.now())) + "\n\n\n"
			return header
		except KeyError as exception:
			self.logger.createLogTelkAlert("Key Error: " + str(exception), 4)
			print("Key Error: " + str(exception))
			sys.exit(1)

	"""
	Method that allows generating the message that will be sent to the Telegram channel.

	Parameters:
	self -- An instantiated object of the Telegram class.
	hit -- Object that contains all the information found in the ElasticSearch search.

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
	name_rule -- Name of the alert rule.
	"""
	def getStatusByTelegramCode(self, telegram_code, name_rule):
		if telegram_code == 200:
			print("\nAlert sent to Telegram. Name rule: " + name_rule)
			self.logger.createLogTelkAlert("Telegram alert sent. Name rule: " + name_rule, 2)
		if telegram_code == 400:
			print("Telegram alert not sent. Bad request. Name rule: " + name_rule)
			self.logger.createLogTelkAlert("Telegram alert not sent. Bad request. Name rule: " + name_rule, 4)
		if telegram_code == 401:
			print("Telegram alert not sent. Unauthorized. Name rule: " + name_rule)
			self.logger.createLogTelkAlert("Telegram alert not sent. Unauthorized. Name rule: " + name_rule, 4)
		if telegram_code == 404:
			print("Telegram alert not sent. Not found. Name rule: " + name_rule)
			self.logger.createLogTelkAlert("Telegram alert not sent. Not found. Name rule: " + name_rule, 4)