import sys
import smtplib
import email.message
from datetime import datetime
from elasticsearch_dsl import utils
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger

"""
Class that allows to manage the sending of alerts by email.
"""
class Email:
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores an object of type Logger.
	"""
	logger = None

	"""
	Constructor for the Email class.

	Parameters:
	self -- An instantiated object of the Email class.
	"""
	def __init__(self):
		self.logger = Logger()
		self.utils = Utils()

	"""
	Method that sends the alert to the destination emails.

	Parameters:
	self -- An instantiated object of the Email class.
	email_from -- Issuing email address.
	email_from_pass -- Password for the issuing email address.
	email_to -- List containing the email addresses that will receive the alert.
	json_message -- String that contains the data of the search result in ElasticSearch.
	name_rule -- Name of the alert rule.

	Return:
	response -- Response of sending the email to the recipients.

	Exceptions:
	smtplib.SMTPAuthenticationError: SMTP authentication went wrong. 
	"""
	def sendEmailAlert(self, email_from, email_from_pass, email_to, json_message, name_rule):
		message_aux = self.utils.readTemplateEmail(json_message, name_rule)
		message_email = email.message.Message()
		message_email['Subject'] = 'Telk-Alert Notification Message'
		message_email['From'] = email_from
		message_email.add_header('Content-Type', 'text/html')
		message_email.set_payload(message_aux)
		try:
			domain_email = email_from.split('@')[1]
			if domain_email == 'outlook.com':
				s = smtplib.SMTP('smtp-mail-outlook.com: 587')
			if domain_email == 'gmail.com':
				s = smtplib.SMTP('smtp.gmail.com: 587')
			s.starttls()
			s.login(message_email['From'], email_from_pass)
			response = s.sendmail(message_email['From'], email_to, message_email.as_string())
			return response
		except smtplib.SMTPAuthenticationError as exception:
			self.logger.createLogTelkAlert(str(exception), 4)
			print("\nAuthentication failed in SMTP. For more information see the application logs.")
		except IndexError as exception:
			self.logger.createLogTelkAlert("Index Error: " + str(exception), 4)
			print("\nIndex Error: " + str(exception))

	"""
	Method that generates the header of the message that will be sent by email.

	Parameters:
	self -- An instantiated object of the Email class.
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
				level = "<b>Alert Level</b>: <span style='color: green'><b>" + rule_yaml['alert_level'] + "</b></span><br/>"
			if rule_yaml['alert_level'] == "Medium":
				level = "<b>Alert Level</b>: <span style='color: yellow'><b>" + rule_yaml['alert_level'] + "</b></span><br/>"
			if rule_yaml['alert_level'] == "High":
				level = "<b>Alert Level</b>: <span style='color: red'><b>" + rule_yaml['alert_level'] + "</b></span><br/>"
			header = level + "At least " + str(rule_yaml['num_events']) + " event(s) ocurred between " + self.utils.convertMillisecondsToDate(self.utils.convertDateToMilliseconds(datetime.now()) - time_back) + " and " + self.utils.convertMillisecondsToDate(self.utils.convertDateToMilliseconds(datetime.now())) + "\n\n\n"
			return header
		except KeyError as exception:
			self.logger.createLogTelkAlert("\nKey Error: " + str(exception), 4)
			print("Key Error: " + str(exception))
			sys.exit(1)

	"""
	Method that generates the body of the message that will be sent by email.

	Parameters:
	self -- An instantiated object of the Email class.
	hit -- Object that contains all the information found in the ElasticSearch search.

	Return: 
	message -- Message with the parsed data, which will be sent to email.
	"""
	def getEmailMessage(self, hit):
		message = "<br/><br/><b>FOUND EVENT: </b><br/><br/><ul>"
		for hits in hit:
			if not (type(hit[str(hits)]) is utils.AttrDict):
				message += "<li><b>" + hits + "</b> = " + str(hit[str(hits)]) + "</li>"
			else:
				for hits_two in hit[str(hits)]:
					if not (type(hit[str(hits)][str(hits_two)]) is utils.AttrDict):
						message += "<li><b>" + hits + "." + hits_two + "</b> = " + str(hit[str(hits)][str(hits_two)]) + "</li>"
					else:
						for hits_three in hit[str(hits)][str(hits_two)]:
							if not (type(hit[str(hits)][str(hits_two)][str(hits_three)]) is utils.AttrDict):
								message += "<li><b>" + hits + "." + hits_two + "." + hits_three + "</b> = " + str(hit[str(hits)][str(hits_two)][str(hits_three)]) + "</li>"
							else:
								for hits_four in hit[str(hits)][str(hits_two)][str(hits_three)]:
									if not (type(hit[str(hits)][str(hits_two)][str(hits_three)][str(hits_four)]) is utils.AttrDict):
										message += "<li><b>" + hits + "." + hits_two + "." + hits_three + "." + hits_four + "</b> = " + str(hit[str(hits)][str(hits_two)][str(hits_three)]) + "</li>"
		message += "</ul><br/><br/>"
		return message								

	"""
	Method that generates the message with the total of events found.

	Parameters:
	self -- An instantiated object of the Email class.
	total_events -- Total events found in the search.

	Return: 
	message_total_events -- Message with the total of events.
	"""
	def getTotalEventsFound(self, total_events):
		message_total_events = "<b>TOTAL EVENTS FOUND: </b>" + str(total_events)
		return message_total_events

	"""
	Method that obtains the status of the sending of email alerts and displays it on the screen.

	Parameters:
	self -- An instantiated object of the Email class.
	response -- Response of sending alerts by email.
	email_to -- List with the email addresses to which the alerts will be sent.
	"""
	def getStatusEmailAlert(self, response, email_to):
		if len(response) == 0:
			self.logger.createLogTelkAlert("Alert sent to email(s): " + " ".join(email_to), 2)
			print("\nAlert sent to email(s): " + " ".join(email_to))
		else:
			self.logger.createLogTelkAlert(str(response), 3)
			print("\n" + str(response))
			