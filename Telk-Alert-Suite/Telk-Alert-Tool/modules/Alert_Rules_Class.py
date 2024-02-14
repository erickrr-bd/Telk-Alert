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


	def create_alert_rule(self):
		"""
		Method that creates an alert rule.
		"""
		try:
			alert_rule_data = []
			alert_rule_name = self.dialog.createFolderOrFileNameDialog("Enter the name of the alert rule:", 8, 50, "rule1")
			alert_rule_data.append(alert_rule_name)
			alert_rule_level = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_ALERT_RULE_LEVEL, "Alert Rule Level")
			alert_rule_data.append(alert_rule_level)
			index_pattern = self.dialog.createInputBoxDialog("Enter the index pattern:", 8, 50, "winlogbeat-*")
			alert_rule_data.append(index_pattern)
			alert_rule_type = self.dialog.createRadioListDialog("Select a option:", 8, 50, self.constants.OPTIONS_ALERT_RULE_TYPE, "Alert Rule Type")
			alert_rule_data.append(alert_rule_type)
			if alert_rule_type == "Frequency":
				total_events = self.dialog.createInputBoxToNumberDialog("Enter the total events to which the alert will be sent:", 9, 50, "1")
				alert_rule_data.append(total_events)
				unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
				alert_rule_data.append(unit_time)
				unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + unit_time + " that the search will be repeated:", 9, 50, "1")
				alert_rule_data.append(unit_time_total)
				unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
				size = 9 if unit_time == "minutes" else 8
				alert_rule_data.append(unit_time)
				unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + unit_time + " of the search range:", size, 50, "1")
				alert_rule_data.append(unit_time_total)
				query_type = self.dialog.createRadioListDialog("Select a option:", 9, 70, self.constants.OPTIONS_QUERY_TYPE, "Query Type")
				alert_rule_data.append(query_type)
				if query_type == "query_string":
					query_string = self.dialog.createInputBoxDialog("Enter the query string:", 8, 50, "event.code: 4625")
					alert_rule_data.append(query_string)
				elif query_type == "wildcard_query":
					field_name = self.dialog.createInputBoxDialog("Enter the name of the field:", 8, 50, "PATH.name")
					alert_rule_data.append(field_name)
					wildcard_query = self.dialog.createInputBoxDialog("Enter the wildcard query:", 8, 50, "*key")
					alert_rule_data.append(wildcard_query)
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
					options_custom_search = self.dialog.createCheckListDialog("Select one or more options:", 10, 50, self.constants.OPTIONS_CUSTOM_SEARCH, "Custom Search")
					if "Source" in options_custom_search:
						alert_rule_data.append(True)
						source_field = self.dialog.createInputBoxDialog("Enter the field name for the source:", 8, 50, "source_ip")
						alert_rule_data.append(source_field)
						total_events_by_source = self.dialog.createInputBoxToNumberDialog("Enter the total events by source:", 8, 50, "5")
						alert_rule_data.append(total_events_by_source)
					else:
						alert_rule_data.append(False)
					if "Destination" in options_custom_search:
						alert_rule_data.append(True)
						destination_field = self.dialog.createInputBoxDialog("Enter the field name for the destination:", 8, 50, "dst_ip")
						alert_rule_data.append(destination_field)
						total_events_by_destination = self.dialog.createInputBoxToNumberDialog("Enter the total events by destination:", 8, 50, "5")
						alert_rule_data.append(total_events_by_destination)
					else:
						alert_rule_data.append(False)
					if "Username" in options_custom_search:
						alert_rule_data.append(True)
						username_field = self.dialog.createInputBoxDialog("Enter the field name for the username:", 8, 50, "user.name")
						alert_rule_data.append(username_field)
						total_events_by_username = self.dialog.createInputBoxToNumberDialog("Enter the total events by username:", 8, 50, "5")
						alert_rule_data.append(total_events_by_username)
					else:
						alert_rule_data.append(False)
				else:
					alert_rule_data.append(False)
				alert_delivery_type = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_ALERT_DELIVERY_TYPE, "Alert Delivery Type")
				alert_rule_data.append(alert_delivery_type)
				passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_PATH)
				telegram_bot_token = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
				alert_rule_data.append(telegram_bot_token)
				telegram_chat_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
				alert_rule_data.append(telegram_chat_id)
			self.create_yaml_file(alert_rule_data)
			if path.exists(self.constants.ALERT_RULES_PATH + '/' + alert_rule_name + ".yaml"):
				self.dialog.createMessageDialog("\nAlert rule created: " + alert_rule_name, 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Alert rule created: " + alert_rule_name, 1, "__createAlertRule", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.createMessageDialog("\nError creating the alert rule. For more information, see the logs.", 8, 50, "Error Message")
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
			alert_rules_list = self.utils.getListYamlFilesInFolder(self.constants.ALERT_RULES_PATH)
			if alert_rules_list:
				list_checklist_radiolist = self.utils.convertListToDialogList(alert_rules_list, "Alert rule name")
				alert_rule_update =self.dialog.createRadioListDialog("Select a option:", 18, 70, list_checklist_radiolist, "Alert Rules")
				alert_rule_fields = self.dialog.createCheckListDialog("Select one or more options:", 19, 70, self.constants.OPTIONS_ALERT_RULE_FIELDS, "Alert Rule Fields")
				alert_rule_path = self.constants.ALERT_RULES_PATH + '/' + alert_rule_update
				alert_rule_data = self.utils.readYamlFile(alert_rule_path)
				file_hash_original = self.utils.getHashFunctionOfFile(alert_rule_path)
				if "Name" in alert_rule_fields:
					self.update_alert_rule_name(alert_rule_data)
				if "Level" in alert_rule_fields:
					self.update_alert_rule_level(alert_rule_data)
				if "Index" in alert_rule_fields:
					self.update_index_pattern(alert_rule_data)
				if "Total Events" in alert_rule_fields:
					self.update_total_events(alert_rule_data)
				if "Search Time" in alert_rule_fields:
					self.update_search_time(alert_rule_data)
				if "Range Time" in alert_rule_fields:
					self.update_range_time(alert_rule_data)
				if "Query" in alert_rule_fields:
					self.update_query_type(alert_rule_data)
				if "Fields Selection" in alert_rule_fields:
					self.update_fields_selection(alert_rule_data)
				if "Custom Search" in alert_rule_fields:
					self.update_custom_search(alert_rule_data)
				if "Delivery" in alert_rule_fields:
					self.update_alert_delivery_type(alert_rule_data)
				if "Bot Token" in alert_rule_fields:
					self.update_telegram_bot_token(alert_rule_data)
				if "Chat ID" in alert_rule_fields:
					self.update_telegram_chat_id(alert_rule_data)
				alert_rule_new_path = self.constants.ALERT_RULES_PATH + '/' + alert_rule_data["alert_rule_name"] + ".yaml"
				self.utils.createYamlFile(alert_rule_data, alert_rule_new_path)
				files_hash_new = self.utils.getHashFunctionOfFile(alert_rule_new_path)
				if file_hash_original == files_hash_new:
					self.dialog.createMessageDialog("\nAlert rule not updated: " + alert_rule_data["alert_rule_name"], 7, 50, "Notification Message")
				else:
					self.dialog.createMessageDialog("\nUpdated alert rule: " + alert_rule_data["alert_rule_name"], 7, 50, "Notification Message")
					self.logger.generateApplicationLog("Updated alert rule: " + alert_rule_data["alert_rule_name"], 2, "__updateAlertRule", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
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
			alert_rules_list = self.utils.getListYamlFilesInFolder(self.constants.ALERT_RULES_PATH)
			if alert_rules_list:
				list_checklist_radiolist = self.utils.convertListToDialogList(alert_rules_list, "Alert rule name")
				option_alert_rule =self.dialog.createRadioListDialog("Select a option:", 18, 70, list_checklist_radiolist, "Alert Rules")
				yaml_file_data = self.utils.convertYamlFileToString(self.constants.ALERT_RULES_PATH + '/' + option_alert_rule)
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
			alert_rules_list = self.utils.getListYamlFilesInFolder(self.constants.ALERT_RULES_PATH)
			if alert_rules_list:
				list_checklist_radiolist = self.utils.convertListToDialogList(alert_rules_list, "Alert rule name")
				options_alert_rule = self.dialog.createCheckListDialog("Select one or more options:", 18, 70, list_checklist_radiolist, "Remove Alert Rules")
				message_to_display = self.utils.getStringFromList(options_alert_rule, "Alert rules selected to remove:")
				self.dialog.createScrollBoxDialog(message_to_display, 14, 50, "Remove Alert Rules")
				yes_no_remove = self.dialog.createYesOrNoDialog("\nAre you sure to remove the selected alert rules?\n\n** This action cannot be undone.", 10, 50, "Remove Alert Rules")
				if yes_no_remove == "ok":
					[self.utils.deleteFile(self.constants.ALERT_RULES_PATH + '/' + item) for item in options_alert_rule]
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
		Method that displays a list with all the defined alert rules.
		"""
		try:
			alert_rules_list = self.utils.getListYamlFilesInFolder(self.constants.ALERT_RULES_PATH)
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

		:arg alert_rule_data (list): List with the configuration of the new alert rule.
		"""
		alert_rule_data_json = {
			"alert_rule_name" : alert_rule_data[0],
			"alert_rule_level" : alert_rule_data[1],
			"index_pattern" : alert_rule_data[2],
			"alert_rule_type" : alert_rule_data[3],
			"total_events" : int(alert_rule_data[4]),
			"search_time" : {alert_rule_data[5] : int(alert_rule_data[6])},
			"range_time" : {alert_rule_data[7] : int(alert_rule_data[8])}
		}

		if alert_rule_data[9] == "query_string":
			alert_rule_data_json.update({"query_type" : [{alert_rule_data[9] : {"query" : alert_rule_data[10]}}]})
			last_index = 10		
		elif alert_rule_data[9] == "wildcard_query":
			alert_rule_data_json.update({"query_type" : [{alert_rule_data[9] : {alert_rule_data[10] : alert_rule_data[11]}}]})
			last_index = 11
		alert_rule_data_json.update({"use_fields_selection" : alert_rule_data[last_index + 1]})
		if alert_rule_data[last_index + 1]:
			alert_rule_data_json.update({"fields_name" : alert_rule_data[last_index + 2]})
			last_index += 2 
		else:
			last_index += 1 
		alert_rule_data_json.update({"use_custom_search" : alert_rule_data[last_index + 1]})
		if alert_rule_data[last_index + 1]:
			del alert_rule_data_json["total_events"]
			alert_rule_data_json.update({"restriction_by_source" : alert_rule_data[last_index + 2]})
			if alert_rule_data[last_index + 2]:
				alert_rule_data_json.update({"source_field" : alert_rule_data[last_index + 3], "total_events_by_source" : int(alert_rule_data[last_index + 4])})
				last_index += 4
			else:
				last_index += 2
			alert_rule_data_json.update({"restriction_by_destination" : alert_rule_data[last_index + 1]})
			if alert_rule_data[last_index + 1]:
				alert_rule_data_json.update({"destination_field" : alert_rule_data[last_index + 2], "total_events_by_destination" : int(alert_rule_data[last_index + 3])})
				last_index += 3
			else:
				last_index +=1
			alert_rule_data_json.update({"restriction_by_username" : alert_rule_data[last_index + 1]})
			if alert_rule_data[last_index + 1]:
				alert_rule_data_json.update({"username_field" : alert_rule_data[last_index + 2], "total_events_by_username" : int(alert_rule_data[last_index + 3])})
				last_index += 3
			else:
				last_index += 1
		else:
			last_index += 1
		alert_rule_data_json.update({"alert_delivery_type" : alert_rule_data[last_index + 1], "telegram_bot_token" : alert_rule_data[last_index + 2], "telegram_chat_id" : alert_rule_data[last_index + 3]})

		alert_rule_path = self.constants.ALERT_RULES_PATH + '/' + alert_rule_data[0] + ".yaml"
		self.utils.createYamlFile(alert_rule_data_json, alert_rule_path)
		self.utils.changeFileFolderOwner(alert_rule_path, self.constants.USER, self.constants.GROUP, "644")


	def update_alert_rule_name(self, alert_rule_data):
		"""
		Method that updates the name of the alert rule.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		alert_rule_name = self.dialog.createFolderOrFileNameDialog("Enter the name of the alert rule:", 8, 50, alert_rule_data["alert_rule_name"])
		if not alert_rule_data["alert_rule_name"] == alert_rule_name:
			self.utils.renameFileOrFolder(self.constants.ALERT_RULES_PATH + '/' + alert_rule_data["alert_rule_name"] + ".yaml", self.constants.ALERT_RULES_PATH + '/' + alert_rule_name + ".yaml")
			alert_rule_data["alert_rule_name"] = alert_rule_name
		return alert_rule_data


	def update_alert_rule_level(self, alert_rule_data):
		"""
		Method that updates the criticality level of the alert rule.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		for item in self.constants.OPTIONS_ALERT_RULE_LEVEL:
			if item[0] == alert_rule_data["alert_rule_level"]:
				item[2] = 1
			else:
				item[2] = 0
		alert_rule_level = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_ALERT_RULE_LEVEL, "Alert Rule Level")
		alert_rule_data["alert_rule_level"] = alert_rule_level
		return alert_rule_data


	def update_index_pattern(self, alert_rule_data):
		"""
		Method that updates the index pattern.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		index_pattern = self.dialog.createInputBoxDialog("Enter the index pattern:", 8, 50, alert_rule_data["index_pattern"])
		alert_rule_data["index_pattern"] = index_pattern
		return alert_rule_data


	def update_total_events(self, alert_rule_data):
		"""
		Method that updates the number of events to which the alert is sent.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		total_events = self.dialog.createInputBoxToNumberDialog("Enter the total events to which the alert will be sent:", 9, 50, str(alert_rule_data["total_events"]))
		alert_rule_data["total_events"] = int(total_events)
		return alert_rule_data


	def update_search_time(self, alert_rule_data):
		"""
		Method that updates the search repetition time.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		current_unit_time = list(alert_rule_data["search_time"].keys())[0]
		for item in self.constants.OPTIONS_UNIT_TIME:
			if item[0] == current_unit_time:
				item[2] = 1
			else:
				item[2] = 0
		unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
		unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + unit_time + " that the search will be repeated:", 9, 50, str(alert_rule_data["search_time"][current_unit_time]))
		alert_rule_data["search_time"] = {unit_time : int(unit_time_total)}
		return alert_rule_data


	def update_range_time(self, alert_rule_data):
		"""
		Method that updates the time range of the search.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		current_unit_time = list(alert_rule_data["range_time"].keys())[0]
		for item in self.constants.OPTIONS_UNIT_TIME:
			if item[0] == current_unit_time:
				item[2] = 1
			else:
				item[2] = 0
		unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
		size = 9 if unit_time == "minutes" else 8
		unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + unit_time + " of the search range:", size, 50, str(alert_rule_data["range_time"][current_unit_time]))
		alert_rule_data["range_time"] = {unit_time : int(unit_time_total)}
		return alert_rule_data


	def update_query_type(self, alert_rule_data):
		"""
		Method that updates the ElasticSearch Query Type.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		current_query_type = list(alert_rule_data["query_type"][0].keys())[0]
		if current_query_type == "query_string":
			query_string_update = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_QUERY_STRING_UPDATE, "Query String")
			if query_string_update == "Wildcard Query":
				del alert_rule_data["query_type"]
				field_name = self.dialog.createInputBoxDialog("Enter the name of the field:", 8, 50, "PATH.name")
				wildcard_query = self.dialog.createInputBoxDialog("Enter the wildcard query:", 8, 50, "*key")
				alert_rule_data.update({"query_type" : [{"wildcard_query" : {field_name : wildcard_query}}]})
			elif query_string_update == "Query String":
				query_string = self.dialog.createInputBoxDialog("Enter the query string:", 8, 50, alert_rule_data["query_type"][0]["query_string"]["query"])
				alert_rule_data["query_type"] = [{"query_string" : {"query" : query_string}}]
		elif current_query_type == "wildcard_query":
			wildcard_query_update = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_WILDCARD_QUERY_UPDATE, "Wildcard Query")
			if wildcard_query_update == "Query String":
				del alert_rule_data["query_type"]
				query_string = self.dialog.createInputBoxDialog("Enter the query string:", 8, 50, "event.code: 4625")
				alert_rule_data.update({"query_type" : [{"query_string" : {"query" : query_string}}]})
			elif wildcard_query_update == "Data":
				wildcard_query_data = self.dialog.createCheckListDialog("Select one or more options:", 9, 50, self.constants.OPTIONS_WILDCARD_QUERY_DATA, "Wildcard Query")
				field_name = list(alert_rule_data["query_type"][0]["wildcard_query"].keys())[0]
				wildcard_query = alert_rule_data["query_type"][0]["wildcard_query"][field_name]
				if "Field" in wildcard_query_data:
					field_name = self.dialog.createInputBoxDialog("Enter the name of the field:", 8, 50, field_name)
				if "Query" in wildcard_query_data:
					wildcard_query = self.dialog.createInputBoxDialog("Enter the wildcard query:", 8, 50, wildcard_query)
				del alert_rule_data["query_type"]
				alert_rule_data.update({"query_type" : [{"wildcard_query" : {field_name : wildcard_query}}]})
		return alert_rule_data


	def update_fields_selection(self, alert_rule_data):
		"""
		Method that updates the field selection option.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
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

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
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

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
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

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_PATH)
		telegram_bot_token = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.utils.decryptDataWithAES(alert_rule_data["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
		alert_rule_data["telegram_bot_token"] = telegram_bot_token
		return alert_rule_data


	def update_telegram_chat_id(self, alert_rule_data):
		"""
		Method that updates the Telegram Chat ID.

		Returns the dictionary with the updated alert rule configuration.

		:arg alert_rule_data (dict): Dictionary with alert rule configuration.
		"""
		passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_PATH)
		telegram_chat_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.utils.decryptDataWithAES(alert_rule_data["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
		alert_rule_data["telegram_chat_id"] = telegram_chat_id
		return alert_rule_data