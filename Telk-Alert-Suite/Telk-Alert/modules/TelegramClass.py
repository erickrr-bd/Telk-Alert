import sys
import time
import pycurl
from datetime import datetime
from urllib.parse import urlencode
sys.path.append('./modules')
from UtilsClass import Utils
from LoggerClass import Logger

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
	self -- Instance object.
	hit -- Current status of the Telk-Alert service.

	Return: 
	message -- 
	"""
	def getTelegramMessage(self, hit):
		message = "FOUND EVENT: " + '\n\n'
		for hits in hit:
			if (type(hit[str(hits)]) is str) or (type(hit[str(hits)]) is int):
				message += u'\u2611\uFE0F' + " " + hits + " = " + str(hit[str(hits)]) + '\n'
			else:
				for hits_two in hit[str(hits)]:
					if (type(hit[str(hits)][str(hits_two)]) is str) or (type(hit[str(hits)][str(hits_two)]) is int):
						message += u'\u2611\uFE0F' + " " + hits + "." + hits_two + " = " + str(hit[str(hits)][str(hits_two)]) + '\n'
					else:
						for hits_three in hit[str(hits)[str(hits_two)]]:
							if (type(hit[str(hits)][str(hits_two)][str(hits_three)]) is str) or (type(hit[str(hits)][str(hits_two)][str(hits_three)]) is int):
								message += u'\u2611\uFE0F' + " " + hits + "." + hits_two + "." + hits_three + " = " + str(hit[str(hits)][str(hits_two)][str(hits_three)]) + '\n'
		message += "\n\n"
		return message