import yaml
import sys
import glob
import os
sys.path.append('./modules')
from UtilsClass import Utils
from LoggerClass import Logger

class Rules:

	utils = Utils()
	logger = Logger()

	options_level_alert = [("Low", "Low level alert", 1),
						  ("Medium", "Medium level alert", 0),
						  ("High", "High level alert", 0)]

	options_unit_time = [("minutes", "Time expressed in minutes", 1),
						("hours", "Time expressed in hours", 0),
						("days", "Time expressed in days", 0)]

	options_send_alert = [("telegram", "The alert will be sent via Telegram", 0),
						 ("email", "The alert will be sent via email", 0)]


	folder_rules = ""

	def __init__(self):
		self.folder_rules = self.utils.readFileYaml(self.utils.getPathTalert('conf') + '/es_conf.yaml')['rules_folder']

	"""
	Method that allows the user to request the data to create a new alert rule.

	Parameters:
	self -- Instance object.
	form_dialog -- A FormClass class object.
	"""
	def createNewRule(self, form_dialog):
		options_type_alert = [("Frequency", "Make the searches in the index periodically", 1)]

		options_filter_alert = [("query string", "Perform the search using the Query String of ElasticSearch", 1)]

		data_rule = []
		name_rule = form_dialog.getDataNameFolderOrFile("Enter the name of the alert rule:", "rule1")
		data_rule.append(name_rule)
		level_alert = form_dialog.getDataRadioList("Select a option:", self.options_level_alert, "Alert Rule Level")
		data_rule.append(level_alert)
		index_name = form_dialog.getDataInputText("Enter the index pattern where the searches will be made:", "winlogbeat-*")
		data_rule.append(index_name)
		type_rule = form_dialog.getDataRadioList("Select a option:", options_type_alert, "Alert Rule Type")
		data_rule.append(type_rule)
		if type_rule == "Frequency":
			num_events = form_dialog.getDataNumber("Enter the number of events found in the rule to send the alert to:", "1")
			unit_time_search = form_dialog.getDataRadioList("Select a option:", self.options_unit_time, "Search Time Unit")
			num_time_search = form_dialog.getDataNumber("Enter the total amount in " + str(unit_time_search) + " in which you want the search to be repeated:", "2")
			unit_time_back = form_dialog.getDataRadioList("Select a option:", self.options_unit_time, "Search Time Unit")
			num_time_back = form_dialog.getDataNumber("Enter the total amount in " + str(unit_time_search) + " of time back in which you want to perform the search:", "2")
			data_rule.append(num_events)
			data_rule.append(unit_time_search)
			data_rule.append(num_time_search)
			data_rule.append(unit_time_back)
			data_rule.append(num_time_back)
		filter_type = form_dialog.getDataRadioList("Select a option:", options_filter_alert, "Alert Rule Filter:")
		data_rule.append(filter_type)
		if filter_type == "query string":
			query_string = form_dialog.getDataInputText("Enter the query string:", "event.code : 4120")
			data_rule.append(query_string)
			use_restriction_fields = form_dialog.getDataYesOrNo("Do you want your search results to be restricted to certain fields?", "Restriction By Fields")
			if use_restriction_fields == "ok":
				data_rule.append(True)
				number_fields = form_dialog.getDataNumber("Enter how many fields you want to enter for the restriction:", "2")
				list_fields_add = form_dialog.getFieldsAdd(number_fields)
				es_fields = form_dialog.getFields(list_fields_add, "Restriction By Fields", "Enter the name of the field or fields:")
				data_rule.append(es_fields)
			else:
				data_rule.append(False)
		restrict_hostname = form_dialog.getDataYesOrNo("Do you want the sending of the alert to be restricted to a certain number of events per hostname?", "Restriction By Hostname")
		if restrict_hostname == "ok":
			number_events_hostname = form_dialog.getDataNumber("Enter the total number of events per hostname to which the alert will be sent:", "3")
			data_rule.append(True)
			data_rule.append(number_events_hostname)
		else:
			data_rule.append(False)
		opt_alert_send = form_dialog.getDataCheckList("Select one or more options:", self.options_send_alert, "Alert Sending Platforms")
		bandera_telegram = 0
		bandera_email = 0
		for opt_alert in opt_alert_send:
			if opt_alert == "telegram":
				bandera_telegram = 1
			if opt_alert == "email":
				bandera_email = 1
		if bandera_telegram == 1:
			telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
			telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
			data_rule.append(telegram_bot_token)
			data_rule.append(telegram_chat_id)
		if bandera_email == 1:
			email_from = form_dialog.getDataEmail("Enter the email address from which the alerts will be sent (gmail or outlook):", "usuario@gmail.com")
			email_from_password = self.utils.encryptAES(form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"))
			number_email_to = form_dialog.getDataNumber("Enter the total number of email addresses to which the alert will be sent:", "3")
			list_email_to_add = form_dialog.getEmailAdd(number_email_to)
			list_email_to = form_dialog.getEmailsTo(list_email_to_add, "Destination Email Addresses:", "Enter email addresses:")
			data_rule.append(email_from)
			data_rule.append(email_from_password)
			data_rule.append(list_email_to)
		self.createRuleYaml(data_rule, bandera_telegram, bandera_email)
		if(not os.path.exists(self.utils.getPathTalert(self.folder_rules) + '/' + name_rule + '.yaml')):
			form_dialog.d.msgbox("\nError creating alert rule", 7, 50, title = "Error message")
		else:
			form_dialog.d.msgbox("\nAlert rule created", 7, 50, title = "Notification message")
		form_dialog.mainMenu()

	def modifyAlertRule(self, form_dialog, name_alert_rule):
		print("Hola")


	"""
	Method that allows creating the alert rule file with extension .yaml based on what was entered.

	Parameters:
	self -- Instance object.
	data_rule -- List with all the data entered for the alert rule.
	bandera_telegram -- Flag that lets you know if the alert will be sent by telegram or not.
	bandera_email -- Flag that lets you know if the alert will be sent by email or not.

	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” 
	or “disk full” (not for illegal argument types or other incidental errors).
	"""
	def createRuleYaml(self, data_rule, bandera_telegram, bandera_email):
		
		d_rule = {'name_rule' : str(data_rule[0]),
		'alert_level' : str(data_rule[1]),
		'type_alert' : str(data_rule[3]),
		'index_name' : str(data_rule[2]),
		'num_events' : int(data_rule[4]),
		'time_search' : { str(data_rule[5]) : int(data_rule[6]) },
		'time_back' : { str(data_rule[7]) : int(data_rule[8]) },
		'filter_search' : [{ str(data_rule[9]) : { 'query' : str(data_rule[10])}}],
		'use_restriction_fields' : data_rule[11]
		}

		if data_rule[11] == True:
			fields_json = { 'fields' : data_rule[12] }
			d_rule.update(fields_json)
			restrict_by_host = data_rule[13]
			if restrict_by_host == True:
				restriction_json = { 'number_events_host' : int(data_rule[14]) }
				d_rule.update(restriction_json)
				last_index = 14
			else:
				last_index = 13
		else:
			restrict_by_host = data_rule[12]
			if restrict_by_host == True:
				number_events_host = { 'number_events_host' : int(data_rule[13]) }
				d_rule.update(number_events_host)
				last_index = 13
			else:
				last_index = 12
		restrict_host_json = { 'restrict_by_host' : restrict_by_host }
		if bandera_telegram == 1 and bandera_email == 0:
			alert_json = { 'alert' : ['telegram'] }
			telegram_json = { 'telegram_bot_token' : data_rule[last_index + 1].decode('utf-8'), 'telegram_chat_id' : data_rule[last_index + 2].decode('utf-8') }
			d_rule.append(telegram_json)
			d_rule.append(alert_json)
		if bandera_email == 1 and bandera_telegram == 0:
			alert_json = { 'alert' : ['email'] }
			email_json = { 'email_from' : str(data_rule[last_index + 1]), 'email_from_password' : data_rule[last_index + 2].decode('utf-8'), 'email_to' : data_rule[last_index + 3] }
			d_rule.update(email_json)
			d_rule.update(alert_json)
		if bandera_telegram == 1 and bandera_email == 1:
			alert_json = { 'alert' : ['telegram', 'email'] }
			telegram_json = { 'telegram_bot_token' : data_rule[last_index + 1].decode('utf-8'), 'telegram_chat_id' : data_rule[last_index + 2].decode('utf-8') }
			email_json = { 'email_from' : str(data_rule[last_index + 3]), 'email_from_password' : data_rule[last_index + 4].decode('utf-8'), 'email_to' : data_rule[last_index + 5] }
			d_rule.update(telegram_json)
			d_rule.update(email_json)
			d_rule.update(alert_json)
		try:
			with open(self.utils.getPathTalert(self.folder_rules) + '/' + str(data_rule[0]) + '.yaml', 'w') as rule_file:
				yaml.dump(d_rule, rule_file, default_flow_style = False)
		except OSError as exception:
			logger.createLogTool('Error: ' + str(exception), 4)

	"""
	Method that allows to create an interface with the list of alert rules and thus be able to choose the one to be modified.

	Parameters:
	self -- Instance object.
	form_dialog -- A FormClass class object.
	"""
	def getUpdateAlertRules(self, form_dialog):
		list_alert_rules = self.getAllAlertRules(self.utils.getPathTalert(self.folder_rules))
		if len(list_alert_rules) == 0:
			form_dialog.d.msgbox("There are no alert rules in the directory", 5, 50, title = "Error message")
		else:
			options_alert_rules = []
			for alert_rule in list_alert_rules:
				options_alert_rules.append((alert_rule, "", False))
			rule_to_modify = form_dialog.getDataRadioList("Select a option:", options_alert_rules, "Alert Rules List")
			self.modifyAlertRule(form_dialog, rule_to_modify)

	"""
	Method that allows to obtain all the alert rules saved in a directory.

	Parameters:
	self -- Instance object.
	path_folder_rules -- Directory where all alert rules are stored.
	"""
	def getAllAlertRules(self, path_folder_rules):
		list_alert_rules = [os.path.basename(x) for x in glob.glob(path_folder_rules + '/*.yaml')]
		return list_alert_rules




 