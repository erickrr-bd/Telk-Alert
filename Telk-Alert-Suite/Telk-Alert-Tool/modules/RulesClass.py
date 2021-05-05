import os
import yaml
import glob
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger

"""
Class that allows managing alert rules.
"""
class Rules:
	"""
	Property that contains the name of the folder where the alert rules are saved.
	"""
	folder_rules = None

	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Property that contains the options for the alert rule level.
	"""
	options_level_alert = [["Low", "Low level alert", 1],
						  ["Medium", "Medium level alert", 0],
						  ["High", "High level alert", 0]]

	"""
	Property that contains the options for the unit of time.
	"""
	options_unit_time = [["minutes", "Time expressed in minutes", 1],
						["hours", "Time expressed in hours", 0],
						["days", "Time expressed in days", 0]]

	"""
	Property that contains the options for the alert sending platforms.
	"""
	options_send_alert = [("telegram", "The alert will be sent via Telegram", 0),
						 ("email", "The alert will be sent via email", 0)]

	"""
	Property that stores the options for the types of sending alerts.
	"""
	options_type_alert_send = [["only", "A single alert with the total of events found", 1],
						 ["multiple", "An alert for each event found", 0]]

	"""
	Constructor for the Rules class.

	Parameters:
	self -- An instantiated object of the Rules class.
	"""
	def __init__(self):
		self.folder_rules = self.utils.readFileYaml(self.utils.getPathTalert('conf') + '/es_conf.yaml')['rules_folder']

	"""
	Method that requests the data for the creation of an alert rule.

	Parameters:
	self -- An instantiated object of the Rules class.
	form_dialog -- A FormDialogs class object.
	"""
	def createNewRule(self, form_dialog):
		options_type_alert = [("Frequency", "Make the searches in the index periodically", 1)]

		options_filter_alert = [("query_string", "Perform the search using the Query String of ElasticSearch", 1)]

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
			unit_time_back = form_dialog.getDataRadioList("Select a option:", self.options_unit_time, "Time Back Unit")
			num_time_back = form_dialog.getDataNumber("Enter the total amount in " + str(unit_time_back) + " of time back in which you want to perform the search:", "2")
			data_rule.append(num_events)
			data_rule.append(unit_time_search)
			data_rule.append(num_time_search)
			data_rule.append(unit_time_back)
			data_rule.append(num_time_back)
		filter_type = form_dialog.getDataRadioList("Select a option:", options_filter_alert, "Alert Rule Filter:")
		data_rule.append(filter_type)
		if filter_type == "query_string":
			query_string = form_dialog.getDataInputText("Enter the query string:", "event.code : 4120")
			data_rule.append(query_string)
			type_alert_send = form_dialog.getDataRadioList("Select a option:", self.options_type_alert_send, "Alert Sending Type")
			data_rule.append(type_alert_send)
			use_restriction_fields = form_dialog.getDataYesOrNo("\nDo you want your search results to be restricted to certain fields?", "Restriction By Fields")
			if use_restriction_fields == "ok":
				data_rule.append(True)
				number_fields = form_dialog.getDataNumber("Enter how many fields you want to enter for the restriction:", "2")
				list_fields_add = form_dialog.getFieldsAdd(number_fields)
				es_fields = form_dialog.getFields(list_fields_add, "Restriction By Fields", "Enter the name of the field or fields:")
				data_rule.append(es_fields)
			else:
				data_rule.append(False)
		restrict_hostname = form_dialog.getDataYesOrNo("\nDo you want the sending of the alert to be restricted to a certain number of events per hostname?", "Restriction By Hostname")
		if restrict_hostname == "ok":
			number_events_hostname = form_dialog.getDataNumber("Enter the total number of events per hostname to which the alert will be sent:", "3")
			data_rule.append(True)
			data_rule.append(number_events_hostname)
			field_hostname = form_dialog.getDataInputText("Enter the name of the field that contains the hostname:", "host.hostname")
			data_rule.append(field_hostname)
		else:
			data_rule.append(False)
		opt_alert_send = form_dialog.getDataCheckList("Select one or more options:", self.options_send_alert, "Alert Sending Platforms")
		flag_telegram = 0
		flag_email = 0
		for opt_alert in opt_alert_send:
			if opt_alert == "telegram":
				flag_telegram = 1
			if opt_alert == "email":
				flag_email = 1
		if flag_telegram == 1:
			telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
			telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
			data_rule.append(telegram_bot_token)
			data_rule.append(telegram_chat_id)
		if flag_email == 1:
			email_from = form_dialog.getDataEmail("Enter the email address from which the alerts will be sent (gmail or outlook):", "usuario@gmail.com")
			email_from_password = self.utils.encryptAES(form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"))
			number_email_to = form_dialog.getDataNumber("Enter the total number of email addresses to which the alert will be sent:", "3")
			list_email_to_add = form_dialog.getEmailAdd(number_email_to)
			list_email_to = form_dialog.getEmailsTo(list_email_to_add, "Destination Email Addresses:", "Enter email addresses:")
			data_rule.append(email_from)
			data_rule.append(email_from_password)
			data_rule.append(list_email_to)
		self.createRuleYaml(data_rule, flag_telegram, flag_email)
		if(not os.path.exists(self.utils.getPathTalert(self.folder_rules) + '/' + name_rule + '.yaml')):
			form_dialog.d.msgbox("\nError creating alert rule. For more details, see the logs.", 7, 50, title = "Error message")
		else:
			self.logger.createLogTool("Alert rule created: " + name_rule, 2)
			form_dialog.d.msgbox("\nAlert rule created: " + name_rule, 7, 50, title = "Notification message")	
		form_dialog.mainMenu()

	"""
	Method that modifies one or more fields of a specific alert rule.

	Parameters:
	self -- An instantiated object of the Rules class.
	form_dialog -- A FormDialogs class object.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def modifyAlertRule(self, form_dialog, name_alert_rule):
		options_fields_update = [("Name", "Alert rule name", 0),
								("Level", "Alert rule level", 0),
								("Index", "Index name in ElastcSearch", 0),
								("Number of Events", "Number of events found to which the alert is sent", 0),
								("Time Search", "Time in which the event search will be repeated", 0),
								("Time Back", "Time back in which the search will be made", 0),
								("Query String", "Query string for event search", 0),
								("Restriction Fields", "The search result only returns certain fields", 0),
								("Restriction Hostname", "Sending of the alert is retracted by hostname", 0),
								("Shipping Type", "How the alert will be sent", 0),
								("Sending Alert", "Alerts sending platforms", 0)]

		options_rest_field_false = [("Enable", "Enable restriction by fields", 0)]

		options_rest_field_true = [("To Disable", "Disable restriction by fields", 0),
								  ("Modify Data", "Modify existing data", 0)]

		options_rest_field_modify = [("Add New Field(s)", "Add one or more new fields", 0),
									("Modify Field(s)", "Modify Existing Fields", 0),
									("Remove Field(s)", "Remove Existing Fields", 0)]

		options_rest_host_false = [("Enable", "Enable restriction by host", 0)]

		options_rest_host_true = [("To Disable", "Disable restriction by host", 0),
								 ("Modify Data", "Modify existing data", 0)]

		options_rest_host_modify = [("Number of Events", "Number of events per host", 0)]

		options_telegram_true = [("To Disable", "Disable sending by Telegram", 0),
								("Modify Data", "Modify existing data", 0)]

		options_telegram_false = [("Enable", "Enable sending by Telegram", 0)]

		options_telegram_modify = [("Bot Token", "Telegram bot token", 0),
								  ("Chat ID", "Telegram channel identifier", 0)]

		options_email_true = [("To Disable", "Disable sending by Email", 0),
							 ("Modify Data", "Modify existing data", 0)]

		options_email_false = [("Enable", "Enable sending by Email", 0)]

		options_email_modify = [("Email From", "Sender email address", 0),
							   ("Email Password", "Sender email password", 0),
							   ("Email To", "Recipient email addresses", 0)]

		options_email_to = [("Add New Email(s)", "Add one or more new emails", 0),
						   ("Modify Email(s)", "Modify Existing Emails", 0),
						   ("Remove Email(s)", "Remove Existing Emails", 0)]
		flag_name = 0
		flag_level = 0
		flag_index = 0
		flag_number_events = 0
		flag_time_search = 0
		flag_time_back = 0
		flag_query_string = 0
		flag_restriction_fields = 0
		flag_restriction_hostname = 0
		flag_type_alert = 0
		flag_sending_alert = 0
		list_fields_update = form_dialog.getDataCheckList("Select one option or more:", options_fields_update, "Alert Rule Fields")
		for field_update in list_fields_update:
			if field_update == "Name":
				flag_name = 1
			if field_update == "Level":
				flag_level = 1
			if field_update == "Index":
				flag_index = 1
			if field_update == "Number of Events":
				flag_number_events = 1
			if field_update == "Time Search":
				flag_time_search = 1
			if field_update == "Time Back":
				flag_time_back = 1
			if field_update == "Query String":
				flag_query_string = 1
			if field_update == "Restriction Fields":
				flag_restriction_fields = 1
			if field_update == "Restriction Hostname":
				flag_restriction_hostname = 1
			if field_update == "Shipping Type":
				flag_type_alert = 1
			if field_update == "Sending Alert":
				flag_sending_alert = 1
		try:
			with open(self.utils.getPathTalert(self.folder_rules) + '/' + name_alert_rule, "rU") as file_rule:
				data_rule = yaml.safe_load(file_rule)
			hash_origen = self.utils.getSha256File(self.utils.getPathTalert(self.folder_rules) + '/' + name_alert_rule)
			name_rule_actual = data_rule['name_rule']
			if flag_name == 1:
				name_rule = form_dialog.getDataNameFolderOrFile("Enter the name of the alert rule:", str(data_rule['name_rule']))
				data_rule['name_rule'] = str(name_rule)
			if flag_level == 1:
				for opt_level in self.options_level_alert:
					if opt_level[0] == data_rule['alert_level']:
						opt_level[2] = 1
					else:
						opt_level[2] = 0
				level_alert = form_dialog.getDataRadioList("Select a option:", self.options_level_alert, "Alert Rule Level")
				data_rule['alert_level'] = str(level_alert)
			if flag_index == 1:
				index_name = form_dialog.getDataInputText("Enter the index pattern where the searches will be made:", str(data_rule['index_name']))
				data_rule['index_name'] = str(index_name)
			if flag_number_events == 1:
				num_events = form_dialog.getDataNumber("Enter the number of events found in the rule to send the alert to:", str(data_rule['num_events']))
				data_rule['num_events'] = int(num_events)
			if flag_time_search == 1:
				for unit_time in data_rule['time_search']:
					num_time_search_actual = unit_time
				for opt_unit_time in self.options_unit_time:
					if opt_unit_time[0] == num_time_search_actual:
						opt_unit_time[2] = 1
					else:
						opt_unit_time[2] = 0
				unit_time_search = form_dialog.getDataRadioList("Select a option:", self.options_unit_time, "Search Time Unit")
				num_time_search = form_dialog.getDataNumber("Enter the total amount in " + str(unit_time_search) + " in which you want the search to be repeated:", str(data_rule['time_search'][num_time_search_actual]))
				data_rule['time_search'] = { str(unit_time_search) : int(num_time_search) }
			if flag_time_back == 1:
				for unit_time in data_rule['time_back']:
					num_time_back_actual = unit_time
				for opt_unit_time in self.options_unit_time:
					if opt_unit_time[0] == num_time_back_actual:
						opt_unit_time[2] = 1
					else:
						opt_unit_time[2] = 0
				unit_time_back = form_dialog.getDataRadioList("Select a option:", self.options_unit_time, "Search Time Unit")
				num_time_back = form_dialog.getDataNumber("Enter the total amount in " + str(unit_time_back) + " of time back in which you want to perform the search:", str(data_rule['time_back'][num_time_back_actual]))
				data_rule['time_back'] = { str(unit_time_back) : int(num_time_back) }
			if flag_query_string == 1:
				query_string = form_dialog.getDataInputText("Enter the query string:", str(data_rule['filter_search'][0]['query_string']['query']))
				data_rule['filter_search'] = [ { 'query_string' : { 'query' : str(query_string) } } ]
			if flag_restriction_fields == 1:
				if data_rule['use_restriction_fields'] == False:
					opt_rest_field_false = form_dialog.getDataRadioList("Select a option:", options_rest_field_false, "Field Restriction")
					if opt_rest_field_false == "Enable":
						number_fields = form_dialog.getDataNumber("Enter how many fields you want to enter for the restriction:", "2")
						list_fields_add = form_dialog.getFieldsAdd(number_fields)
						es_fields = form_dialog.getFields(list_fields_add, "Restriction By Fields", "Enter the name of the field or fields:")
						data_rule['use_restriction_fields'] = True
						restriction_fields_json = { 'fields' : es_fields }
						data_rule.update(restriction_fields_json)
				else:
					list_fields_actual = data_rule['fields']
					opt_rest_field_true = form_dialog.getDataRadioList("Select a option:", options_rest_field_true, "Field Restriction")
					if opt_rest_field_true == "To Disable":
						data_rule['use_restriction_fields'] = False
						del(data_rule['fields'])
					if opt_rest_field_true == "Modify Data":
						opt_rest_field_modify = form_dialog.getDataRadioList("Select a option:", options_rest_field_modify, "Field Restriction")
						if opt_rest_field_modify == "Add New Field(s)":
							number_fields = form_dialog.getDataNumber("Enter how many fields you want to enter for the restriction:", "2")
							list_fields_add = form_dialog.getFieldsAdd(number_fields)
							es_fields = form_dialog.getFields(list_fields_add, "Restriction By Fields", "Enter the name of the field or fields:")
							for field in es_fields:
								list_fields_actual.append(field)
							data_rule['fields'] = list_fields_actual
						if opt_rest_field_modify == "Modify Field(s)":
							list_fields_update = form_dialog.getFields(list_fields_actual, "Modify Existing Field(s)", "Modify field name(s):")
							del(data_rule['fields'])
							data_rule['fields'] = list_fields_update
						if opt_rest_field_modify == "Remove Field(s)":
							options_remove_fields = []
							for field in list_fields_actual:
								options_remove_fields.append((field, "", 0))
							opt_remove_fields = form_dialog.getDataCheckList("Select one or more options:", options_remove_fields, "Remove Existing Fields")
							for opt_remove in opt_remove_fields:
								list_fields_actual.remove(opt_remove)
							data_rule['fields'] = list_fields_actual
			if flag_restriction_hostname == 1:
				if data_rule['restrict_by_host'] == False:
					opt_rest_host_false = form_dialog.getDataRadioList("Select a option:", options_rest_host_false, "Restriction By Host")
					if opt_rest_host_false == "Enable":
						number_events_hostname = form_dialog.getDataNumber("Enter the total number of events per hostname to which the alert will be sent:", "3")
						data_rule['restrict_by_host'] = True
						restriction_host_json = { 'number_events_host' : int(number_events_hostname) }
						data_rule.update(restriction_host_json)
				else:
					opt_rest_host_true = form_dialog.getDataRadioList("Select a option:", options_rest_host_true, "Restriction By Host")
					if opt_rest_host_true == "To Disable":
						del data_rule['number_events_host']
						data_rule['restrict_by_host'] = False
					if opt_rest_host_true == "Modify Data":
						opt_rest_host_modify = form_dialog.getDataRadioList("Select a option:", options_rest_host_modify, "Restriction By Host")
						if opt_rest_host_modify == "Number of Events":
							number_events_hostname = form_dialog.getDataNumber("Enter the total number of events per hostname to which the alert will be sent:", str(data_rule['number_events_host']))
							data_rule['number_events_host'] = int(number_events_hostname)
			if flag_type_alert == 1:
				for opt_type_send in self.options_type_alert_send:
					if opt_type_send[0] == data_rule['type_alert_send']:
						opt_type_send[2] = 1
					else:
						opt_type_send[2] = 0
				type_alert_send = form_dialog.getDataRadioList("Select a option:", self.options_type_alert_send, "Alert Sending Type")
				data_rule['type_alert_send'] = str(type_alert_send)
			if flag_sending_alert == 1:
				flag_telegram = 0
				flag_email = 0
				flag_telegram_two = 0
				flag_email_two = 0
				for platform in data_rule['alert']:
					if platform == "telegram":
						flag_telegram = 1
					if platform == "email":
						flag_email = 1
				opt_send_alert = form_dialog.getDataCheckList("Select one or more options:", self.options_send_alert, "Alert Sending Platforms")
				for opt_send in opt_send_alert:
					if opt_send == "telegram":
						flag_telegram_two = 1
					if opt_send == "email":
						flag_email_two = 1
				if flag_telegram_two == 1:
					if flag_telegram == 1:
						opt_telegram_true = form_dialog.getDataRadioList("Select a option:", options_telegram_true, "Sending By Telegram")
						if opt_telegram_true == "To Disable":
							if flag_email == 1:
								del data_rule['alert']
								del data_rule['telegram_bot_token']
								del data_rule['telegram_chat_id']
								alert_json = { 'alert' : ['email'] }
								data_rule.update(alert_json)
							else:
								form_dialog.d.msgbox("\nThere must be at least one way to send the alert", 7, 50, title = "Error message")
								form_dialog.mainMenu()
						if opt_telegram_true == "Modify Data":
							flag_bot_token = 0
							flag_chat_id = 0
							opt_telegram_modify = form_dialog.getDataCheckList("Select one or more options:", options_telegram_modify, "Sending By Telegram")
							for opt_telegram in opt_telegram_modify:
								if opt_telegram == "Bot Token":
									flag_bot_token = 1
								if opt_telegram == "Chat ID":
									flag_chat_id = 1
							if flag_bot_token == 1:
								telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", self.utils.decryptAES(data_rule['telegram_bot_token']).decode('utf-8')))
								data_rule['telegram_bot_token'] = telegram_bot_token.decode('utf-8')
							if flag_chat_id == 1:
								telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", self.utils.decryptAES(data_rule['telegram_chat_id']).decode('utf-8')))
								data_rule['telegram_chat_id'] = telegram_chat_id.decode('utf-8')
					else:
						opt_telegram_false = form_dialog.getDataRadioList("Select a option:", options_telegram_false, "Sending By Telegram")
						if opt_telegram_false == "Enable":
							del data_rule['alert']
							telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
							telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
							telegram_json = { 'telegram_bot_token' : telegram_bot_token.decode('utf-8'), 'telegram_chat_id' : telegram_chat_id.decode('utf-8') }
							if flag_email == 1:
								alert_json = { 'alert' : ['telegram', 'email'] }
							else:
								alert_json = { 'alert' : ['telegram'] }
							data_rule.update(alert_json)
							data_rule.update(telegram_json)
				if flag_email_two == 1:
					if flag_email == 1:
						opt_email_true = form_dialog.getDataRadioList("Select a option:", options_email_true, "Sending By Email")
						if opt_email_true == "To Disable":
							if flag_telegram == 1:
								del data_rule['alert']
								del data_rule['email_from']
								del data_rule['email_from_password']
								del data_rule['email_to']
								alert_json = { 'alert' : ['telegram'] }
								data_rule.update(alert_json)
							else:
								form_dialog.d.msgbox("\nThere must be at least one way to send the alert", 7, 50, title = "Error message")
								form_dialog.mainMenu()
						if opt_email_true == "Modify Data":
							flag_email_from = 0
							flag_email_from_pass = 0
							flag_email_to = 0
							opt_email_modify = form_dialog.getDataCheckList("Select one or more options:", options_email_modify, "Sending By Email")
							for opt_email in opt_email_modify:
								if opt_email == "Email From":
									flag_email_from = 1
								if opt_email == "Email Password":
									flag_email_from_pass = 1
								if opt_email == "Email To":
									flag_email_to = 1
							if flag_email_from == 1:
								email_from = form_dialog.getDataEmail("Enter the email address from which the alerts will be sent (gmail or outlook):", str(data_rule['email_from']))
								data_rule['email_from'] = str(email_from)
							if flag_email_from_pass == 1:
								email_from_password = self.utils.encryptAES(form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"))
								data_rule['email_from_password'] = email_from_password.decode('utf-8')
							if flag_email_to == 1:
								list_emails_to_actual = data_rule['email_to']
								opt_email_to = form_dialog.getDataRadioList("Select a option:", options_email_to, "Recipient Email Addresses")
								if opt_email_to == "Add New Email(s)":
									number_email_to = form_dialog.getDataNumber("Enter the total number of email addresses to which the alert will be sent:", "3")
									list_email_to_add = form_dialog.getEmailAdd(number_email_to)
									list_email_to = form_dialog.getEmailsTo(list_email_to_add, "Destination Email Addresses:", "Enter email addresses:")
									for email_to in list_email_to:
										list_emails_to_actual.append(email_to)
									data_rule['email_to'] = list_emails_to_actual
								if opt_email_to == "Modify Email(s)":
									list_emails_to_update = form_dialog.getEmailsTo(list_emails_to_actual, "Recipient Email Addresses", "Modify the email address:")
									del data_rule['email_to']
									data['email_to'] = list_emails_to_update
								if opt_email_to == "Remove Email(s)":
									options_email_to_remove = []
									for email_to in list_emails_to_actual:
										options_email_to_remove.append((email_to, "", 0))
									opt_email_to_remove = form_dialog.getDataCheckList("Select one or more options:", options_email_to_remove, "Recipient Email Addresses")
									for opt_email_remove in opt_email_to_remove:
										list_emails_to_actual.remove(opt_email_remove)
									data_rule['email_to'] = list_emails_to_actual

					else:
						opt_email_false = form_dialog.getDataRadioList("Select a option:", options_email_false, "Sending By Email")
						if opt_email_false == "Enable":
							del data_rule['alert']
							email_from = form_dialog.getDataEmail("Enter the email address from which the alerts will be sent (gmail or outlook):", "usuario@gmail.com")
							email_from_password = self.utils.encryptAES(form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"))
							number_email_to = form_dialog.getDataNumber("Enter the total number of email addresses to which the alert will be sent:", "3")
							list_email_to_add = form_dialog.getEmailAdd(number_email_to)
							list_email_to = form_dialog.getEmailsTo(list_email_to_add, "Destination Email Addresses:", "Enter email addresses:")
							email_json = { 'email_from' : str(email_from), 'email_from_password' : email_from_password.decode('utf-8'), 'email_to' : list_email_to }
							if flag_telegram == 1:
								alert_json = { 'alert' : ['telegram', 'email'] }
							else:
								alert_json = { 'alert' : ['email'] }
							data_rule.update(email_json)
							data_rule.update(alert_json)
			with open(self.utils.getPathTalert(self.folder_rules) + '/' + name_alert_rule, "w") as file_rule_update:
				yaml.safe_dump(data_rule, file_rule_update, default_flow_style = False)
			hash_modify = self.utils.getSha256File(self.utils.getPathTalert(self.folder_rules) + '/' + name_alert_rule)
			if hash_origen == hash_modify:
				form_dialog.d.msgbox("\nAlert rule not modified", 7, 50, title = "Error message")
			else:
				self.logger.createLogTool("Modified alert rule: " + name_alert_rule, 3)
				form_dialog.d.msgbox("\nModified alert rule: " + name_alert_rule, 7, 50, title = "Notification message")
			if flag_name == 1:
				os.rename(self.utils.getPathTalert(self.folder_rules) + '/' + name_alert_rule, self.utils.getPathTalert(self.folder_rules) + '/' + name_rule + '.yaml')	
			form_dialog.mainMenu()
		except KeyError as exception:
			self.logger.createLogTool("Key not found in configuration file: " + str(exception), 4)
			form_dialog.d.msgbox("\nKey not found in configuration file: " + str(exception), 7, 50, title = "Error message")
			form_dialog.mainMenu()
		except OSError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nError opening the alert rule. For more details, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()

	"""
	Method that eliminates one or more alert rules.

	Parameters:
	self -- An instantiated object of the Rules class.
	form_dialog -- A FormDialogs class object.
	"""
	def getDeleteRules(self, form_dialog):
		list_rules_delete = self.getAllAlertRules(self.utils.getPathTalert(self.folder_rules))
		if len(list_rules_delete) == 0:
			form_dialog.d.msgbox("\nThere are no alert rules in the directory", 7, 50, title = "Error message")
		else:
			options_rules_delete = []
			for rule in list_rules_delete:
				options_rules_delete.append((rule, "", 0))
			opt_rules_delete = form_dialog.getDataCheckList("Select one or more options:", options_rules_delete, "Delete Alert Rules")
			for opt_rule in opt_rules_delete:
				os.remove(self.utils.getPathTalert(self.folder_rules) + '/' + opt_rule)
			form_dialog.d.msgbox("\nAlert rule(s) removed", 7, 50, title = "Notification message")
		form_dialog.mainMenu()

	"""
	Method that shows all the alert rules created so far on the screen.

	Parameters:
	self -- An instantiated object of the Rules class.
	form_dialog -- A FormDialogs class object.
	"""
	def showAllAlertRules(self, form_dialog):
		list_all_rules = self.getAllAlertRules(self.utils.getPathTalert(self.folder_rules))
		if len(list_all_rules) == 0:
			form_dialog.getScrollBox("Zero alert rules in " + str(self.folder_rules), "Alert Rules")
		else:
			message = "\nAlert rules in " + str(self.folder_rules) + ":\n\n"
			for rule in list_all_rules:
				message += "-" + rule + "\n"
			form_dialog.getScrollBox(message, "Alert Rules")

	"""
	Method that allows creating the alert rule file with extension .yaml based on what was entered.

	Parameters:
	self -- An instantiated object of the Rules class.
	data_rule -- List with all the data entered for the alert rule.
	flag_telegram -- Flag that lets you know if the alert will be sent by telegram or not.
	flag_email -- Flag that lets you know if the alert will be sent by email or not.

	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” 
	or “disk full” (not for illegal argument types or other incidental errors).
	"""
	def createRuleYaml(self, data_rule, flag_telegram, flag_email):
		d_rule = {'name_rule' : str(data_rule[0]),
		'alert_level' : str(data_rule[1]),
		'type_alert' : str(data_rule[3]),
		'index_name' : str(data_rule[2]),
		'num_events' : int(data_rule[4]),
		'time_search' : { str(data_rule[5]) : int(data_rule[6]) },
		'time_back' : { str(data_rule[7]) : int(data_rule[8]) },
		'filter_search' : [{ str(data_rule[9]) : { 'query' : str(data_rule[10])}}],
		'type_alert_send' : str(data_rule[11]),
		'use_restriction_fields' : data_rule[12]
		}

		if data_rule[12] == True:
			fields_json = { 'fields' : data_rule[13] }
			d_rule.update(fields_json)
			restrict_by_host = data_rule[14]
			if restrict_by_host == True:
				number_events_host = { 'number_events_host' : int(data_rule[15]), 'field_hostname' : str(data_rule[16]) }
				d_rule.update(number_events_host)
				last_index = 16
			else:
				last_index = 14
		else:
			restrict_by_host = data_rule[13]
			if restrict_by_host == True:
				number_events_host = { 'number_events_host' : int(data_rule[14]), 'field_hostname' : str(data_rule[15]) }
				d_rule.update(number_events_host)
				last_index = 15
			else:
				last_index = 13
		restrict_host_json = { 'restrict_by_host' : restrict_by_host }
		d_rule.update(restrict_host_json)
		if flag_telegram == 1 and flag_email == 0:
			alert_json = { 'alert' : ['telegram'] }
			telegram_json = { 'telegram_bot_token' : data_rule[last_index + 1].decode('utf-8'), 'telegram_chat_id' : data_rule[last_index + 2].decode('utf-8') }
			d_rule.update(telegram_json)
			d_rule.update(alert_json)
		if flag_email == 1 and flag_telegram == 0:
			alert_json = { 'alert' : ['email'] }
			email_json = { 'email_from' : str(data_rule[last_index + 1]), 'email_from_password' : data_rule[last_index + 2].decode('utf-8'), 'email_to' : data_rule[last_index + 3] }
			d_rule.update(email_json)
			d_rule.update(alert_json)
		if flag_telegram == 1 and flag_email == 1:
			alert_json = { 'alert' : ['telegram', 'email'] }
			telegram_json = { 'telegram_bot_token' : data_rule[last_index + 1].decode('utf-8'), 'telegram_chat_id' : data_rule[last_index + 2].decode('utf-8') }
			email_json = { 'email_from' : str(data_rule[last_index + 3]), 'email_from_password' : data_rule[last_index + 4].decode('utf-8'), 'email_to' : data_rule[last_index + 5] }
			d_rule.update(telegram_json)
			d_rule.update(email_json)
			d_rule.update(alert_json)
		try:
			with open(self.utils.getPathTalert(self.folder_rules) + '/' + str(data_rule[0]) + '.yaml', 'w') as rule_file:
				yaml.dump(d_rule, rule_file, default_flow_style = False)
			self.utils.changeUidGid(self.utils.getPathTalert(self.folder_rules) + '/' + str(data_rule[0]) + '.yaml')
		except OSError as exception:
			self.logger.createLogTool(str(exception), 4)

	"""
	Method that shows on screen all the alert rules created so far to select one, which will be modified.

	Parameters:
	self -- An instantiated object of the Rules class.
	form_dialog -- A FormDialogs class object.
	"""
	def getUpdateAlertRules(self, form_dialog):
		list_alert_rules = self.getAllAlertRules(self.utils.getPathTalert(self.folder_rules))
		if len(list_alert_rules) == 0:
			form_dialog.d.msgbox("\nThere are no alert rules in the directory", 5, 50, title = "Error message")
		else:
			options_alert_rules = []
			for alert_rule in list_alert_rules:
				options_alert_rules.append((alert_rule, "", False))
			rule_to_modify = form_dialog.getDataRadioList("Select a option:", options_alert_rules, "Alert Rules List")
			self.modifyAlertRule(form_dialog, rule_to_modify)

	"""
	Method that gets a list with all the names of the alert rules stored in the rules directory.

	Parameters:
	self -- An instantiated object of the Rules class.
	path_folder_rules -- Directory where all alert rules are stored.

	Return:
	list_alert_rules -- List with the names of the alert rules stored in the directory.
	"""
	def getAllAlertRules(self, path_folder_rules):
		list_alert_rules = [os.path.basename(x) for x in glob.glob(path_folder_rules + '/*.yaml')]
		return list_alert_rules




 