from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related with the alert rules.
"""
class AlertRules:

	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel (object): Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)
		folder_rules_name = self.__utils.readYamlFile(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE)["folder_rules_name"]
		self.__folder_alert_rules_path = self.__constants.PATH_BASE_TELK_ALERT + '/' + folder_rules_name


	def createNewAlertRule(self):
		"""
		Method that collects the information for the creation of the new alert rule.
		"""
		alert_rule_data = []
		#try:
		alert_rule_name = self.__dialog.createFolderOrFileNameDialog("Enter alert rule's name:", 8, 50, "rule1")
		alert_rule_data.append(alert_rule_name)
		option_alert_rule_level = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_ALERT_RULE_LEVEL, "Alert Rule Level")
		alert_rule_data.append(option_alert_rule_level)
		index_pattern_name = self.__dialog.createInputBoxDialog("Enter index pattern's name where the search will be made:", 9, 50, "winlogbeat-*")
		alert_rule_data.append(index_pattern_name)
		option_alert_rule_type = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_ALERT_RULE_TYPE, "Alert Rule Type")
		alert_rule_data.append(option_alert_rule_type)
		if option_alert_rule_type == "Frequency":
			number_events_found_by_alert = self.__dialog.createInputBoxToNumberDialog("Enter the number of events found to which the alert is sent:", 9, 50, "1")
			alert_rule_data.append(number_events_found_by_alert)
			option_unit_time_search = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_UNIT_TIME, "Unit Time")
			alert_rule_data.append(option_unit_time_search)
			total_unit_time_search = self.__dialog.createInputBoxToNumberDialog("Enter the total in " + option_unit_time_search + " that the search will be repeated:", 9, 50, "1")
			alert_rule_data.append(total_unit_time_search)
			option_unit_time_range = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_UNIT_TIME, "Unit Time")
			alert_rule_data.append(option_unit_time_range)
			total_unit_time_range = self.__dialog.createInputBoxToNumberDialog("Enter the range in " + option_unit_time_range + " of the search:", 8, 50, "1")
			alert_rule_data.append(total_unit_time_range)
		query_type = self.__dialog.createRadioListDialog("Select a option:", 9, 70, self.__constants.OPTIONS_QUERY_TYPE, "Query Type")
		alert_rule_data.append(query_type)
		if query_type == "query_string":
			query_string = self.__dialog.createInputBoxDialog("Enter the query string:", 8, 50, "event.code: 4625")
			alert_rule_data.append(query_string)
			use_fields_option = self.__dialog.createYesOrNoDialog("\nDo you require to use the fields option for the search?", 8, 50, "Fields Option Search")
			if use_fields_option == "ok":
				alert_rule_data.append(True)
				number_of_fields_to_enter = self.__dialog.createInputBoxToNumberDialog("Enter the total of fields to be define:", 8, 50, "3")
				list_to_form_dialog = self.__utils.createListToDialogForm(int(number_of_fields_to_enter), "Field")
				list_all_fields = self.__dialog.createFormDialog("Enter the field's names:", list_to_form_dialog, 15, 50, "Fields Form")
				alert_rule_data.append(list_all_fields)
			else:
				alert_rule_data.append(False)
			use_custom_rule_option = self.__dialog.createYesOrNoDialog("\nDo you require to use the custom rule option?", 8, 50, "Custom Rule Option")
			if use_custom_rule_option == "ok":
				alert_rule_data.append(True)
				options_custom_rule_option = self.__dialog.createCheckListDialog("Select one or more options:", 10, 50, self.__constants.OPTIONS_CUSTOM_RULE, "Custom Rule Options")
				if "Hostname" in options_custom_rule_option:
					alert_rule_data.append(True)
					field_name_hostname = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the hostname:", 8, 50, "host.hostname")
					alert_rule_data.append(field_name_hostname)
					number_total_events_by_hostname = self.__dialog.createInputBoxToNumberDialog("Enter the total of events by hostname for the alert rule:", 8, 50, "5")
					alert_rule_data.append(number_total_events_by_hostname)
				else:
					alert_rule_data.append(False)
				if "Username" in options_custom_rule_option:
					alert_rule_data.append(True)
					field_name_username = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the username", 8, 50, "winlog.username")
					alert_rule_data.append(field_name_username)
					number_total_events_by_username = self.__dialog.createInputBoxToNumberDialog("Enter the total of events by username for the alert rule", 8, 50, "5")
					alert_rule_data.append(number_total_events_by_username)
				else:
					alert_rule_data.append(False)
			else:
				alert_rule_data.append(False)
			option_send_type_alert_rule = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_SHIPPING_KIND, "Alert Shipping Kind Options")
			alert_rule_data.append(option_send_type_alert_rule)
		elif query_type == "aggregations":
			index_field_name = self.__dialog.createInputBoxDialog("Enther the index field's name:", 8, 50, "host.hostname.keyword")
			alert_rule_data.append(index_field_name)
		passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
		telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
		alert_rule_data.append(telegram_bot_token.decode("utf-8"))
		telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
		alert_rule_data.append(telegram_chat_id.decode("utf-8"))
		self.__createYamlFileAlertRule(alert_rule_data)
		if path.exists(self.__folder_alert_rules_path + '/' + alert_rule_name + ".yaml"):
			self.__logger.generateApplicationLog("Alert rule created: " + alert_rule_name, 1, "__createAlertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__dialog.createMessageDialog("\nAlert rule created: " + alert_rule_name, 7, 50, "Notification Message")
		#except ValueError as exception:
		#	self.__dialog.createMessageDialog("\nValue Error. For more information, see the logs.", 8, 50, "Error Message")
		#	self.__logger.generateApplicationLog(exception, 3, "__createAlertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		#except (OSError, FileNotFoundError) as exception:
		#	self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
		#	self.__logger.generateApplicationLog(exception, 3, "__createAlertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		#finally:
		#	self.__action_to_cancel()


	def modifyAlertRule(self):
		"""
		Method tha modifies one or more values in a specific alert rule.
		"""
		try:
			list_all_alert_rules = self.__utils.getListOfAllYamlFilesInFolder(self.__folder_alert_rules_path)
			if list_all_alert_rules:
				flag_rename_alert_rule = 0
				list_alert_rules_to_update = self.__utils.convertListToDialogList(list_all_alert_rules, "Alert Rule")
				alert_rule_to_update = self.__dialog.createRadioListDialog("Select a option:", 18, 70, list_alert_rules_to_update, "Alert Rules")
				options_alert_rule_update = self.__dialog.createCheckListDialog("Select one or more options:", 19, 70, self.__constants.OPTIONS_ALERT_RULE_UPDATE, "Alert Rule's Values")
				alert_rule_path = self.__folder_alert_rules_path + '/' + alert_rule_to_update
				alert_rule_data = self.__utils.readYamlFile(alert_rule_path)
				hash_alert_rule_actual = self.__utils.getHashFunctionToFile(alert_rule_path)
				alert_rule_name_actual = alert_rule_data["alert_rule_name"]
				if "Name" in options_alert_rule_update:
					alert_rule_name = self.__dialog.createFolderOrFileNameDialog("Enter alert rule's name:", 8, 50, alert_rule_data["alert_rule_name"])
					if not alert_rule_name == alert_rule_data["alert_rule_name"]:
						flag_rename_alert_rule = 1
						alert_rule_data["alert_rule_name"] = alert_rule_name
				if "Level" in options_alert_rule_update:
					for option in self.__constants.OPTIONS_ALERT_RULE_LEVEL:
						if option[0] == alert_rule_data["alert_rule_level"]:
							option[2] = 1
						else:
							option[2] = 0
					option_alert_rule_level = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_ALERT_RULE_LEVEL, "Alert Rule Level")
					alert_rule_data["alert_rule_level"] = option_alert_rule_level
				if "Index" in options_alert_rule_update:
					index_pattern_name = self.__dialog.createInputBoxDialog("Enter index pattern's name where the search will be made:", 9, 50, alert_rule_data["index_pattern_name"])
					alert_rule_data["index_pattern_name"] = index_pattern_name
				if "Number Events" in options_alert_rule_update:
					number_events_found_by_alert = self.__dialog.createInputBoxToNumberDialog("Enter the number of events found to which the alert is sent:", 9, 50, str(alert_rule_data["number_events_found_by_alert"]))
					alert_rule_data["number_events_found_by_alert"] = int(number_events_found_by_alert)
				if "Time Search" in options_alert_rule_update:
					for unit_time in alert_rule_data["time_search"]:
						unit_time_actual = unit_time
					for unit_time in self.__constants.OPTIONS_UNIT_TIME:
						if unit_time[0] == unit_time_actual:
							unit_time[2] = 1
						else:
							unit_time[2] = 0
					option_unit_time = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_UNIT_TIME, "Unit Time")
					time_search_total = self.__dialog.createInputBoxToNumberDialog("Enter the total in " + option_unit_time + " that the search will be repeated:", 9, 50, str(alert_rule_data["time_search"][unit_time_actual]))
					alert_rule_data["time_search"] = {option_unit_time : int(time_search_total)}
				if "Time Range" in options_alert_rule_update:
					for unit_time in alert_rule_data["time_range"]:
						unit_time_actual = unit_time
					for unit_time in self.__constants.OPTIONS_UNIT_TIME:
						if unit_time[0] == unit_time_actual:
							unit_time[2] = 1
						else:
							unit_time[2] = 0
					option_unit_time = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_UNIT_TIME, "Unit Time")
					time_range_total = self.__dialog.createInputBoxToNumberDialog("Enter the range in " + option_unit_time + " of the search:", 8, 50, str(alert_rule_data["time_range"][unit_time_actual]))
					alert_rule_data["time_range"] = {option_unit_time : int(time_range_total)}
				if "Query Kind" in options_alert_rule_update:
					for unit_time in alert_rule_data["query_string"]:
						unit_time_actual = unit_time
						print(unit_time_actual)
					#query_string = self.__dialog.createInputBoxDialog("Enter the query string:", 8, 50, alert_rule_data['query_type'][0]['query_string']['query'])
					#alert_rule_data["query_type"] = [{"query_string" : {"query" : query_string}}]
				if "Fields Option" in options_alert_rule_update:
					if alert_rule_data["use_fields_option"] == True:
						option_fields_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_FIELDS_OPTION_TRUE, "Field's Option")
						if option_fields_true == "Disable":
							alert_rule_data["use_fields_option"] = False
							del alert_rule_data["fields_name"]
						elif option_fields_true == "Data":
							option_fields_update = self.__dialog.createMenuDialog("Select a option:", 10, 50, self.__constants.OPTIONS_FIELDS_OPTION_UPDATE, "Field's Option Menu")
							if option_fields_update == "1":
								total_fields = self.__dialog.createInputBoxToNumberDialog("Enter the total of fields that will be defined:", 9, 50, "3")
								list_to_form_dialog = self.__utils.createListToDialogForm(int(total_fields), "Field's Name")
								list_all_fields = self.__dialog.createFormDialog("Enter the field's names:", list_to_form_dialog, 15, 50, "Add Field's Form")
								alert_rule_data["fields_name"].extend(list_all_fields)
							elif option_fields_update == "2":
								list_to_form_dialog = self.__utils.convertListToDialogForm(alert_rule_data["fields_name"], "Field")
								list_all_fields = self.__dialog.createFormDialog("Enter the field's names:", list_to_form_dialog, 15, 50, "Update Field's Form")
								alert_rule_data["fields_name"] = list_all_fields
							elif option_fields_update == "3":
								list_to_dialog = self.__utils.convertListToDialogList(alert_rule_data["fields_name"], "Field's Name")
								options_fields_remove = self.__dialog.createCheckListDialog("Select one or more options:", 14, 50, list_to_dialog, "Remove Field's Form")
								
								for option in options_fields_remove:
									alert_rule_data["fields_name"].remove(option)
					else:
						option_fields_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_FIELDS_OPTION_FALSE, "Field's Option")
						if option_fields_false == "Enable":
							alert_rule_data["use_fields_option"] = True
							total_fields = self.__dialog.createInputBoxToNumberDialog("Enter the total of fields that will be defined:", 9, 50, "3")
							list_to_form_dialog = self.__utils.createListToDialogForm(int(total_fields), "Field's Name")
							list_all_fields = self.__dialog.createFormDialog("Enter the field's names:", list_to_form_dialog, 15, 50, "Field's Option Form")
							fields_name_json = {"fields_name" : list_all_fields}
							alert_rule_data.update(fields_name_json)
				if "Custom Rule" in options_alert_rule_update:
					if alert_rule_data["use_custom_rule_option"] == True:
						option_custom_rule_true = self.__dialog.createRadioListDialog("Select a option:", 9, 55, self.__constants.OPTIONS_CUSTOM_RULE_OPTION_TRUE, "Custom Rule's Option")
						if option_custom_rule_true == "Disable":
							alert_rule_data["use_custom_rule_option"] = False
							if "restriction_by_hostname" in alert_rule_data:
								if alert_rule_data["restriction_by_hostname"] == True:
									del alert_rule_data["field_name_hostname"]
									del alert_rule_data["number_total_events_by_hostname"]
								del alert_rule_data["restriction_by_hostname"]
							if "restriction_by_username" in alert_rule_data:
								if alert_rule_data["restriction_by_username"] == True:
									del alert_rule_data["field_name_username"]
									del alert_rule_data["number_total_events_by_username"]
								del alert_rule_data["restriction_by_username"]
						elif option_custom_rule_true == "Data":
							options_custom_rule = self.__dialog.createCheckListDialog("Select one or more options:", 9, 50, self.__constants.OPTIONS_CUSTOM_RULE, "Custom Rule's Options")
							if "Hostname" in options_custom_rule:
								if "restriction_by_hostname" in alert_rule_data:
									if alert_rule_data["restriction_by_hostname"] == True:
										option_restriction_by_hostname_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_RESTRICTION_BY_HOSTNAME_TRUE, "Restriction By Hostname")
										if option_restriction_by_hostname_true == "Disable":
											if alert_rule_data["restriction_by_username"] == True:
												alert_rule_data["restriction_by_hostname"] = False
												del alert_rule_data["field_name_hostname"]
												del alert_rule_data["number_total_events_by_hostname"]
											else:
												self.__dialog.createMessageDialog("\nIt is necessary to enable at least one restriction.", 7, 50, "Notification Message")
										elif option_restriction_by_hostname_true == "Data":
											options_restriction_by_hostname_update = self.__dialog.createCheckListDialog("Select one or more options:", 9, 50, self.__constants.OPTIONS_RESTRICTION_UPDATE, "Restriction By Hostname")
											if "Field" in options_restriction_by_hostname_update:
												hostname_field_name = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the hostname:", 9, 50, alert_rule_data["field_name_hostname"])
												alert_rule_data["field_name_hostname"] = hostname_field_name
											if "Events" in options_restriction_by_hostname_update:
												total_events_by_hostname = self.__dialog.createInputBoxToNumberDialog("Enter the total number of events per hostname for the search:", 9, 50, str(alert_rule_data["number_total_events_by_hostname"]))
												alert_rule_data["number_total_events_by_hostname"] = int(total_events_by_hostname)
									else:
										option_restriction_by_hostname_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_RESTRICTION_BY_HOSTNAME_FALSE, "Restriction By Hostname")
										if option_restriction_by_hostname_false == "Enable":
											alert_rule_data["restriction_by_hostname"] = True
											hostname_field_name = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the hostname:", 9, 50, "host.hostname")
											total_events_by_hostname = self.__dialog.createInputBoxToNumberDialog("Enter the total number of events per hostname for the search:", 9, 50, "5")
											restriction_by_hostname_json = {"field_name_hostname" : hostname_field_name, "number_total_events_by_hostname" : int(total_events_by_hostname)}
											alert_rule_data.update(restriction_by_hostname_json)
							if "Username" in options_custom_rule:
								if "restriction_by_username" in alert_rule_data:
									if alert_rule_data["restriction_by_username"] == True:
										option_restriction_by_username_true = self.__dialog.createRadioListDialog("select a option:", 9, 50, self.__constants.OPTIONS_RESTRICTION_BY_USERNAME_TRUE, "Restriction By Username")
										if option_restriction_by_username_true == "Disable":
											if alert_rule_data["restriction_by_hostname"] == True:
												alert_rule_data["restriction_by_username"] = False
												del alert_rule_data["field_name_username"]
												del alert_rule_data["number_total_events_by_username"]
											else:
												self.__dialog.createMessageDialog("\nIt is necessary to enable at least one restriction.", 7, 50, "Notification Message")
										elif option_restriction_by_username_true == "Data":
											options_restriction_by_username_update = self.__dialog.createCheckListDialog("Select one or more options:", 9, 50, self.__constants.OPTIONS_RESTRICTION_UPDATE, "Restriction By Username")
											if "Field" in options_restriction_by_username_update:
												username_field_name = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the username:", 9, 50, alert_rule_data["field_name_username"])
												alert_rule_data["field_name_username"] = username_field_name
											if "Events" in options_restriction_by_username_update:
												total_events_by_username = self.__dialog.createInputBoxToNumberDialog("Enter the total number of events per username for the search:", 9, 50, str(alert_rule_data["number_total_events_by_username"]))
												alert_rule_data["number_total_events_by_username"] = int(total_events_by_username)
									else:
										option_restriction_by_username_false = self.__dialog.createRadioListDialog("select a option:", 8, 50, self.__constants.OPTIONS_RESTRICTION_BY_USERNAME_FALSE, "Restriction By Username")
										if option_restriction_by_username_false == "Enable":
											alert_rule_data["restriction_by_username"] = True
											username_field_name = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the username", 9, 50, "winlog.username")
											total_events_by_username = self.__dialog.createInputBoxToNumberDialog("Enter the total number of events per username for the search:", 9, 50, "5")
											restriction_by_username_json = {"field_name_username" : username_field_name, "number_total_events_by_username" : int(total_events_by_username)}
											alert_rule_data.update(restriction_by_username_json)
					else:
						option_custom_rule_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CUSTOM_RULE_OPTION_FALSE, "Custom Rule's Option")
						if option_custom_rule_false == "Enable":
							alert_rule_data["use_custom_rule_option"] = True
							options_custom_rule = self.__dialog.createCheckListDialog("Select one or more options:", 9, 50, self.__constants.OPTIONS_CUSTOM_RULE, "Custom Rule's Options")
							if "Hostname" in options_custom_rule:
								hostname_field_name = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the hostname:", 9, 50, "host.hostname")
								total_events_by_hostname = self.__dialog.createInputBoxToNumberDialog("Enter the total number of events per hostname for the search:", 9, 50, "5")
								restriction_by_hostname_json = {"restriction_by_hostname" : True, "field_name_hostname" : hostname_field_name, "number_total_events_by_hostname" : int(total_events_by_hostname)}
							else:
								restriction_by_hostname_json = {"restriction_by_hostname" : False}
							if "Username" in options_custom_rule:
								username_field_name = self.__dialog.createInputBoxDialog("Enter the field's name in the index that corresponds the username", 9, 50, "winlog.username")
								total_events_by_username = self.__dialog.createInputBoxToNumberDialog("Enter the total number of events per username for the search:", 9, 50, "5")
								restriction_by_username_json = {"restriction_by_username" : True, "field_name_username" : username_field_name, "number_total_events_by_username" : int(total_events_by_username)}
							else:
								restriction_by_username_json = {"restriction_by_username" : False}
							alert_rule_data.update(restriction_by_hostname_json)
							alert_rule_data.update(restriction_by_username_json)
				if "Shipping Kind" in options_alert_rule_update:
					for option in self.__constants.OPTIONS_SHIPPING_KIND:
						if option[0] == alert_rule_data["send_type_alert_rule"]:
							option[2] = 1
						else:
							option[2] = 0
					option_shipping_kind = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_SHIPPING_KIND, "Alert Rule's Shipping Options")
					alert_rule_data["send_type_alert_rule"] = option_shipping_kind
				if "Bot Token" in options_alert_rule_update:
					passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
					telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram's bot token:", 8, 50, self.__utils.decryptDataWithAES(alert_rule_data["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
					alert_rule_data["telegram_bot_token"] = telegram_bot_token.decode("utf-8")
				if "Chat ID" in options_alert_rule_update:
					passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
					telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram's channel identifier:", 8, 50, self.__utils.decryptDataWithAES(alert_rule_data["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
					alert_rule_data["telegram_chat_id"] = telegram_chat_id.decode("utf-8")
				self.__utils.createYamlFile(alert_rule_data, alert_rule_path)
				hash_alert_rule_new = self.__utils.getHashFunctionToFile(alert_rule_path)
				if hash_alert_rule_new == hash_alert_rule_actual:
					self.__dialog.createMessageDialog("\nAlert rule not modified: " + alert_rule_name_actual, 8, 50, "Notification Message")
				else:
					if flag_rename_alert_rule == 1:
						self.__utils.renameFileOrFolder(alert_rule_path, self.__folder_alert_rules_path + '/' + alert_rule_name + ".yaml")	
					self.__dialog.createMessageDialog("\nAlert rule modified: " + alert_rule_name_actual, 8, 50, "Notification Message")
					self.__logger.generateApplicationLog("Alert rule modified: " + alert_rule_name_actual, 2, "__updateAlertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			else:
				self.__dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__updateAlertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nValue Error. For more information, see the logs.", 7, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateAlertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateAlertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def showAlertRuleData(self):
		"""
		Method that shows the data of a specific alert rule.
		"""
		try:
			list_all_alert_rules = self.__utils.getListOfAllYamlFilesInFolder(self.__folder_alert_rules_path)
			if list_all_alert_rules:
				dialog_list = self.__utils.convertListToDialogList(list_all_alert_rules, "Alert Rule's Name")
				alert_rule_to_show = self.__dialog.createRadioListDialog("Select a option:", 18, 70, dialog_list, "Alert Rules")
				alert_rule_data = self.__utils.convertDataYamlFileToString(self.__folder_alert_rules_path + '/' + alert_rule_to_show)
				message_to_display = '\n' + alert_rule_to_show[:-5] + "\n\n" + alert_rule_data
				self.__dialog.createScrollBoxDialog(message_to_display, 18, 70, "Alert Rule's Data")
			else:
				self.__dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
		except (OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__showDataAlertRule", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def deleteAlertRules(self):
		"""
		Method that delete one or more alert rules.
		"""
		try:
			list_all_alert_rules = self.__utils.getListOfAllYamlFilesInFolder(self.__folder_alert_rules_path)
			if list_all_alert_rules:
				dialog_list = self.__utils.convertListToDialogList(list_all_alert_rules, "Alert Rule's Name")
				list_alert_rules_remove = self.__dialog.createCheckListDialog("Select one or more options:", 18, 70, dialog_list, "Alert Rules")
				message_to_display = self.__utils.getStringFromList(list_alert_rules_remove, "Alert rules selected to remove:")
				self.__dialog.createScrollBoxDialog(message_to_display, 14, 50, "Delete Alert Rules")
				remove_alert_rules_confirmation = self.__dialog.createYesOrNoDialog("\nAre you sure to delete the selected alert rules?\n\n** This action cannot be undone.", 10, 50, "Delete Alert Rules")
				if remove_alert_rules_confirmation == "ok":
					for alert_rule in list_alert_rules_remove:
						self.__utils.deleteFile(self.__folder_alert_rules_path + '/' + alert_rule)
						self.__logger.generateApplicationLog("Alert rule deleted: " + alert_rule, 2, "__deleteAlertRules", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
				self.__dialog.createMessageDialog("\nAlert rules deleted.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
		except (OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__deleteAlertRules", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def showAllAlertRules(self):
		"""
		Method that displays all alert rules created.
		"""
		try:
			list_all_alert_rules = self.__utils.getListOfAllYamlFilesInFolder(self.__folder_alert_rules_path)
			if list_all_alert_rules:
				message_to_display = "\nAlert rules:\n"
				for alert_rule in list_all_alert_rules:
					message_to_display += "\n- " + alert_rule[:-5]
				self.__dialog.createScrollBoxDialog(message_to_display, 18, 50, "Show Alert Rules")
			else:
				self.__dialog.createMessageDialog("\nNo alert rules found.", 7, 50, "Notification Message")
		except (OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__showAlertRules", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def __createYamlFileAlertRule(self, alert_rule_data):
		"""
		Method that creates the YAML file corresponding to the new alert rule.

		:arg alert_rule_data (dict): Object containing the data that will be stored in the new alert rule.
		"""
		alert_rule_data_json = {
			"alert_rule_name" : alert_rule_data[0],
			"alert_rule_level" : alert_rule_data[1],
			"index_pattern_name" : alert_rule_data[2],
			"alert_rule_type" : alert_rule_data[3],
			"number_events_found_by_alert" : int(alert_rule_data[4]),
			"time_search" : {alert_rule_data[5] : int(alert_rule_data[6])},
			"time_range" : {alert_rule_data[7] : int(alert_rule_data[8])},
		}

		if alert_rule_data[9] == "aggregations":
			index_field_name_json = {"index_field_name" : alert_rule_data[10]}
			last_index = 10
		elif alert_rule_data[9] == "query_string":
			query_string_json = {alert_rule_data[9] : {"query" : alert_rule_data[10]}}
			alert_rule_data_json.update(query_string_json)
			if alert_rule_data[11] == True:
				fields_option_json = {"use_fields_option" : alert_rule_data[11], "fields_name" : alert_rule_data[12]}
				last_index = 12
			else:
				fields_option_json = {"use_fields_option" : alert_rule_data[11]}
				last_index = 11
			alert_rule_data_json.update(fields_option_json)
			if alert_rule_data[last_index + 1] == True:
				if alert_rule_data[last_index + 2] == True:
					restriction_by_hostname_json = {"restriction_by_hostname" : alert_rule_data[last_index + 2], "field_name_hostname" : alert_rule_data[last_index + 3], "number_total_events_by_hostname" : int(alert_rule_data[last_index + 4])}
					last_index += 4
				else:
					restriction_by_hostname_json = {"restriction_by_hostname" : alert_rule_data[last_index + 2]}
					last_index += 2
				alert_rule_data_json.update(restriction_by_hostname_json)
				if alert_rule_data[last_index + 1] == True:
					restriction_by_username_json = {"restriction_by_username" : alert_rule_data[last_index + 1], "field_name_username" : alert_rule_data[last_index + 2], "number_total_events_by_username" : int(alert_rule_data[last_index + 3])}
					last_index += 3
				else:
					restriction_by_username_json = {"restriction_by_username" : alert_rule_data[last_index + 1]}
					last_index += 1
				alert_rule_data_json.update(restriction_by_username_json)
				use_custom_rule_json = {"use_custom_rule_option" : True}
			else:
				use_custom_rule_json = {"use_custom_rule_option" : False}
				last_index += 1
			alert_rule_data_json.update(use_custom_rule_json)
			send_type_alert_json = {"send_type_alert_rule" : alert_rule_data[last_index + 1]}
			last_index += 1
		telegram_data_json = {"telegram_bot_token" : alert_rule_data[last_index + 1], "telegram_chat_id" : alert_rule_data[last_index + 2]}
		alert_rule_data_json.update(telegram_data_json)

		alert_rule_path = self.__folder_alert_rules_path + '/' + alert_rule_data[0] + ".yaml"
		self.__utils.createYamlFile(alert_rule_data_json, alert_rule_path)
		self.__utils.changeOwnerToPath(alert_rule_path, self.__constants.USER, self.__constants.GROUP)