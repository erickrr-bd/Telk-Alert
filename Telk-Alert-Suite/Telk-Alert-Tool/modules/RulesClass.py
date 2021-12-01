from glob import glob
from os import path, remove
from modules.UtilsClass import Utils

"""
Class that allows handling everything related to alert rules.
"""
class Rules:
	"""
	Property that stores the path of the folder where the alert rules are saved.
	"""
	path_folder_rules = None

	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Property that stores an object of the FormDialog class.
	"""
	form_dialog = None
	
	"""
	Property that contains the options for the alert rule level.
	"""
	list_level_alert = [["Low", "Low level alert", 1],
						["Medium", "Medium level alert", 0],
						["High", "High level alert", 0]]

	"""
	Property that contains the options for the unit of time.
	"""
	list_unit_time = [["minutes", "Time expressed in minutes", 1],
					  ["hours", "Time expressed in hours", 0],
					  ["days", "Time expressed in days", 0]]

	"""
	Property that contains the options for the alert sending platforms.
	"""
	list_send_platform = [("telegram", "The alert will be sent via Telegram", 0),
					      ("email", "The alert will be sent via email", 0)]

	"""
	Property that stores the options for the types of sending alerts.
	"""
	list_type_alert_send = [["only", "A single alert with the total of events found", 1],
						    ["multiple", "An alert for each event found", 0]]

	"""
	Property that stores the options of the types of restrictions for a custom rule.
	"""
	list_custom_rule = [("Hostname", "Restrict by hostname", 0),
					 	("Username", "Restrict by username", 0)]

	"""
	Constructor for the Rules class.

	Parameters:
	self -- An instantiated object of the Rules class.
	form_dialog -- FormDialog class object.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		name_folder_rules = self.utils.readYamlFile(self.utils.getPathTelkAlert('conf') + '/telk_alert_conf.yaml', 'r')['rules_folder']
		self.path_folder_rules = self.utils.getPathTelkAlert(name_folder_rules)

	"""
	Method that requests the data for the creation of an alert rule.

	Parameters:
	self -- An instantiated object of the Rules class.
	"""
	def createNewRule(self):
		list_type_alert = [("Frequency", "Make the searches in the index periodically", 1)]

		list_query_type = [("query_string", "Perform the search using the Query String of ElasticSearch", 1)]

		data_alert_rule = []
		name_alert_rule = self.form_dialog.getDataNameFolderOrFile("Enter the name of the alert rule:", "rule1")
		data_alert_rule.append(name_alert_rule)
		option_level_alert = self.form_dialog.getDataRadioList("Select a option:", self.list_level_alert, "Alert Rule Level")
		data_alert_rule.append(option_level_alert)
		es_index_name = self.form_dialog.getDataInputText("Enter the name of the index or index pattern where it will be searched:", "winlogbeat-*")
		data_alert_rule.append(es_index_name)
		option_type_rule = self.form_dialog.getDataRadioList("Select a option:", list_type_alert, "Alert Rule Type")
		data_alert_rule.append(option_type_rule)
		if option_type_rule == "Frequency":
			number_events = self.form_dialog.getDataNumber("Enter the number of events found to which the alert is sent:", "1")
			data_alert_rule.append(number_events)
			option_unit_time_search = self.form_dialog.getDataRadioList("Select a option:", self.list_unit_time, "Time Unit")
			data_alert_rule.append(option_unit_time_search)
			number_unit_time_search = self.form_dialog.getDataNumber("Enter the total in " + str(option_unit_time_search) + " in which you want the search to be repeated:", "2")
			data_alert_rule.append(number_unit_time_search)
			option_unit_time_range = self.form_dialog.getDataRadioList("Select a option:", self.list_unit_time, "Time Unit")
			data_alert_rule.append(option_unit_time_range)
			number_unit_time_range = self.form_dialog.getDataNumber("Enter the total in " + str(option_unit_time_range) + " that define the range in which the events to search should be found:", "2")
			data_alert_rule.append(number_unit_time_range)
		query_type = self.form_dialog.getDataRadioList("Select a option:", list_query_type, "Query Type")
		data_alert_rule.append(query_type)
		if query_type == "query_string":
			query_string = self.form_dialog.getDataInputText("Enter the query string:", "event.code : 4120")
			data_alert_rule.append(query_string)
		specific_fields_search = self.form_dialog.getDataYesOrNo("\nDo you require that the search only return certain fields?", "Specific Fields In Search")
		if specific_fields_search == "ok":
			data_alert_rule.append(True)
			total_fields_to_enter = self.form_dialog.getDataNumber("Enter the total number of field names to be defined:", "2")
			list_to_fields = self.utils.generateListToForm(int(total_fields_to_enter), "Field")
			list_fields_names = self.form_dialog.getForm("Enter the name of the fields:", list_to_fields, "Field Names", 1)
			data_alert_rule.append(list_fields_names)
		else:
			data_alert_rule.append(False)
		is_custom_rule = self.form_dialog.getDataYesOrNo("\nDo you need to create a custom alert rule?", "Custom Rule")
		if is_custom_rule == "ok":
			data_alert_rule.append(True)
			flag_hostname = 0
			flag_username = 0
			options_custom_rule = self.form_dialog.getDataCheckList("Select one or more options:", self.list_custom_rule, "Custom Rule")
			for option in options_custom_rule:
				if option == "Hostname":
					flag_hostname = 1
				elif option == "Username":
					flag_username = 1
			if flag_hostname == 1:
				data_alert_rule.append(True)
				field_name_hostname = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the hostname:", "host.hostname")
				data_alert_rule.append(field_name_hostname)
				number_events_hostname = self.form_dialog.getDataNumber("Enter the number of events per hostname to which the alert will be sent:", "3")
				data_alert_rule.append(number_events_hostname)
			else:
				data_alert_rule.append(False)
			if flag_username == 1:
				data_alert_rule.append(True)
				field_name_username = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the username:", "winlog.username")
				data_alert_rule.append(field_name_username)
				number_events_username = self.form_dialog.getDataNumber("Enter the number of events per username to which the alert will be sent:", "3")
				data_alert_rule.append(number_events_username)
			else:
				data_alert_rule.append(False)
		else:
			data_alert_rule.append(False)
		option_type_alert_send = self.form_dialog.getDataRadioList("Select a option:", self.list_type_alert_send, "Alert Sending Type")
		data_alert_rule.append(option_type_alert_send)
		options_send_platform = self.form_dialog.getDataCheckList("Select one or more options:", self.list_send_platform, "Alert Sending Platforms")
		flag_telegram = 0
		flag_email = 0
		for option in options_send_platform:
			if option == "telegram":
				flag_telegram = 1
			elif option == "email":
				flag_email = 1
		if flag_telegram == 1:
			telegram_bot_token = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
			data_alert_rule.append(telegram_bot_token.decode('utf-8'))
			telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
			data_alert_rule.append(telegram_chat_id.decode('utf-8'))
		if flag_email == 1:
			email_from = self.form_dialog.getDataEmail("Enter the email address from which the alerts will be sent (gmail or outlook):", "usuario@gmail.com")
			data_alert_rule.append(email_from)
			email_from_password = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"))
			data_alert_rule.append(email_from_password.decode('utf-8'))
			total_emails_to_enter = self.form_dialog.getDataNumber("Enter the total number of email address to be defined:", "3")
			list_to_emails = self.utils.generateListToForm(int(total_emails_to_enter), "Email")
			list_email_address = self.form_dialog.getForm("Enter the email addresses:", list_to_emails, "Email Addresses", 2)
			data_alert_rule.append(list_email_address)
		self.createRuleYaml(data_alert_rule, flag_telegram, flag_email)
		if(not path.exists(self.path_folder_rules + '/' + name_rule + '.yaml')):
			self.form_dialog.d.msgbox("\nError creating alert rule. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
		else:
			self.utils.createTelkAlertToolLog("Alert rule created: " + name_rule, 1)
			self.form_dialog.d.msgbox(text = "\nAlert rule created: " + name_rule + '.', height = 7, width = 50, title = "Notification Message")	
		self.form_dialog.mainMenu()

	"""
	Method that modifies one or more fields of a specific alert rule.

	Parameters:
	self -- An instantiated object of the Rules class.
	name_alert_rule -- Name of the alert rule to be modified.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict).
	"""
	def updateAlertRule(self, name_alert_rule):
		list_fields_update = [("Name", "Alert rule name", 0),
							  ("Level", "Alert rule level", 0),
							  ("Index", "Index name or index pattern in ElastcSearch", 0),
							  ("Number Events", "Number of events to which the alert is sent", 0),
							  ("Time Search", "Time in which the search will be repeated", 0),
							  ("Time Range", "Time range in which events will be searched", 0),
							  ("Query String", "Query string for event search", 0),
							  ("Specific Fields", "Enables or disables the use of specific fields", 0),
							  ("Custom Rule", "Enable or disable the use of custom rule", 0),
							  ("Shipping Type", "How the alert will be sent", 0),
							  ("Platforms", "Alerts sending platforms", 0)]

		list_specific_fields_false = [("Enable", "Enables the use of specific fields", 0)]

		list_specific_fields_true = [("Disable", "Disable the use of specific fields", 0),
								     ("Data", "Modify configured data", 0)]

		list_specific_fields_update = [("1", "Add New Field(s)"),
									   ("2", "Modify Field(s)"),
									   ("3", "Remove Field(s)")]

		list_custom_rule_false = [("Enable", "Enable the use of a custom rule", 0)]

		list_custom_rule_true = [("Disable", "Disable the use of a custom rule", 0),
								 ("Data", "Modify configured data", 0)]

		list_restriction_hostname_false = [("Enable", "Enable restriction by hostname", 0)]

		list_restriction_hostname_true = [("Disable", "Disable hostname restriction", 0),
								 		   ("Data", "Modify configured data", 0)]

		list_restriction_hostname_update = [("Field", "Name of the field in the index", 0),
								 		    ("Events", "Number of events per hostname", 0)]

		list_restriction_username_false = [("Enable", "Enable restriction by username", 0)]

		list_restriction_username_true = [("Disable", "Disable restriction by username", 0),
								 		  ("Data", "Modify configured data", 0)]

		list_restriction_username_update = [("Field", "Name of the field in the index", 0),
								 		    ("Events", "Number of events per hostname", 0)]

		list_telegram_true = [("Disable", "Disable the sending of alerts by Telegram", 0),
							  ("Data", "Modify configured data", 0)]

		list_telegram_false = [("Enable", "Enable the sending of alerts by Telegram", 0)]

		list_telegram_update = [("Bot Token", "Telegram bot token", 0),
								("Chat ID", "Telegram channel identifier", 0)]

		list_email_true = [("Disable", "Disable the sending of alerts by Email", 0),
						   ("Data", "Modify configured data", 0)]

		list_email_false = [("Enable", "Enable the sending of alerts by Email", 0)]

		list_email_update = [("Email From", "Sender email address", 0),
							 ("Email Password", "Sender email password", 0),
							 ("Email To", "Recipient email addresses", 0)]

		list_email_to = [("1", "Add New Email(s)"),
						 ("2", "Modify Email(s)"),
						 ("3", "Remove Email(s)")]

		flag_name_rule = 0
		flag_level_rule = 0
		flag_index_rule = 0
		flag_number_events_rule = 0
		flag_time_search_rule = 0
		flag_time_range_rule = 0
		flag_query_string_rule = 0
		flag_specific_fields_rule = 0
		flag_custom_rule = 0
		flag_type_alert_rule = 0
		flag_platform_rule = 0
		flag_name_rename = 0
		options_fields_update = self.form_dialog.getDataCheckList("Select one or more options:", list_fields_update, "Alert Rule Fields")
		for option in options_fields_update:
			if option == "Name":
				flag_name_rule = 1
			elif option == "Level":
				flag_level_rule = 1
			elif option == "Index":
				flag_index_rule = 1
			elif option == "Number Events":
				flag_number_events_rule = 1
			elif option == "Time Search":
				flag_time_search_rule = 1
			elif option == "Time Range":
				flag_time_range_rule = 1
			elif option == "Query String":
				flag_query_string_rule = 1
			elif option == "Specific Fields":
				flag_specific_fields_rule = 1
			elif option == "Custom Rule":
				flag_custom_rule = 1
			elif option == "Shipping Type":
				flag_type_alert_rule = 1
			elif option == "Platforms":
				flag_platform_rule = 1
		try:
			data_rule = self.utils.readYamlFile(self.path_folder_rules + '/' + name_alert_rule, 'rU')
			hash_file_actual = self.utils.getHashToFile(self.utils.getPathTelkAlert(self.path_folder_rules) + '/' + name_alert_rule)
			if flag_name_rule == 1:
				name_rule_actual = data_rule['name_rule']
				name_rule = self.form_dialog.getDataNameFolderOrFile("Enter the name of the alert rule:", data_rule['name_rule'])
				if not name_rule == name_rule_actual:
					flag_name_rename = 1
					data_rule['name_rule'] = name_rule
			if flag_level_rule == 1:
				for option in self.list_level_alert:
					if option[0] == data_rule['alert_level']:
						option[2] = 1
					else:
						option[2] = 0
				level_alert = self.form_dialog.getDataRadioList("Select a option:", self.list_level_alert, "Alert Rule Level")
				data_rule['alert_level'] = level_alert
			if flag_index_rule == 1:
				index_name = self.form_dialog.getDataInputText("Enter the name of the index or index pattern where it will be searched:", data_rule['index_name'])
				data_rule['index_name'] = index_name
			if flag_number_events_rule == 1:
				num_events = self.form_dialog.getDataNumber("Enter the number of events found to which the alert is sent:", str(data_rule['num_events']))
				data_rule['num_events'] = int(num_events)
			if flag_time_search_rule == 1:
				for unit_time in data_rule['time_search']:
					num_time_search_actual = unit_time
				for option in self.list_unit_time:
					if option[0] == num_time_search_actual:
						option[2] = 1
					else:
						option[2] = 0
				unit_time_search = self.form_dialog.getDataRadioList("Select a option:", self.list_unit_time, "Time Unit")
				num_time_search = self.form_dialog.getDataNumber("Enter the total in " + str(unit_time_search) + " in which you want the search to be repeated:", str(data_rule['time_search'][num_time_search_actual]))
				data_rule['time_search'] = { str(unit_time_search) : int(num_time_search) }
			if flag_time_range_rule == 1:
				for unit_time in data_rule['time_range']:
					num_time_range_actual = unit_time
				for option in self.list_unit_time:
					if option[0] == num_time_range_actual:
						option[2] = 1
					else:
						option[2] = 0
				unit_time_range = self.form_dialog.getDataRadioList("Select a option:", self.list_unit_time, "Time Unit")
				num_time_range = self.form_dialog.getDataNumber("Enter the total in " + str(unit_time_range) + " that define the range in which the events to search should be found:", str(data_rule['time_range'][num_time_range_actual]))
				data_rule['time_range'] = { unit_time_range : int(num_time_range) }
			if flag_query_string_rule == 1:
				query_string = self.form_dialog.getDataInputText("Enter the query string:", data_rule['query_type'][0]['query_string']['query'])
				data_rule['query_type'] = [ { 'query_string' : { 'query' : query_string }}]
			if flag_specific_fields_rule == 1:
				if data_rule['specific_fields_search'] == True:
					option_specific_fields_true = self.form_dialog.getDataRadioList("Select a option:", list_specific_fields_true, "Use Of Specific Fields")
					if option_specific_fields_true == "Disable":
						data_rule['specific_fields_search'] = False
						del(data_rule['field_name'])
					elif option_specific_fields_true == "Data":
						option_specific_fields_update = self.form_dialog.getMenu("Select a option:", list_specific_fields_update, "Actions To Perform")
						if int(option_specific_fields_update) == 1:
							total_fields_to_enter = self.form_dialog.getDataNumber("Enter the total number of field names to be add:", "2")
							list_to_fields = self.utils.generateListToForm(int(total_fields_to_enter), "Field")
							list_fields_names = self.form_dialog.getForm("Enter the name of the fields:", list_to_fields, "Field Names", 1)
							data_rule['field_name'].extend(list_fields_names)
						elif int(option_specific_fields_update) == 2:
							list_convert_to_form = self.utils.convertListToForm("Field", data_rule['field_name'])
							list_fields_names = self.form_dialog.getForm("Enter the name of the fields:", list_convert_to_form, "Field Names", 1)
							data_rule['field_name'] = list_fields_names
						elif int(option_specific_fields_update) == 3:
							list_specific_fields = self.utils.convertListToCheckOrRadioList(data_rule['field_name'], "Field")
							options_specific_fields = self.form_dialog.getDataCheckList("Select one or more options:", list_specific_fields, "Fields Names")
							for option in options_specific_fields:
								data_rule['field_name'].remove(option)
				else:
					option_specific_fields_false = self.form_dialog.getDataRadioList("Select a option:", list_specific_fields_false, "Use Of Specific Fields")
					if option_specific_fields_false == "Enable":
						data_rule['specific_fields_search'] = True
						total_fields_to_enter = self.form_dialog.getDataNumber("Enter the total number of field names to be defined:", "2")
						list_to_fields = self.utils.generateListToForm(int(total_fields_to_enter), "Field")
						list_fields_names = self.form_dialog.getForm("Enter the name of the fields:", list_to_fields, "Field Names", 1)
						fields_name_json = { 'field_name' : list_fields_names }
						data_rule.update(fields_name_json)
			if flag_custom_rule == 1:
				if data_rule['custom_rule'] == True:
					option_custom_rule_true = self.form_dialog.getDataRadioList("Select a option:", list_custom_rule_true, "Custom Rule")
					if option_custom_rule_true == "Disable":
						data_rule['custom_rule'] = False
						if 'restriction_hostname' in data_rule:
							if data_rule['restriction_hostname'] == True:
								del(data_rule['field_hostname'])
								del(data_rule['number_events_hostname'])
							del(data_rule['restriction_hostname'])
						if 'restriction_username' in data_rule:
							if data_rule['restriction_username'] == True:
								del(data_rule['field_username'])
								del(data_rule['number_events_username'])
							del(data_rule['restriction_username'])
					elif option_custom_rule_true == "Data":
						flag_hostname = 0
						flag_username = 0
						options_custom_rule = self.form_dialog.getDataCheckList("Select one or more options:", self.list_custom_rule, "Custom Rule")
						for option in options_custom_rule:
							if option == "Hostname":
								flag_hostname = 1
							elif option == "Username":
								flag_username = 1
						if flag_hostname == 1:
							if 'restriction_hostname' in data_rule:
								if data_rule['restriction_hostname'] == True:
									option_restriction_hostname_true = self.form_dialog.getDataRadioList("Select a option:", list_restriction_hostname_true, "Restriction By Hostname")
									if option_restriction_hostname_true == "Disable":
										data_rule['restriction_hostname'] = False
										del(data_rule['field_hostname'])
										del(data_rule['number_events_hostname'])
									elif option_restriction_hostname_true == "Data":
										flag_field_hostname = 0
										flag_number_events_hostname = 0
										options_restriction_hostname_update = self.form_dialog.getDataCheckList("Select one or more options:", list_restriction_hostname_update, "Restriction By Hostname")
										for option in options_restriction_hostname_update:
											if option == "Field":
												flag_field_hostname = 1
											elif option == "Events":
												flag_number_events_hostname = 1
										if flag_field_hostname == 1:
											field_name_hostname = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the hostname:", data_rule['field_hostname'])
											data_rule['field_hostname'] = field_name_hostname
										if flag_number_events_hostname == 1:
											number_events_hostname = self.form_dialog.getDataNumber("Enter the number of events per hostname to which the alert will be sent:", str(data_rule['number_events_hostname']))
											data_rule['number_events_hostname'] = int(number_events_hostname)
								else:
									option_restriction_hostname_false = self.form_dialog.getDataRadioList("Select a option:", list_restriction_hostname_false, "Restriction By Hostname")
									if option_restriction_hostname_false == "Enable":
										data_rule['restriction_hostname'] = True
										field_name_hostname = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the hostname:", "host.hostname")
										number_events_hostname = self.form_dialog.getDataNumber("Enter the number of events per hostname to which the alert will be sent:", "3")
										restriction_hostname_json = { 'field_hostname' : field_name_hostname, 'number_events_hostname' : int(number_events_hostname) }
										data_rule.update(restriction_hostname_json)
						if flag_username == 1:
							if 'restriction_username' in data_rule:
								if data_rule['restriction_username'] == True:
									option_restriction_username_true = self.form_dialog.getDataRadioList("Select a option:", list_restriction_username_true, "Restriction By Username")
									if option_restriction_username_true == "Disable":
										data_rule['restriction_username'] = False
										del(data_rule['field_username'])
										del(data_rule['number_events_username'])
									elif option_restriction_username_true == "Data":
										flag_field_username = 0
										flag_number_events_username = 0
										options_restriction_username_update = self.form_dialog.getDataCheckList("Select one or more options:", list_restriction_username_update, "Restriction By Username")
										for option in options_restriction_username_update:
											if option == "Field":
												flag_field_username = 1
											elif option == "Events":
												flag_number_events_username = 1
										if flag_field_username == 1:
											field_name_username = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the username:", data_rule['field_username'])
											data_rule['field_username'] = field_name_username
										if flag_number_events_username == 1:
											number_events_username = self.form_dialog.getDataNumber("Enter the number of events per username to which the alert will be sent:", str(data_rule['number_events_username']))
											data_rule['number_events_username'] = int(number_events_username)
								else:
									option_restriction_username_false = self.form_dialog.getDataRadioList("Select a option:", list_restriction_username_false, "Restriction By Username")
									if option_restriction_username_false == "Enable":
										data_rule['restriction_username'] = True
										field_name_username = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the username:", "winlog.username")
										number_events_username = self.form_dialog.getDataNumber("Enter the number of events per username to which the alert will be sent:", "3")
										restriction_username_json = { 'field_username' : field_name_username, 'number_events_username' : int(number_events_username) }
										data_rule.update(restriction_username_json)
				else:
					option_custom_rule_false = self.form_dialog.getDataRadioList("Select a option:", list_custom_rule_false, "Custom Rule")
					if option_custom_rule_false == "Enable":
						flag_hostname = 0
						flag_username = 0
						options_custom_rule = self.form_dialog.getDataCheckList("Select one or more options:", self.list_custom_rule, "Custom Rule")
						for option in options_custom_rule:
							if option == "Hostname":
								flag_hostname = 1
							elif option == "Username":
								flag_username = 1
						if flag_hostname == 1:
							field_name_hostname = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the hostname:", "host.hostname")
							number_events_hostname = self.form_dialog.getDataNumber("Enter the number of events per hostname to which the alert will be sent:", "3")
							restriction_hostname_json = { 'restriction_hostname' : True, 'field_hostname' : field_name_hostname, 'number_events_hostname' : int(number_events_hostname) }
						else:
							restriction_hostname_json = { 'restriction_hostname' : False }
						if flag_username == 1:
							field_name_username = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the username:", "winlog.username")
							number_events_username = self.form_dialog.getDataNumber("Enter the number of events per username to which the alert will be sent:", "3")
							restriction_username_json = { 'restriction_username' : True, 'field_username' : field_name_username, 'number_events_username' : int(number_events_username) }
						else:
							restriction_username_json = { 'restriction_username' : False }
						data_rule['custom_rule'] = True
						data_rule.update(restriction_hostname_json)
						data_rule.update(restriction_username_json)
			if flag_type_alert_rule == 1:
				for option in self.list_type_alert_send:
					if option[0] == data_rule['type_alert_send']:
						option[2] = 1
					else:
						option[2] = 0
				option_type_alert_send = self.form_dialog.getDataRadioList("Select a option:", self.list_type_alert_send, "Alert sending type")
				data_rule['type_alert_send'] = option_type_alert_send
			if flag_platform_rule == 1:
				flag_telegram_defined = 0
				flag_telegram_option = 0
				flag_email_defined = 0
				flag_email_option = 0
				for value in data_rule['alert']:
					if value == "telegram":
						flag_telegram_defined = 1
					elif value == "email":
						flag_email_defined = 1
				options_send_platform = self.form_dialog.getDataCheckList("Select one or more options:", self.list_send_platform, "Alert Sending Platform")
				for option in options_send_platform:
					if option == "telegram":
						flag_telegram_option = 1
					elif option == "email":
						flag_email_option = 1
				if flag_telegram_option == 1:
					if flag_telegram_defined == 1:
						option_telegram_true = self.form_dialog.getDataRadioList("Select a option:", list_telegram_true, "Telegram")
						if option_telegram_true == "Disable":
							if flag_email_defined == 1:
								data_rule['alert'].remove('telegram')
								del(data_rule['telegram_bot_token'])
								del(data_rule['telegram_chat_id'])
							else:
								self.form_dialog.d.msgbox(text = "\nFailed to disable. There must be at least one way to send alerts.", height = 8, width = 50, title = "Notification Message")
						elif option_telegram_true == "Data":
							flag_telegram_bot_token = 0
							flag_telegram_chat_id = 0
							options_telegram_update = self.form_dialog.getDataCheckList("Select one or more options:", list_telegram_update, "Telegram")
							for option in options_telegram_update:
								if option == "Bot Token":
									flag_telegram_bot_token = 1
								elif option == "Chat ID":
									flag_telegram_chat_id = 1
							if flag_telegram_bot_token == 1:
								telegram_bot_token = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram bot token:", self.utils.decryptAES(data_rule['telegram_bot_token']).decode('utf-8')))
								data_rule['telegram_bot_token'] = telegram_bot_token.decode('utf-8')
							if flag_telegram_chat_id == 1:
								telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", self.utils.decryptAES(data_rule['telegram_chat_id']).decode('utf-8')))
								data_rule['telegram_chat_id'] = telegram_chat_id.decode('utf-8')
					else:
						option_telegram_false = self.form_dialog.getDataRadioList("Select a option:", list_telegram_false, "Telegram")
						if option_telegram_false == "Enable":
							data_rule['alert'].append('telegram')
							telegram_bot_token = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
							telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
							telegram_data_json = { 'telegram_bot_token' : telegram_bot_token.decode('utf-8'), 'telegram_chat_id' : telegram_chat_id.decode('utf-8') }
							data_rule.update(telegram_data_json)
				if flag_email_option == 1:
					if flag_email_defined == 1:
						option_email_true = self.form_dialog.getDataRadioList("Select a option:", list_email_true, "Email")
						if option_email_true == "Disable":
							if flag_telegram_defined == 1:
								data_rule['alert'].remove('email')
								del(data_rule['email_from'])
								del(data_rule['email_from_password'])
								del(data_rule['email_to'])
							else:
								self.form_dialog.d.msgbox(text = "\nFailed to disable. There must be at least one way to send alerts.", height = 8, width = 50, title = "Notification Message")
						elif option_email_true == "Data":
							flag_email_from = 0
							flag_email_from_password = 0
							flag_email_to = 0
							options_email_update = self.form_dialog.getDataCheckList("Select one or more options:", list_email_update, "Email")
							for option in options_email_update:
								if option == "Email From":
									flag_email_from = 1
								elif option == "Email Password":
									flag_email_from_password = 1
								elif option == "Email To":
									flag_email_to = 1
							if flag_email_from == 1:
								email_from = self.form_dialog.getDataEmail("Enter the email address from which the alerts will be sent (gmail or outlook):", data_rule['email_from'])
								data_rule['email_from'] = email_from
							if flag_email_from_password == 1:
								email_from_password = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"))
								data_rule['email_from_password'] = email_from_password.decode('utf-8')
							if flag_email_to == 1:
								option_email_to = self.form_dialog.getMenu("Select a option:", list_email_to, "Actions To Perform")
								if int(option_email_to) == 1:
									total_emails_to_enter = self.form_dialog.getDataNumber("Enter the total number of email address to add:", "3")
									list_to_emails = self.utils.generateListToForm(int(total_emails_to_enter), "Email")
									list_email_address = self.form_dialog.getForm("Enter the email addresses:", list_to_emails, "Email Addresses", 2)
									data_rule['email_to'].extend(list_email_address)
								elif int(option_email_to) == 2:
									list_convert_to_form = self.utils.convertListToForm("Email", data_rule['email_to'])
									list_email_address = self.form_dialog.getForm("Enter the email addresses:", list_convert_to_form, "Email Addresses", 2)
									data_rule['email_to'] = list_email_address
								elif int(option_email_to) == 3:
									list_emails_to = self.utils.convertListToCheckOrRadioList(data_rule['email_to'], "Email")
									options_email_to = self.form_dialog.getDataCheckList("Select one or more options:", list_emails_to, "Email To")
									for option in options_email_to:
										data_rule['email_to'].remove(option)
					else:
						option_email_false = self.form_dialog.getDataRadioList("Select a option:", list_email_false, "Email")
						if option_email_false == "Enable":
							data_rule['alert'].append('email')
							email_from = self.form_dialog.getDataEmail("Enter the email address from which the alerts will be sent (gmail or outlook):", "usuario@gmail.com")
							email_from_password = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"))
							total_emails_to_enter = self.form_dialog.getDataNumber("Enter the total number of email address to be defined:", "3")
							list_to_emails = self.utils.generateListToForm(int(total_emails_to_enter), "Email")
							list_email_address = self.form_dialog.getForm("Enter the email addresses:", list_to_emails, "Email Addresses", 2)
							email_data_json = { 'email_from' : email_from, 'email_from_password' : email_from_password.decode('utf-8'), 'email_to' : list_email_address }
							data_rule.update(email_data_json)
			self.utils.createYamlFile(data_rule, self.path_folder_rules + '/' + name_alert_rule, 'w')
			hash_file_new = self.utils.getHashToFile(self.path_folder_rules + '/' + name_alert_rule)
			if hash_file_actual == hash_file_new:
				self.form_dialog.d.msgbox(text = "\nAlert rule not modified: " + name_alert_rule, height = 7, width = 50, title = "Notification message")
			else:
				self.utils.createTelkAlertToolLog("Modified alert rule: " + name_alert_rule, 2)
				self.form_dialog.d.msgbox(text = "\nModified alert rule: " + name_alert_rule, height = 7, width = 50, title = "Notification Message")
			if flag_name_rename == 1:
				self.utils.renameFileOrDirectory(self.path_folder_rules + '/' + name_rule_actual + ".yaml", self.path_folder_rules + '/' + name_rule + ".yaml")	
			self.form_dialog.mainMenu()
		except KeyError as exception:
			self.utils.createTelkAlertToolLog("Key Error: " + str(exception), 3)
			self.form_dialog.d.msgbox(text = "\nFailed to update alert rule. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that allows creating the alert rule file with extension .yaml based on what was entered.

	Parameters:
	self -- An instantiated object of the Rules class.
	data_rule -- List with all the data entered for the alert rule.
	flag_telegram -- Flag that lets you know if the alert will be sent by telegram or not.
	flag_email -- Flag that lets you know if the alert will be sent by email or not.
	"""
	def createRuleYaml(self, data_alert_rule, flag_telegram, flag_email):
		data_json_alert_rule = {'name_rule' : data_alert_rule[0],
						  		'alert_level' : data_alert_rule[1],
						  		'index_name' : data_alert_rule[2],
						  		'type_alert' : data_alert_rule[3],
			  			  		'num_events' : int(data_alert_rule[4]),
						  		'time_search' : { data_alert_rule[5] : int(data_alert_rule[6]) },
		 				  		'time_range' : { data_alert_rule[7] : int(data_alert_rule[8]) },
						  		'query_type' : [{ data_alert_rule[9] : { 'query' : data_alert_rule[10] }}],
						  		'specific_fields_search' : data_alert_rule[11]}

		if data_alert_rule[11] == True:
			fields_name_json = { 'field_name' : data_alert_rule[12] }
			data_json_alert_rule.update(fields_name_json)
			last_index = 12
		else:
			last_index = 11
		custom_rule_json = { 'custom_rule' : data_alert_rule[last_index + 1] }
		if data_alert_rule[last_index + 1] == True:
			if data_alert_rule[last_index + 2] == True:
				restriction_hostname_json = { 'restriction_hostname' : data_alert_rule[last_index + 2], 'field_hostname' : data_alert_rule[last_index + 3], 'number_events_hostname' : int(data_alert_rule[last_index + 4]) }
				last_index += 3
			else:
				restriction_hostname_json = { 'restriction_hostname' : data_alert_rule[last_index + 2] }
				last_index += 1
			data_json_alert_rule.update(restriction_hostname_json)
			if data_alert_rule[last_index + 1] == True:
				restriction_username_json = { 'restriction_username' : data_alert_rule[last_index + 1], 'field_username' : data_alert_rule[last_index + 2], 'number_events_username' : int(data_alert_rule[last_index + 3]) }
				last_index += 3
			else:
				restriction_username_json = { 'restriction_username' : data_alert_rule[last_index + 1] }
				last_index += 1
			data_json_alert_rule.update(restriction_username_json)
		data_json_alert_rule.update(custom_rule_json)
		last_index += 1
		type_alert_send_json = { 'type_alert_send' : data_alert_rule[last_index + 1] }
		data_json_alert_rule.update(type_alert_send_json)
		last_index += 1
		if flag_telegram == 1 and flag_email == 0:
			alert_platform_json = { 'alert' : ['telegram'] }
			telegram_data_json = { 'telegram_bot_token' : data_alert_rule[last_index + 1], 'telegram_chat_id' : data_alert_rule[last_index + 2] }
			data_json_alert_rule.update(telegram_data_json)
		if flag_email == 1 and flag_telegram == 0:
			alert_platform_json = { 'alert' : ['email'] }
			email_data_json = { 'email_from' : data_alert_rule[last_index + 1], 'email_from_password' : data_alert_rule[last_index + 2], 'email_to' : data_alert_rule[last_index + 3] }
			data_json_alert_rule.update(email_data_json)
		if flag_telegram == 1 and flag_email == 1:
			alert_platform_json = { 'alert' : ['telegram', 'email'] }
			telegram_data_json = { 'telegram_bot_token' : data_alert_rule[last_index + 1], 'telegram_chat_id' : data_alert_rule[last_index + 2] }
			data_json_alert_rule.update(telegram_data_json)
			email_data_json = { 'email_from' : data_alert_rule[last_index + 3], 'email_from_password' : data_alert_rule[last_index + 4], 'email_to' : data_alert_rule[last_index + 5] }
			data_json_alert_rule.update(email_data_json)
		data_json_alert_rule.update(alert_platform_json)
		self.utils.createYamlFile(data_json_alert_rule, self.path_folder_rules + '/' + data_rule[0] + '.yaml', 'w')

	"""
	Method that removes the YAML file corresponding to a specific alert rule.

	Parameters:
	self -- An instantiated object of the Rules class.
	name_alert_rule -- Name of the rule to be removed.

	exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	"""
	def deleteAlertRule(self, name_alert_rule):
		try:
			remove(self.path_folder_rules + '/' + name_alert_rule)
		except OSError as exception:
			self.utils.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to delete alert rule. For more information see the logs.", height = 8, width = 50, title = "Error message")
			self.form_dialog.mainMenu()

	"""
	Method that gets a list with all the names of the alert rules stored in the rules directory.

	Parameters:
	self -- An instantiated object of the Rules class.

	Return:
	list_all_alert_rules -- List with the names of the alert rules stored in the directory.
	"""
	def getAllAlertRules(self):
		try:
			list_all_alert_rules = [path.basename(x) for x in glob(self.path_folder_rules + '/*.yaml')]
		except OSError as exception:
			self.utils.createTelkAlertToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to get alert rules. For more information, see the logs." , height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return list_all_alert_rules