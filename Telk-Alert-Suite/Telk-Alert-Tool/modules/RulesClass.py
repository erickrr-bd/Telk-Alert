from glob import glob
from os import path, remove, rename
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

		list_custom_rule = [("Hostname", "Restrict by hostname", 0),
							   ("Username", "Restrict by username", 0)]

		data_rule = []
		name_rule = self.form_dialog.getDataNameFolderOrFile("Enter the name of the alert rule:", "rule1")
		data_rule.append(name_rule)
		option_level_alert = self.form_dialog.getDataRadioList("Select a option:", self.list_level_alert, "Alert Rule Level")
		data_rule.append(option_level_alert)
		index_name = self.form_dialog.getDataInputText("Enter the index pattern where the searches will be made:", "winlogbeat-*")
		data_rule.append(index_name)
		option_type_rule = self.form_dialog.getDataRadioList("Select a option:", list_type_alert, "Alert Rule Type")
		data_rule.append(option_type_rule)
		if option_type_rule == "Frequency":
			number_events = self.form_dialog.getDataNumber("Enter the number of events found in the rule to send the alert to:", "1")
			data_rule.append(number_events)
			option_unit_time_search = self.form_dialog.getDataRadioList("Select a option:", self.list_unit_time, "Search Time Unit")
			data_rule.append(option_unit_time_search)
			number_unit_time_search = self.form_dialog.getDataNumber("Enter the total amount in " + str(option_unit_time_search) + " in which you want the search to be repeated:", "2")
			data_rule.append(number_unit_time_search)
			option_unit_time_range = self.form_dialog.getDataRadioList("Select a option:", self.list_unit_time, "Time Unit")
			data_rule.append(option_unit_time_range)
			number_unit_time_range = self.form_dialog.getDataNumber("Enter the total in " + str(option_unit_time_range) + " that define the range in which the events to search should be found:", "2")
			data_rule.append(number_unit_time_range)
		query_type = self.form_dialog.getDataRadioList("Select a option:", list_query_type, "Query Type")
		data_rule.append(query_type)
		if query_type == "query_string":
			query_string = self.form_dialog.getDataInputText("Enter the query string:", "event.code : 4120")
			data_rule.append(query_string)
		specific_fields_search = self.form_dialog.getDataYesOrNo("\nDo you require that the search only return certain fields?", "Specific Fields In Search")
		if specific_fields_search == "ok":
			data_rule.append(True)
			total_fields_to_enter = self.form_dialog.getDataNumber("Enter the total number of field names to be defined:", "2")
			list_to_fields = self.utils.generateListToForm(int(total_fields_to_enter), "Field")
			list_fields_names = self.form_dialog.getForm("Enter the name of the fields:", list_to_fields, "Field Names", 1)
			data_rule.append(list_fields_names)
		else:
			data_rule.append(False)
		is_custom_rule = self.form_dialog.getDataYesOrNo("\nDo you need to create a custom alert rule?", "Custom Rule")
		if is_custom_rule == "ok":
			data_rule.append(True)
			flag_hostname = 0
			flag_username = 0
			options_custom_rule = self.form_dialog.getDataCheckList("Select one or more options:", list_custom_rule, "Custom Rule")
			for option in options_custom_rule:
				if option == "Hostname":
					flag_hostname = 1
				elif option == "Username":
					flag_username = 1
			if flag_hostname == 1:
				data_rule.append(True)
				field_name_hostname = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the hostname:", "host.hostname")
				data_rule.append(field_name_hostname)
				number_events_hostname = self.form_dialog.getDataNumber("Enter the number of events per hostname to which the alert will be sent:", "3")
				data_rule.append(number_events_hostname)
			else:
				data_rule.append(False)
			if flag_username == 1:
				data_rule.append(True)
				field_name_username = self.form_dialog.getDataInputText("Enter the name of the field in the index that corresponds to the username:", "winlog.username")
				data_rule.append(field_name_username)
				number_events_username = self.form_dialog.getDataNumber("Enter the number of events per username to which the alert will be sent:", "3")
				data_rule.append(number_events_username)
			else:
				data_rule.append(False)
		else:
			data_rule.append(False)
		option_type_alert_send = self.form_dialog.getDataRadioList("Select a option:", self.list_type_alert_send, "Alert Sending Type")
		data_rule.append(option_type_alert_send)
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
			data_rule.append(telegram_bot_token.decode('utf-8'))
			telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
			data_rule.append(telegram_chat_id.decode('utf-8'))
		if flag_email == 1:
			email_from = self.form_dialog.getDataEmail("Enter the email address from which the alerts will be sent (gmail or outlook):", "usuario@gmail.com")
			data_rule.append(email_from)
			email_from_password = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"))
			data_rule.append(email_from_password.decode('utf-8'))
			total_emails_to_enter = self.form_dialog.getDataNumber("Enter the total number of email address to be defined:", "3")
			list_to_emails = self.utils.generateListToForm(int(total_emails_to_enter), "Email")
			list_email_address = self.form_dialog.getForm("Enter the email addresses:", list_to_emails, "Email Addresses", 2)
			data_rule.append(list_email_address)
		self.createRuleYaml(data_rule, flag_telegram, flag_email)
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
							  ("Specific Fields", "Enables or disables the use of specific fields in the alert", 0),
							  ("Custom Rule", "Enable or disable the use of custom rule", 0),
							  ("Shipping Type", "How the alert will be sent", 0),
							  ("Platforms", "Alerts sending platforms", 0)]

		list_specific_fields_false = [("Enable", "Enables the use of specific fields", 0)]

		list_specific_fields_true = [("Disable", "Disable the use of specific fields", 0),
								     ("Data", "Modify configured data", 0)]

		list_specific_fields_update = [("1", "Add New Field(s)"),
									   ("2", "Modify Field(s)"),
									   ("3", "Remove Field(s)")]

		options_rest_host_false = [("Enable", "Enable restriction by host", 0)]

		options_rest_host_true = [("To Disable", "Disable restriction by host", 0),
								 ("Modify Data", "Modify existing data", 0)]

		options_rest_host_modify = [("Number of Events", "Number of events per host", 0),
									("Field", "Host name field", 0)]

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
				num_time_search = self.form_dialog.getDataNumber("Enter the total amount in " + str(unit_time_search) + " in which you want the search to be repeated:", str(data_rule['time_search'][num_time_search_actual]))
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
						list_specific_fields_definied = data_rule['field_name']
						option_specific_fields_update = self.form_dialog.getMenu("Select a option:", list_specific_fields_update, "Actions To Perform")
						if int(option_specific_fields_update) == 1:
							total_fields_to_enter = self.form_dialog.getDataNumber("Enter the total number of field names to be add:", "2")
							list_to_fields = self.utils.generateListToForm(int(total_fields_to_enter), "Field")
							list_fields_names = self.form_dialog.getForm("Enter the name of the fields:", list_to_fields, "Field Names", 1)
							list_specific_fields_definied.extend(list_fields_names)
							data_rule['field_name'] = list_specific_fields_definied
						elif int(option_specific_fields_update) == 2:
							list_convert_to_form = self.utils.convertListToForm("Field", list_specific_fields_definied)
							list_fields_names = self.form_dialog.getForm("Enter the name of the fields:", list_convert_to_form, "Field Names", 1)
							data_rule['field_name'] = list_fields_names
						elif int(option_specific_fields_update) == 3:
							list_specific_fields = self.utils.convertListToCheckOrRadioList(list_specific_fields_definied, "Field")
							options_specific_fields = self.form_dialog.getDataCheckList("Select one or more options:", list_specific_fields, "Fields Names")
							for option in options_specific_fields:
								list_specific_fields_definied.remove(option)
							data_rule['field_name'] = list_specific_fields_definied
				else:
					option_specific_fields_false = self.form_dialog.getDataRadioList("Select a option:", list_specific_fields_false, "Use Of Specific Fields")
					if option_specific_fields_false == "Enable":
						data_rule['specific_fields_search'] = True
						total_fields_to_enter = self.form_dialog.getDataNumber("Enter the total number of field names to be defined:", "2")
						list_to_fields = self.utils.generateListToForm(int(total_fields_to_enter), "Field")
						list_fields_names = self.form_dialog.getForm("Enter the name of the fields:", list_to_fields, "Field Names", 1)
						fields_name_json = { 'field_name' : list_fields_names }
						data_rule.update(fields_name_json)
			"""
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
					if opt_rest_field_true == "Modify Data":
						opt_rest_field_modify = form_dialog.getDataRadioList("Select a option:", options_rest_field_modify, "Field Restriction")
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
						field_hostname = form_dialog.getDataInputText("Enter the name of the field that contains the hostname:", "host.hostname")
						data_rule['restrict_by_host'] = True
						restriction_host_json = { 'number_events_host' : int(number_events_hostname), 'field_hostname' : str(field_hostname) }
						data_rule.update(restriction_host_json)
				else:
					opt_rest_host_true = form_dialog.getDataRadioList("Select a option:", options_rest_host_true, "Restriction By Host")
					if opt_rest_host_true == "To Disable":
						del data_rule['number_events_host']
						del data_rule['field_hostname']
						data_rule['restrict_by_host'] = False
					if opt_rest_host_true == "Modify Data":
						opt_rest_host_modify = form_dialog.getDataRadioList("Select a option:", options_rest_host_modify, "Restriction By Host")
						if opt_rest_host_modify == "Number of Events":
							number_events_hostname = form_dialog.getDataNumber("Enter the total number of events per hostname to which the alert will be sent:", str(data_rule['number_events_host']))
							data_rule['number_events_host'] = int(number_events_hostname)
						if opt_rest_host_modify == "Field":
							field_hostname = form_dialog.getDataInputText("Enter the name of the field that contains the hostname:", data_rule['field_hostname'])
							data_rule['field_hostname'] = field_hostname
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
								telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", self.utils.decryptAES(data_rule['telegram_bot_token'], form_dialog).decode('utf-8')), form_dialog)
								data_rule['telegram_bot_token'] = telegram_bot_token.decode('utf-8')
							if flag_chat_id == 1:
								telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", self.utils.decryptAES(data_rule['telegram_chat_id'], form_dialog).decode('utf-8')), form_dialog)
								data_rule['telegram_chat_id'] = telegram_chat_id.decode('utf-8')
					else:
						opt_telegram_false = form_dialog.getDataRadioList("Select a option:", options_telegram_false, "Sending By Telegram")
						if opt_telegram_false == "Enable":
							del data_rule['alert']
							telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), form_dialog)
							telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"), form_dialog)
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
								email_from_password = self.utils.encryptAES(form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"), form_dialog)
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
							email_from_password = self.utils.encryptAES(form_dialog.getDataPassword("Enter the password of the email address from which the alerts will be sent:", "password"), form_dialog)
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
			"""
			self.utils.createYamlFile(data_rule, self.path_folder_rules + '/' + name_alert_rule, 'w')
			hash_file_new = self.utils.getHashToFile(self.path_folder_rules + '/' + name_alert_rule)
			if hash_file_actual == hash_file_new:
				self.form_dialog.d.msgbox(text = "\nAlert rule not modified: " + name_alert_rule, height = 7, width = 50, title = "Notification message")
			else:
				self.utils.createTelkAlertToolLog("Modified alert rule: " + name_alert_rule, 2)
				self.form_dialog.d.msgbox(text = "\nModified alert rule: " + name_alert_rule, height = 7, width = 50, title = "Notification Message")
			if flag_name_rename == 1:
				rename(self.path_folder_rules + '/' + name_rule_actual + ".yaml", self.path_folder_rules + '/' + name_rule + ".yaml")	
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
	def createRuleYaml(self, data_rule, flag_telegram, flag_email):
		data_json_rule = {'name_rule' : data_rule[0],
						  'alert_level' : data_rule[1],
						  'index_name' : data_rule[2],
						  'type_alert' : data_rule[3],
			  			  'num_events' : int(data_rule[4]),
						  'time_search' : { data_rule[5] : int(data_rule[6]) },
		 				  'time_range' : { data_rule[7] : int(data_rule[8]) },
						  'query_type' : [{ data_rule[9] : { 'query' : data_rule[10] }}],
						  'specific_fields_search' : data_rule[11]}

		if data_rule[11] == True:
			fields_name_json = { 'field_name' : data_rule[12] }
			data_json_rule.update(fields_name_json)
			last_index = 12
		else:
			last_index = 11
		custom_rule_json = { 'custom_rule' : data_rule[last_index + 1] }
		if data_rule[last_index + 1] == True:
			data_json_rule.update(custom_rule_json)
			if data_rule[last_index + 2] == True:
				restriction_hostname_json = { 'restriction_hostname' : data_rule[last_index + 2], 'field_hostname' : data_rule[last_index + 3], 'number_events_hostname' : int(data_rule[last_index + 4]) }
				last_index += 3
			else:
				restriction_hostname_json = { 'restriction_hostname' : data_rule[last_index + 2] }
				last_index += 1
			data_json_rule.update(restriction_hostname_json)
			if data_rule[last_index + 1] == True:
				restriction_username_json = { 'restriction_username' : data_rule[last_index + 1], 'field_username' : data_rule[last_index + 2], 'number_events_username' : int(data_rule[last_index + 3]) }
				last_index += 3
			else:
				restriction_username_json = { 'restriction_username' : data_rule[last_index + 1] }
				last_index += 1
			data_json_rule.update(restriction_username_json)
		last_index += 1
		type_alert_send_json = { 'type_alert_send' : data_rule[last_index + 1] }
		data_json_rule.update(type_alert_send_json)
		last_index += 1
		if flag_telegram == 1 and flag_email == 0:
			alert_platform_json = { 'alert' : ['telegram'] }
			telegram_data_json = { 'telegram_bot_token' : data_rule[last_index + 1], 'telegram_chat_id' : data_rule[last_index + 2] }
			data_json_rule.update(telegram_data_json)
		if flag_email == 1 and flag_telegram == 0:
			alert_platform_json = { 'alert' : ['email'] }
			email_data_json = { 'email_from' : data_rule[last_index + 1], 'email_from_password' : data_rule[last_index + 2], 'email_to' : data_rule[last_index + 3] }
			data_json_rule.update(email_data_json)
		if flag_telegram == 1 and flag_email == 1:
			alert_platform_json = { 'alert' : ['telegram', 'email'] }
			telegram_data_json = { 'telegram_bot_token' : data_rule[last_index + 1], 'telegram_chat_id' : data_rule[last_index + 2] }
			data_json_rule.update(telegram_data_json)
			email_data_json = { 'email_from' : data_rule[last_index + 3], 'email_from_password' : data_rule[last_index + 4], 'email_to' : data_rule[last_index + 5] }
			data_json_rule.update(email_data_json)
		data_json_rule.update(alert_platform_json)
		self.utils.createYamlFile(data_json_rule, self.path_folder_rules + '/' + data_rule[0] + '.yaml', 'w')

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