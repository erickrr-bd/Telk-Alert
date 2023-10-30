from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages alert rules.
"""
class AlertRules:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)
		alert_rules_folder = self.utils.readYamlFile(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)["alert_rules_folder"]
		self.alert_rules_folder_path = self.constants.TELK_ALERT_PATH + '/' + alert_rules_folder


	def create_alert_rule(self):
		"""
		Method that creates an alert rule.
		"""
		try:
			alert_rule_data = []
			alert_rule_name = self.dialog.createFolderOrFileNameDialog("Enter the name of the alert rule:", 8, 50, "rule1")
			alert_rule_data.append(alert_rule_name)
			option_alert_rule_level = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_ALERT_RULE_LEVEL, "Alert Rule Level")
			alert_rule_data.append(option_alert_rule_level)
			index_pattern = self.dialog.createInputBoxDialog("Enter the index pattern:", 8, 50, "winlogbeat-*")
			alert_rule_data.append(index_pattern)
			option_alert_rule_type = self.dialog.createRadioListDialog("Select a option:", 8, 50, self.constants.OPTIONS_ALERT_RULE_TYPE, "Alert Rule Type")
			alert_rule_data.append(option_alert_rule_type)
			if option_alert_rule_type == "Frequency":
				total_number_events = self.dialog.createInputBoxToNumberDialog("Enter the total number of events to which the alert will be sent:", 9, 50, "1")
				alert_rule_data.append(total_number_events)
				option_unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
				alert_rule_data.append(option_unit_time)
				unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + option_unit_time + " that the search will be repeated:", 9, 50, "1")
				alert_rule_data.append(unit_time_total)
				option_unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
				size = 9 if option_unit_time == "minutes" else 8
				alert_rule_data.append(option_unit_time)
				unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + option_unit_time + " of the search range:", size, 50, "1")
				alert_rule_data.append(unit_time_total)
				option_query_type = self.dialog.createRadioListDialog("Select a option:", 8, 70, self.constants.OPTIONS_QUERY_TYPE, "Query Type")
				alert_rule_data.append(option_query_type)
				if option_query_type == "query_string":
					query_string = self.dialog.createInputBoxDialog("Enter the query string:", 8, 50, "event.code: 4625")
					alert_rule_data.append(query_string)
					use_fields_selection = self.dialog.createYesOrNoDialog("\nIs the selection of certain fields required for the search?", 8, 50, "Fields Selection")
					if use_fields_selection == "ok":
						alert_rule_data.append(True)
						total_fields = self.dialog.createInputBoxToNumberDialog("Enter the total fields:", 8, 50, "3")
						list_form = self.utils.createListToDialogForm(int(total_fields), "Field name")
						fields_list = self.dialog.createFormDialog("Enter the field's names:", list_form, 15 ,50, "Fields Form", False)
						alert_rule_data.append(fields_list)
					else:
						alert_rule_data.append(False)
					use_custom_search = self.dialog.createYesOrNoDialog("\nIs the use of a custom search required?", 7, 50, "Custom Search")
					if use_custom_search == "ok":
						alert_rule_data.append(True)
						options_custom_search = self.dialog.createCheckListDialog("Select one or more options:", 9, 50, self.constants.OPTIONS_CUSTOM_SEARCH, "Custom Search")
						if "Hostname" in options_custom_search:
							alert_rule_data.append(True)
							field_name_hostname = self.dialog.createInputBoxDialog("Enter the field name for the hostname:", 8, 50, "host.hostname")
							alert_rule_data.append(field_name_hostname)
							total_events_by_hostname = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by hostname:", 8, 50, "5")
							alert_rule_data.append(total_events_by_hostname)
						else:
							alert_rule_data.append(False)
						if "Username" in options_custom_search:
							alert_rule_data.append(True)
							field_name_username = self.dialog.createInputBoxDialog("Enter the field name for the username:", 8, 50, "user.name")
							alert_rule_data.append(field_name_username)
							total_events_by_username = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by username:", 8, 50, "5")
							alert_rule_data.append(total_events_by_username)
						else:
							alert_rule_data.append(False)
					else:
						alert_rule_data.append(False)
				option_alert_delivery_type = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_ALERT_DELIVERY_TYPE, "Alert Delivery Type")
				alert_rule_data.append(option_alert_delivery_type)
				passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
				telegram_bot_token = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
				alert_rule_data.append(telegram_bot_token)
				telegram_chat_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
				alert_rule_data.append(telegram_chat_id)
			self.create_yaml_file(alert_rule_data)
			if path.exists(self.alert_rules_folder_path + '/' + alert_rule_name + ".yaml"):
				self.dialog.createMessageDialog("\nAlert rule created: " + alert_rule_name, 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Alert rule created: " + alert_rule_name, 1, "__createAlertRule", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.createMessageDialog("\nError creating the alert rule.For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__createAlertRule", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def update_alert_rule(self):
		"""
		Method that updates one or more values of an alert rule.
		"""
		try:
			alert_rules_list = self.utils.getListYamlFilesInFolder(self.alert_rules_folder_path)
			if alert_rules_list:
				list_checklist_radiolist = self.utils.convertListToDialogList(alert_rules_list, "Alert rule name")
				option_alert_rule_update =self.dialog.createRadioListDialog("Select a option:", 18, 70, list_checklist_radiolist, "Alert Rules")
				options_alert_rule_update = self.dialog.createCheckListDialog("Select one or more options:", 19, 70, self.constants.OPTIONS_ALERT_RULE_UPDATE, "Alert Rule Fields")
				alert_rule_path = self.alert_rules_folder_path + '/' + option_alert_rule_update
				alert_rule_data = self.utils.readYamlFile(alert_rule_path)
				file_hash_original = self.utils.getHashFunctionOfFile(alert_rule_path)
				if "Name" in options_alert_rule_update:
					self.update_alert_rule_name(alert_rule_data)
				if "Level" in options_alert_rule_update:
					self.update_alert_rule_level(alert_rule_data)
				if "Index" in options_alert_rule_update:
					self.update_index_pattern(alert_rule_data)
				if "Total Events" in options_alert_rule_update:
					self.update_total_number_events(alert_rule_data)
				if "Search Time" in options_alert_rule_update:
					self.update_search_time(alert_rule_data)
				if "Range Time" in options_alert_rule_update:
					self.update_range_time(alert_rule_data)
				if "Query" in options_alert_rule_update:
					self.update_query_type(alert_rule_data)
				if "Fields Selection" in options_alert_rule_update:
					self.update_fields_selection(alert_rule_data)
				if "Custom Search" in options_alert_rule_update:
					self.update_custom_search(alert_rule_data)
				if "Delivery" in options_alert_rule_update:
					self.update_alert_delivery_type(alert_rule_data)
				if "Bot Token" in options_alert_rule_update:
					self.update_telegram_bot_token(alert_rule_data)
				if "Chat ID" in options_alert_rule_update:
					self.update_telegram_chat_id(alert_rule_data)
				alert_rule_new_path = self.alert_rules_folder_path + '/' + alert_rule_data["alert_rule_name"] + ".yaml"
				self.utils.createYamlFile(alert_rule_data, alert_rule_new_path)
				files_hash_new = self.utils.getHashFunctionOfFile(alert_rule_new_path)
				if file_hash_original == files_hash_new:
					self.dialog.createMessageDialog("\nAlert rule wasn't updated: " + alert_rule_data["alert_rule_name"], 7, 50, "Notification Message")
				else:
					self.dialog.createMessageDialog("\nAlert rule was updated: " + alert_rule_data["alert_rule_name"], 7, 50, "Notification Message")
					self.logger.generateApplicationLog("Alert rule was updated: " + alert_rule_data["alert_rule_name"], 2, "__updateAlertRule", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
			else:
				self.dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.createMessageDialog("\nError updating alert rule. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__updateAlertRule", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def display_alert_rule(self):
		"""
		Method that displays the data of an alert rule.
		"""
		try:
			alert_rules_list = self.utils.getListYamlFilesInFolder(self.alert_rules_folder_path)
			if alert_rules_list:
				list_checklist_radiolist = self.utils.convertListToDialogList(alert_rules_list, "Alert rule name")
				option_alert_rule =self.dialog.createRadioListDialog("Select a option:", 18, 70, list_checklist_radiolist, "Alert Rules")
				yaml_file_data = self.utils.convertYamlFileToString(self.alert_rules_folder_path + '/' + option_alert_rule)
				message_to_display = '\n' + option_alert_rule[:-5] + "\n\n" + yaml_file_data
				self.dialog.createScrollBoxDialog(message_to_display, 18, 70, "Alert Rule Data")
			else:
				self.dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.createMessageDialog("\nError displaying the alert rule data. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__displayAlertRule", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def remove_alert_rules(self):
		"""
		Method that removes one or more alert rules.
		"""
		try:
			alert_rules_list = self.utils.getListYamlFilesInFolder(self.alert_rules_folder_path)
			if alert_rules_list:
				list_checklist_radiolist = self.utils.convertListToDialogList(alert_rules_list, "Alert rule name")
				options_alert_rule = self.dialog.createCheckListDialog("Select one or more options:", 18, 70, list_checklist_radiolist, "Remove Alert Rules")
				message_to_display = self.utils.getStringFromList(options_alert_rule, "Alert rules selected to remove:")
				self.dialog.createScrollBoxDialog(message_to_display, 14, 50, "Remove Alert Rules")
				yes_no_remove = self.dialog.createYesOrNoDialog("\nAre you sure to remove the selected alert rules?\n\n** This action cannot be undone.", 10, 50, "Remove Alert Rules")
				if yes_no_remove == "ok":
					[self.utils.deleteFile(self.alert_rules_folder_path + '/' + item) for item in options_alert_rule]
					self.dialog.createMessageDialog("\nAlert rules removed.", 7, 50, "Notification Message")
			else:
				self.dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.createMessageDialog("\nError removing one or more alert rules. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__removeAlertRule", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def display_all_alert_rules(self):
		"""
		"""
		try:
			alert_rules_list = self.utils.getListYamlFilesInFolder(self.alert_rules_folder_path)
			if alert_rules_list:
				alert_rules_list.sort()
				message_to_display = "\nAlert rules:\n"
				for alert_rule in alert_rules_list:
					message_to_display += "\n- " + alert_rule[:-5]
				self.dialog.createScrollBoxDialog(message_to_display, 18, 70, "Alert Rules")
			else:
				self.dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.createMessageDialog("\nError displaying all alert rules. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__displayAllAlertRules", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def create_yaml_file(self, alert_rule_data):
		"""
		Method that creates the YAML file corresponding to the new alert rule.

		:arg alert_rule_data (list): List with the data that will be stored in the YAML file.
		"""
		alert_rule_data_json = {
			"alert_rule_name" : alert_rule_data[0],
			"alert_rule_level" : alert_rule_data[1],
			"index_pattern" : alert_rule_data[2],
			"alert_rule_type" : alert_rule_data[3],
			"total_number_events" : int(alert_rule_data[4]),
			"search_time" : {alert_rule_data[5] : int(alert_rule_data[6])},
			"range_time" : {alert_rule_data[7] : int(alert_rule_data[8])}
		}

		if alert_rule_data[9] == "query_string":
			alert_rule_data_json.update({"query_type" : [{alert_rule_data[9] : {"query" : alert_rule_data[10]}}]})
			alert_rule_data_json.update({"use_fields_selection" : alert_rule_data[11]})
			if alert_rule_data[11]:
				alert_rule_data_json.update({"fields_name" : alert_rule_data[12]})
				last_index = 12
			else:
				last_index = 11
			alert_rule_data_json.update({"use_custom_search" : alert_rule_data[last_index + 1]})
			if alert_rule_data[last_index + 1]:
				del alert_rule_data_json["total_number_events"]
				alert_rule_data_json.update({"restriction_by_hostname" : alert_rule_data[last_index + 2]})
				if alert_rule_data[last_index + 2]:
					alert_rule_data_json.update({"field_name_hostname" : alert_rule_data[last_index + 3], "total_events_by_hostname" : int(alert_rule_data[last_index + 4])})
					last_index += 4
				else:
					last_index += 2
				alert_rule_data_json.update({"restriction_by_username" : alert_rule_data[last_index + 1]})
				if alert_rule_data[last_index + 1]:
					alert_rule_data_json.update({"field_name_username" : alert_rule_data[last_index + 2], "total_events_by_username" : int(alert_rule_data[last_index + 3])})
					last_index += 3
				else:
					last_index += 1
			else:
				last_index += 1
			alert_rule_data_json.update({"alert_delivery_type" : alert_rule_data[last_index + 1], "telegram_bot_token" : alert_rule_data[last_index + 2], "telegram_chat_id" : alert_rule_data[last_index + 3]})

		alert_rule_path = self.alert_rules_folder_path + '/' + alert_rule_data[0] + ".yaml"
		self.utils.createYamlFile(alert_rule_data_json, alert_rule_path)
		self.utils.changeFileFolderOwner(alert_rule_path, self.constants.USER, self.constants.GROUP, "640")


	def update_alert_rule_name(self, alert_rule_data):
		"""
		Method that updates the name of the alert rule.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		alert_rule_name = self.dialog.createFolderOrFileNameDialog("Enter the name of the alert rule:", 8, 50, alert_rule_data["alert_rule_name"])
		if not alert_rule_data["alert_rule_name"] == alert_rule_name:
			self.utils.renameFileOrFolder(self.alert_rules_folder_path + '/' + alert_rule_data["alert_rule_name"] + ".yaml", self.alert_rules_folder_path + '/' + alert_rule_name + ".yaml")
			alert_rule_data["alert_rule_name"] = alert_rule_name
		return alert_rule_data


	def update_alert_rule_level(self, alert_rule_data):
		"""
		Method that updates the level of the alert rule.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		for item in self.constants.OPTIONS_ALERT_RULE_LEVEL:
			if item[0] == alert_rule_data["alert_rule_level"]:
				item[2] = 1
			else:
				item[2] = 0
		option_alert_rule_level = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_ALERT_RULE_LEVEL, "Alert Rule Level")
		alert_rule_data["alert_rule_level"] = option_alert_rule_level
		return alert_rule_data


	def update_index_pattern(self, alert_rule_data):
		"""
		Method that updates the index pattern.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		index_pattern = self.dialog.createInputBoxDialog("Enter the index pattern:", 8, 50, alert_rule_data["index_pattern"])
		alert_rule_data["index_pattern"] = index_pattern
		return alert_rule_data


	def update_total_number_events(self, alert_rule_data):
		"""
		Method that updates how many events found the alert is sent.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		total_number_events = self.dialog.createInputBoxToNumberDialog("Enter the total number of events to which the alert will be sent:", 9, 50, str(alert_rule_data["total_number_events"]))
		alert_rule_data["total_number_events"] = int(total_number_events)
		return alert_rule_data


	def update_search_time(self, alert_rule_data):
		"""
		Method that updates the time at which the search is repeated.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		current_unit_time = list(alert_rule_data["search_time"].keys())[0]
		for item in self.constants.OPTIONS_UNIT_TIME:
			if item[0] == current_unit_time:
				item[2] = 1
			else:
				item[2] = 0
		option_unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
		unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + option_unit_time + " that the search will be repeated:", 9, 50, str(alert_rule_data["search_time"][current_unit_time]))
		alert_rule_data["search_time"] = {option_unit_time : int(unit_time_total)}
		return alert_rule_data


	def update_range_time(self, alert_rule_data):
		"""
		Method that updates the search range time.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		current_unit_time = list(alert_rule_data["range_time"].keys())[0]
		for item in self.constants.OPTIONS_UNIT_TIME:
			if item[0] == current_unit_time:
				item[2] = 1
			else:
				item[2] = 0
		option_unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
		size = 9 if option_unit_time == "minutes" else 8
		unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + option_unit_time + " of the search range:", size, 50, str(alert_rule_data["range_time"][current_unit_time]))
		alert_rule_data["range_time"] = {option_unit_time : int(unit_time_total)}
		return alert_rule_data


	def update_query_type(self, alert_rule_data):
		"""
		Method that updates the query type.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		query_type = list(alert_rule_data["query_type"][0].keys())[0]
		if query_type == "query_string":
			query_string = self.dialog.createInputBoxDialog("Enter the query string:", 8, 50, alert_rule_data["query_type"][0]["query_string"]["query"])
			alert_rule_data["query_type"] = [{"query_string" : {"query" : query_string}}]
		return alert_rule_data


	def update_fields_selection(self, alert_rule_data):
		"""
		Method that updates the field selection option.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		if alert_rule_data["use_fields_selection"]:
			option_fields_selection_true = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_FIELDS_SELECTION_TRUE, "Fields Selection")
			if option_fields_selection_true == "Disable":
				alert_rule_data["use_fields_selection"] = False
				del alert_rule_data["fields_name"]
			elif option_fields_selection_true == "Data":
				option_fields_selection_update = self.dialog.createMenuDialog("Select a option:", 10, 50, self.constants.OPTIONS_FIELDS_SELECTION_UPDATE, "Fields Selection")
				if option_fields_selection_update == "1":
					total_fields = self.dialog.createInputBoxToNumberDialog("Enter the total fields:", 8, 50, "3")
					list_form = self.utils.createListToDialogForm(int(total_fields), "Field name")
					fields_list = self.dialog.createFormDialog("Enter the field's names:", list_form, 15 ,50, "Fields Form", False)
					alert_rule_data["fields_name"].extend(fields_list)
				elif option_fields_selection_update == "2":
					list_form = self.utils.convertListToDialogForm(alert_rule_data["fields_name"], "Field name")
					fields_list = self.dialog.createFormDialog("Enter the field's names:", list_form, 15, 50, "Fields Form", False)
					alert_rule_data["fields_name"] = fields_list
				elif option_fields_selection_update == "3":
					list_checklist_radiolist = self.utils.convertListToDialogList(alert_rule_data["fields_name"], "Field name")
					options_remove_fields = self.dialog.createCheckListDialog("Select one or more options:", 15, 50, list_checklist_radiolist, "Remove Fields")
					message_to_display = self.utils.getStringFromList(options_remove_fields, "Selected Fields:")
					self.dialog.createScrollBoxDialog(message_to_display, 15, 60, "Remove Fields")
					remove_fields = self.dialog.createYesOrNoDialog("\nAre you sure to remove the selected fields?", 7, 50, "Remove Fields")
					if remove_fields == "ok":
						[alert_rule_data["fields_name"].remove(item) for item in options_remove_fields]
		else:
			option_fields_selection_false = self.dialog.createRadioListDialog("Select a option:", 8, 50, self.constants.OPTIONS_FIELDS_SELECTION_FALSE, "Fields Selection")
			if option_fields_selection_false == "Enable":
				alert_rule_data["use_fields_selection"] = True
				total_fields = self.dialog.createInputBoxToNumberDialog("Enter the total fields:", 8, 50, "3")
				list_form = self.utils.createListToDialogForm(int(total_fields), "Field name")
				fields_list = self.dialog.createFormDialog("Enter the field's names:", list_form, 15 ,50, "Fields Form", False)
				alert_rule_data.update({"fields_name" : fields_list})
		return alert_rule_data


	def update_custom_search(self, alert_rule_data):
		"""
		Method that updates the custom search option.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		if alert_rule_data["use_custom_search"]:
			option_custom_search_true = self.dialog.createRadioListDialog("Select a option:", 9 , 55, self.constants.OPTIONS_CUSTOM_SEARCH_TRUE, "Custom Search")
			if option_custom_search_true == "Disable":
				alert_rule_data["use_custom_search"] = False
				if "restriction_by_hostname" in alert_rule_data:
					del alert_rule_data["field_name_hostname"]
					del alert_rule_data["total_events_by_hostname"]
					del alert_rule_data["restriction_by_hostname"]
				if "restriction_by_username" in alert_rule_data:
					del alert_rule_data["field_name_username"]
					del alert_rule_data["total_events_by_username"]
					del alert_rule_data["restriction_by_username"]
				total_number_events = self.dialog.createInputBoxToNumberDialog("Enter the total number of events to which the alert will be sent:", 9, 50, "1")
				alert_rule_data.update({"total_number_events" : int(total_number_events)})
			elif option_custom_search_true == "Data":
				options_custom_search = self.dialog.createCheckListDialog("Select one or more options:", 9, 50, self.constants.OPTIONS_CUSTOM_SEARCH, "Custom Search")
				if "Hostname" in options_custom_search:
					if "restriction_by_hostname" in alert_rule_data:
						option_restriction_by_hostname_true = self.dialog.createRadioListDialog("Select a option:", 8, 55, self.constants.OPTIONS_RESTRICTION_BY_HOSTNAME_TRUE, "Custom Search")
						if option_restriction_by_hostname_true == "Disable":
							del alert_rule_data["restriction_by_hostname"]
							del alert_rule_data["field_name_hostname"]
							del alert_rule_data["total_events_by_hostname"]
							field_name_username = self.dialog.createInputBoxDialog("Enter the field name for the username:", 8, 50, "user.name")
							total_events_by_username = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by username:", 8, 50, "5")
							alert_rule_data.update({"restriction_by_username" : True, "field_name_username" : field_name_username, "total_events_by_username" : int(total_events_by_username)})
						elif option_restriction_by_hostname_true == "Data":
							options_restriction_update = self.dialog.createCheckListDialog("Select one or more options:", 9, 55, self.constants.OPTIONS_RESTRICTION_UPDATE, "Custom Search")
							if "Field" in options_restriction_update:
								field_name_hostname = self.dialog.createInputBoxDialog("Enter the field name for the hostname:", 8, 50, alert_rule_data["field_name_hostname"])
								alert_rule_data["field_name_hostname"] = field_name_hostname
							if "Events" in options_restriction_update:
								total_events_by_hostname = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by hostname:", 8, 50, str(alert_rule_data["total_events_by_hostname"]))
								alert_rule_data["total_events_by_hostname"] = int(total_events_by_hostname)
					else:
						option_restriction_by_hostname_false = self.dialog.createRadioListDialog("Select a option:", 8, 55, self.constants.OPTIONS_RESTRICTION_BY_HOSTNAME_FALSE, "Custom Search")
						if option_restriction_by_hostname_false == "Enable":
							field_name_hostname = self.dialog.createInputBoxDialog("Enter the field name for the hostname:", 8, 50, "host.hostname")
							total_events_by_hostname = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by hostname:", 8, 50, "5")
							alert_rule_data.update({"restriction_by_hostname" : True, "field_name_hostname" : field_name_hostname, "total_events_by_hostname" : int(total_events_by_hostname)})
				if "Username" in options_custom_search:
					if "restriction_by_username" in alert_rule_data:
						option_restriction_by_username_true = self.dialog.createRadioListDialog("Select a option:", 8, 55, self.constants.OPTIONS_RESTRICTION_BY_USERNAME_TRUE, "Custom Search")
						if option_restriction_by_username_true == "Disable":
							del alert_rule_data["field_name_username"]
							del alert_rule_data["total_events_by_username"]
							del alert_rule_data["restriction_by_username"]
							field_name_username = self.dialog.createInputBoxDialog("Enter the field name for the username:", 8, 50, "user.name")
							total_events_by_username = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by username:", 8, 50, "5")
							alert_rule_data.update({"restriction_by_username" : True, "field_name_username" : field_name_username, "total_events_by_username" : int(total_events_by_username)})
						elif option_restriction_by_username_true  == "Data":
							options_restriction_update = self.dialog.createCheckListDialog("Select one or more options:", 9, 55, self.constants.OPTIONS_RESTRICTION_UPDATE, "Custom Search")
							if "Field" in options_restriction_update:
								field_name_username = self.dialog.createInputBoxDialog("Enter the field name for the username:", 8, 50, alert_rule_data["field_name_username"])
								alert_rule_data["field_name_username"] = field_name_username
							if "Events" in options_restriction_update:
								total_events_by_username = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by username:", 8, 50, str(alert_rule_data["total_events_by_username"]))
								alert_rule_data["total_events_by_username"] = int(total_events_by_username)
					else:
						option_restriction_by_username_false = self.dialog.createRadioListDialog("Select a option:", 8, 55, self.constants.OPTIONS_RESTRICTION_BY_USERNAME_FALSE, "Restriction By Username")
						if option_restriction_by_username_false == "Enable":
							field_name_username = self.dialog.createInputBoxDialog("Enter the field name for the username:", 8, 50, "user.name")
							total_events_by_username = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by username:", 8, 50, "5")
							alert_rule_data.update({"restriction_by_username" : True, "field_name_username" : field_name_username, "total_events_by_username" : int(total_events_by_username)})
		else:
			option_custom_search_false = self.dialog.createRadioListDialog("Select a option:", 8, 55, self.constants.OPTIONS_CUSTOM_SEARCH_FALSE, "Custom Search")
			if option_custom_search_false == "Enable":
				alert_rule_data["use_custom_search"] = True
				del alert_rule_data["total_number_events"]
				options_custom_search = self.dialog.createCheckListDialog("Select one or more options:", 9, 50, self.constants.OPTIONS_CUSTOM_SEARCH, "Custom Search")
				if "Hostname" in options_custom_search:
					field_name_hostname = self.dialog.createInputBoxDialog("Enter the field name for the hostname:", 8, 50, "host.hostname")
					total_events_by_hostname = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by hostname:", 8, 50, "5")
					alert_rule_data.update({"restriction_by_hostname" : True, "field_name_hostname" : field_name_hostname, "total_events_by_hostname" : int(total_events_by_hostname)})
				if "Username" in options_custom_search:
					field_name_username = self.dialog.createInputBoxDialog("Enter the field name for the username:", 8, 50, "user.name")
					total_events_by_username = self.dialog.createInputBoxToNumberDialog("Enter the total number of events by username:", 8, 50, "5")
					alert_rule_data.update({"restriction_by_username" : True, "field_name_username" : field_name_username, "total_events_by_username" : int(total_events_by_username)})
		return alert_rule_data


	def update_alert_delivery_type(self, alert_rule_data):
		"""
		Method that updates the type of alert delivery.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		for item in self.constants.OPTIONS_ALERT_DELIVERY_TYPE:
			if item[0] == alert_rule_data["alert_delivery_type"]:
				item[2] = 1
			else:
				item[2] = 0
		option_alert_delivery_type = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_ALERT_DELIVERY_TYPE, "Alert Delivery Type")
		alert_rule_data["alert_delivery_type"] = option_alert_delivery_type
		return alert_rule_data


	def update_telegram_bot_token(self, alert_rule_data):
		"""
		Method that updates the Telegram Bot Token.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
		telegram_bot_token = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.utils.decryptDataWithAES(alert_rule_data["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
		alert_rule_data["telegram_bot_token"] = telegram_bot_token
		return alert_rule_data


	def update_telegram_chat_id(self, alert_rule_data):
		"""
		Method that updates the Telegram Chat ID.

		Returns the dictionary with the updated data of the alert rule.

		:arg alert_rule_data (dict): Dictionary with the data stored in the alert rule.
		"""
		passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
		telegram_chat_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.utils.decryptDataWithAES(alert_rule_data["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
		alert_rule_data["telegram_chat_id"] = telegram_chat_id
		return alert_rule_data