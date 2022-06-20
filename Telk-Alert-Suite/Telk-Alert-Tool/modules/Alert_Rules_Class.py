from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related with the alert rules.
"""
class AlertRules:
	"""
	Attribute that stores an object of the libPyUtils class.
	"""
	__utils = None

	"""
	Attribute that stores an object of the libPyDialog class.
	"""
	__dialog = None

	"""
	Attribute that stores an object of the libPyLog class.
	"""
	__logger = None

	"""
	Attribute that stores an object of the Constants class.
	"""
	__constants = None

	"""
	Attribute that stores the method to be called when the user chooses the cancel option.
	"""
	__action_to_cancel = None

	"""
	Attribute that stores the absolute path of the folder where the alert rules are saved.
	"""
	__folder_alert_rules_path = None


	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel: Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)
		name_folder_rules = self.__utils.readYamlFile(self.__constants.PATH_FILE_CONFIGURATION)['name_folder_rules']
		self.__folder_alert_rules_path = self.__constants.PATH_BASE_TELK_ALERT + '/' + name_folder_rules


	def createNewAlertRule(self):
		"""
		Method that collects the information for the creation of the new alert rule.
		"""
		data_alert_rule = []
		try:
			alert_rule_name = self.__dialog.createFolderOrFileNameDialog("Enter the name of the alert rule:", 8, 50, "rule1")
			data_alert_rule.append(alert_rule_name)
			option_alert_rule_level = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_ALERT_RULE_LEVEL, "Alert Rule Level")
			data_alert_rule.append(option_alert_rule_level)
			index_pattern_name = self.__dialog.createInputBoxDialog("Enter the name of the index or index pattern where it will be searched:", 10, 50, "winlogbeat-*")
			data_alert_rule.append(index_pattern_name)
			option_alert_rule_type = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_ALERT_RULE_TYPE, "Alert Rule Type")
			data_alert_rule.append(option_alert_rule_type)
			if option_alert_rule_type == "Frequency":
				number_events_found_by_alert = self.__dialog.createInputBoxToNumberDialog("Enter the number of events found to which the alert is sent:", 10, 50, "1")
				data_alert_rule.append(number_events_found_by_alert)
				option_unit_time_search = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_UNIT_TIME, "Unit Time")
				data_alert_rule.append(option_unit_time_search)
				total_unit_time_search = self.__dialog.createInputBoxToNumberDialog("Enter the total in " + str(option_unit_time_search) + " in which you want the search to be repeated:", 10, 50, "1")
				data_alert_rule.append(total_unit_time_search)
				option_unit_time_range = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_UNIT_TIME, "Unit Time")
				data_alert_rule.append(option_unit_time_range)
				total_unit_time_range = self.__dialog.createInputBoxToNumberDialog("Enter the total in " + str(option_unit_time_range) + " that define the range in which the events to search should be found:", 10, 50, "1")
				data_alert_rule.append(total_unit_time_range)
			query_type = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_QUERY_TYPE, "Query Type")
			data_alert_rule.append(query_type)
			if query_type == "query_string":
				query_string = self.__dialog.createInputBoxDialog("Enter the query string:", 8, 50, "event.code: 4625")
				data_alert_rule.append(query_string)
			use_fields_option = self.__dialog.createYesOrNoDialog("\nDo you require to use the fields option for the search?", 8, 50, "Fields Option Search")
			if use_fields_option == "ok":
				data_alert_rule.append(True)
				number_of_fields_to_enter = self.__dialog.createInputBoxToNumberDialog("Enter the total of fields to be define:", 8, 50, "3")
				list_to_form_dialog = self.__utils.createListToDialogForm(int(number_of_fields_to_enter), "Field")
				list_all_fields = self.__dialog.createFormDialog("Enter the field's names:", list_to_form_dialog, 15, 50, "Fields Form")
				data_alert_rule.append(list_all_fields)
			else:
				data_alert_rule.append(False)
			use_custom_rule_option = self.__dialog.createYesOrNoDialog("\nDo you require to use the custom rule option?", 8, 50, "Custom Rule Option")
			if use_custom_rule_option == "ok":
				data_alert_rule.append(True)
				options_custom_rule_option = self.__dialog.createCheckListDialog("Select one or more options:", 10, 50, self.__constants.OPTIONS_CUSTOM_RULE, "Custom Rule Options")
				if "Hostname" in options_custom_rule_option:
					data_alert_rule.append(True)
					field_name_hostname = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the hostname:", 8, 50, "host.hostname")
					data_alert_rule.append(field_name_hostname)
					number_total_events_by_hostname = self.__dialog.createInputBoxToNumberDialog("Enter the total of events by hostname for the alert rule:", 8, 50, "5")
					data_alert_rule.append(number_total_events_by_hostname)
				else:
					data_alert_rule.append(False)
				if "Username" in options_custom_rule_option:
					data_alert_rule.append(True)
					field_name_username = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the username", 8, 50, "winlog.username")
					data_alert_rule.append(field_name_username)
					number_total_events_by_username = self.__dialog.createInputBoxToNumberDialog("Enter the total of events by username for the alert rule", 8, 50, "5")
					data_alert_rule.append(number_total_events_by_username)
				else:
					data_alert_rule.append(False)
			else:
				data_alert_rule.append(False)
			option_send_type_alert_rule = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_SEND_TYPE_ALERT, "Alert Sending Type Options")
			data_alert_rule.append(option_send_type_alert_rule)
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			data_alert_rule.append(telegram_bot_token.decode('utf-8'))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			data_alert_rule.append(telegram_chat_id.decode('utf-8'))
			self.__createFileYamlAlertRule(data_alert_rule)
			if path.exists(self.__folder_alert_rules_path + '/' + alert_rule_name + ".yaml"):
				self.__logger.generateApplicationLog("Alert rule created: " + alert_rule_name, 1, "__alertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
				self.__dialog.createMessageDialog("\nAlert rule created: " + alert_rule_name, 7, 50, "Notification Message")
			self.__action_to_cancel()
		except (OSError, IOError, FileNotFoundError, ValueError) as exception:
			self.__logger.generateApplicationLog(exception, 3, "__alertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__dialog.createMessageDialog("\nError creating the alert rule. For more information, see the logs.", 8, 50, "Error Message")
			self.__action_to_cancel()


	def modifyAlertRule(self):
		"""
		"""
		try:
			list_all_alert_rules = self.__utils.getListOfAllFilesYamlInFolder(self.__folder_alert_rules_path)
			if list_all_alert_rules:
				flag_rename_alert_rule = 0
				list_alert_rules_to_modify = self.__utils.convertListToDialogList(list_all_alert_rules, "Alert Rule")
				alert_rule_to_modify = self.__dialog.createRadioListDialog("Select a option:", 10, 50, list_alert_rules_to_modify, "Alert Rules")
				options_fields_to_update = self.__dialog.createCheckListDialog("Select one or more options:", 18, 70, self.__constants.OPTIONS_FIELDS_UPDATE_ALERT_RULE, "Fields")
				data_alert_rule = self.__utils.readYamlFile(self.__folder_alert_rules_path + '/' + alert_rule_to_modify)
				hash_alert_rule_actual = self.__utils.getHashFunctionToFile(self.__folder_alert_rules_path + '/' + alert_rule_to_modify)
				alert_rule_name_actual = data_alert_rule["alert_rule_name"]
				if "Name" in options_fields_to_update:
					alert_rule_name = self.__dialog.createFolderOrFileNameDialog("Enter the name of the alert rule:", 8, 50, data_alert_rule["alert_rule_name"])
					if not alert_rule_name == data_alert_rule["alert_rule_name"]:
						flag_rename_alert_rule = 1
						data_alert_rule["alert_rule_name"] = alert_rule_name
				if "Level" in options_fields_to_update:
					for level_option in self.__constants.OPTIONS_ALERT_RULE_LEVEL:
						if level_option[0] == data_alert_rule["alert_rule_level"]:
							level_option[2] = 1
						else:
							level_option[2] = 0
					option_alert_rule_level = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_ALERT_RULE_LEVEL, "Alert Rule Level")
					data_alert_rule["alert_rule_level"] = option_alert_rule_level
				if "Index" in options_fields_to_update:
					index_pattern_name = self.__dialog.createInputBoxDialog("Enter the name of the index or index pattern where it will be searched:", 10, 50, data_alert_rule["index_pattern_name"])
					data_alert_rule["index_pattern_name"] = index_pattern_name
				if "Number Events" in options_fields_to_update:
					number_events_found_by_alert = self.__dialog.createInputBoxToNumberDialog("Enter the number of events found to which the alert is sent:", 10, 50, str(data_alert_rule["number_events_found_by_alert"]))
					data_alert_rule["number_events_found_by_alert"] = int(number_events_found_by_alert)
				if "Time Search" in options_fields_to_update:
					for number_unit_time in data_alert_rule["time_search"]:
						number_unit_time_search_actual = number_unit_time
					for unit_time in self.__constants.OPTIONS_UNIT_TIME:
						if unit_time[0] == number_unit_time_search_actual:
							unit_time[2] = 1
						else:
							unit_time[2] = 0
					option_unit_time_search = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_UNIT_TIME, "Unit Time")
					total_unit_time_search = self.__dialog.createInputBoxToNumberDialog("Enter the total in " + str(option_unit_time_search) + " in which you want the search to be repeated:", 10, 50, str(data_alert_rule["time_search"][number_unit_time_search_actual]))
					data_alert_rule["time_search"] = {option_unit_time_search : int(total_unit_time_search)}
				if "Time Range" in options_fields_to_update:
					for number_unit_time in data_alert_rule["time_range"]:
						number_unit_time_range_actual = number_unit_time
					for unit_time in self.__constants.OPTIONS_UNIT_TIME:
						if unit_time[0] == number_unit_time_range_actual:
							unit_time[2] = 1
						else:
							unit_time[2] = 0
					option_unit_time_range = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_UNIT_TIME, "Unit Time")
					total_unit_time_range = self.__dialog.createInputBoxToNumberDialog("Enter the total in " + str(option_unit_time_range) + " that define the range in which the events to search should be found:", 10, 50, str(data_alert_rule["time_range"][number_unit_time_range_actual]))
					data_alert_rule["time_range"] = {option_unit_time_range : int(total_unit_time_range)}
				if "Query String" in options_fields_to_update:
					query_string = self.__dialog.createInputBoxDialog("Enter the query string:", 8, 50, data_alert_rule['query_type'][0]['query_string']['query'])
					data_alert_rule["query_type"] = [{'query_string' : {'query' : query_string}}]
				#if "Fields Option" in options_fields_to_update:
				#	if data_alert_rule["use_fields_option"] == True:		
				self.__utils.createYamlFile(data_alert_rule, self.__folder_alert_rules_path + '/' + alert_rule_to_modify)
				hash_alert_rule_new = self.__utils.getHashFunctionToFile(self.__folder_alert_rules_path + '/' + alert_rule_to_modify)
				if hash_alert_rule_new == hash_alert_rule_actual:
					self.__dialog.createMessageDialog("\nAlert rule not modified: " + alert_rule_to_modify, 8, 50, "Notification Message")
				else:
					self.__logger.createApplicationLog("Alert rule modified: " + alert_rule_to_modify, 2)
					self.__dialog.createMessageDialog("\nAlert rule modified: " + alert_rule_to_modify, 8, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
			self.__action_to_cancel()
		except KeyError as exception:
			self.__logger.createApplicationLog("Key Error: " + str(exception), 3)
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__action_to_cancel()
		except (OSError, FileNotFoundError, IOError) as exception:
			self.__logger.createApplicationLog(exception, 3)
			self.__dialog.createMessageDialog("\nError to modify the alert rule. For more information, see the logs.", 8, 50, "Error Message")
			self.__action_to_cancel()


	def deleteAlertRules(self):
		"""
		Method that delete one or more alert rules.
		"""
		try:
			list_all_alert_rules = self.__utils.getListOfAllYamlFilesInFolder(self.__folder_alert_rules_path)
			if list_all_alert_rules:
				list_alert_rules_to_delete = self.__utils.convertListToDialogList(list_all_alert_rules, "Alert Rule")
				alert_rules_to_delete= self.__dialog.createCheckListDialog("Select one or more options:", 10, 50, list_alert_rules_to_delete, "Alert Rules")
				confirmation_delete_alert_rules = self.__dialog.createYesOrNoDialog("\nAre you sure to delete the following alert rules?\n\n** This action cannot be undone.", 10, 50, "Delete Alert Rules")
				if confirmation_delete_alert_rules == "ok":
					message_to_display = "\nAlert rules removed:\n"
					for alert_rule in alert_rules_to_delete:
						self.__utils.deleteFile(self.__folder_alert_rules_path + '/' + alert_rule)
						message_to_display += "\n- " + alert_rule
					self.__dialog.createScrollBoxDialog(message_to_display, 14, 50, "Delete Alert Rules")
			else:
				self.__dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
			self.__action_to_cancel()
		except (OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nError to delete one or more alert rules. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__deleteAlertRules", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()


	def __createFileYamlAlertRule(self, data_alert_rule):
		"""
		Method that creates the YAML file corresponding to the new alert rule.

		:arg data_alert_rule: Object containing the data defined for the new alert rule.
		"""
		data_alert_rule_json = {'alert_rule_name' : data_alert_rule[0],
								'alert_rule_level' : data_alert_rule[1],
								'index_pattern_name' : data_alert_rule[2],
								'alert_rule_type' : data_alert_rule[3],
								'number_events_found_by_alert' : int(data_alert_rule[4]),
								'time_search' : {data_alert_rule[5] : int(data_alert_rule[6])},
								'time_range' : {data_alert_rule[7] : int(data_alert_rule[8])},
								'query_type' : [{data_alert_rule[9] : {'query' : data_alert_rule[10]}}],
								'use_fields_option' : data_alert_rule[11]}

		if data_alert_rule[11] == True:
			fields_name_json = {'fields_name' : data_alert_rule[12]}
			data_alert_rule_json.update(fields_name_json)
			last_index = 12
		else:
			last_index = 11
		if data_alert_rule[last_index + 1] == True:
			if data_alert_rule[last_index + 2] == True:
				restriction_by_hostname_json = {'restriction_by_hostname' : data_alert_rule[last_index + 2], 'field_name_hostname' : data_alert_rule[last_index + 3], 'number_total_events_by_hostname' : int(data_alert_rule[last_index + 4])}
				last_index += 4
			else:
				restriction_by_hostname_json = {'restriction_by_hostname' : data_alert_rule[last_index + 2]}
				last_index += 2
			data_alert_rule_json.update(restriction_by_hostname_json)
			if data_alert_rule[last_index + 1] == True:
				restriction_by_username_json = {'restriction_by_username' : data_alert_rule[last_index + 1], 'field_name_username' : data_alert_rule[last_index + 2], 'number_total_events_by_username' : int(data_alert_rule[last_index + 3])}
				last_index += 3
			else:
				restriction_by_username_json = {'restriction_by_username' : data_alert_rule[last_index + 1]}
				last_index += 1
			data_alert_rule_json.update(restriction_by_username_json)
			use_custom_rule_json = {'use_custom_rule_option' : True}
		else:
			use_custom_rule_json = {'use_custom_rule_option' : False}
			last_index += 1
		data_alert_rule_json.update(use_custom_rule_json)
		aux_data_json = {'send_type_alert_rule' : data_alert_rule[last_index + 1], 'telegram_bot_token' : data_alert_rule[last_index + 2], 'telegram_chat_id' : data_alert_rule[last_index + 3]}
		data_alert_rule_json.update(aux_data_json)

		self.__utils.createYamlFile(data_alert_rule_json, self.__folder_alert_rules_path + '/' + data_alert_rule[0] + ".yaml")
		self.__utils.changeOwnerToPath(self.__folder_alert_rules_path + '/' + data_alert_rule[0] + ".yaml", self.__constants.USER, self.__constants.GROUP)