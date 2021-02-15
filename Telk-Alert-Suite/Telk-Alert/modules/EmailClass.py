import smtplib
import sys
import email.message
sys.path.append('./modules')
from UtilsClass import Utils
from LoggerClass import Logger

class Email:

	utils = Utils()
	logger = Logger()

	def sendEmailAlert(self, email_from, email_from_pass, email_to, json_message, name_rule):
		message = self.utils.readTemplateEmail(json_message, name_rule)
		message_email = email.message.Message()
		message_email['Subject'] = 'Telk-Alert Notification Message'
		message_email['From'] = email_from
		message_email.add_header('Content-Type', 'text/html')
		message_email.set_payload(message)
		domain_email = email_from-split('@')[1]
		try:
			if domain_email == 'outlook.com':
				s = smtplib.SMTP('smtp-mail-outlook.com: 587')
			if domain_email == 'gmail.com':
				s = smtplib.SMTP('smtp-gmail.com: 587')
			s.starttls()
			s.login(message_email['From'], email_from_pass)
			s.sendmail(message_email['From'], email_to, message_email.as_string())
		except smtplib.SMTPAuthenticationError as exception:
			print("Authentication failed in SMTP. For more information see the application logs.")
			self.logger.createLogTelkAlert("Error: " + str(exception), 4)

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
	def getEmailHeader(self, rule_yaml, time_back):
		try:
			if rule_yaml['alert_level'] == "Low":
				print("Hola")
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