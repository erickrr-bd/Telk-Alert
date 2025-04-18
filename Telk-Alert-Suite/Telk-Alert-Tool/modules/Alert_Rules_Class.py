from os import path
from json import dumps
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from dataclasses import dataclass, field

@dataclass
class AlertRules:
	"""
	Class that manages everything related to alert rules.
	"""

	is_custom_rule: bool = False
	name: str = None
	level: str = None
	index_pattern: str = None
	timestamp_field: str = None
	total_events: int = 0
	search_time: dict = field(default_factory = dict)
	range_time: dict = field(default_factory = dict)
	query: dict = field(default_factory = dict)
	use_fields: bool = False
	fields: list = field(default_factory = list)
	telegram_bot_token: tuple = field(default_factory = tuple)
	telegram_chat_id: tuple = field(default_factory = tuple)


	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def define_name(self) -> None:
		"""
		Method that defines the name of the new alert rule.
		"""
		self.name = self.dialog.create_filename_inputbox("Enter the name of the alert rule:", 8, 50, "rule1")


	def define_level(self) -> None:
		"""
		Method that defines the level of the new alert rule.
		"""
		self.level = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.ALERT_RULE_LEVEL, "Alert Rule Level")


	def define_index_pattern(self) -> None:
		"""
		Method that defines the index pattern of the alert rule.
		"""
		self.index_pattern = self.dialog.create_inputbox("Enter the index pattern:", 8, 50, "winlogbeat-*")


	def define_timestamp_field(self) -> None:
		"""
		Method that defines the name of the field corresponding to the index timestamp.
		"""
		self.timestamp_field = self.dialog.create_inputbox("Enter the name of the field that corresponds to the index timestamp:", 9, 50, "@timestamp")


	def define_total_events(self) -> None:
		"""
		Method that defines the total number of events that will trigger the alert rule.
		"""
		self.total_events = int(self.dialog.create_integer_inputbox("Enter the total events to which the alert will be sent:", 9, 50, "1"))


	def define_search_time(self) -> None:
		"""
		Method that defines how often the search will be repeated.
		"""
		option = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.UNIT_TIME, "Unit Time")
		total_time = self.dialog.create_integer_inputbox(f"Enter the total in {option} that the search will be repeated:", 9, 50, "1")
		self.search_time = {option : int(total_time)}


	def define_range_time(self) -> None:
		"""
		Method that defines the time range from the current moment in which the event search will be performed.
		"""
		option = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.UNIT_TIME, "Unit Time")
		size = 9 if option == "minutes" else 8
		total_time = self.dialog.create_integer_inputbox(f"Enter the total in {option} of the search range:", size, 50, "1")
		self.range_time = {option : int(total_time)}


	def define_query_type(self) -> None:
		"""
		Method that defines the type of query to use for the search.
		"""
		option = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.QUERY_TYPE, "Unit Time")
		if option == "query_string":
			query_string = self.dialog.create_inputbox("Enter the query string:", 8, 50, "event.code: 4625")
			self.query = {"query_type" : [{"query_string" : {"query" : query_string}}]}


	def define_use_fields(self) -> None:
		"""
		Method that defines whether the search result will be limited to specific fields.
		"""
		use_fields_yn = self.dialog.create_yes_or_no("\nIs the selection of specific field(s) required for the alert?", 8, 50, "Field(s) Selection")
		if use_fields_yn == "ok":
			self.use_fields = True
			total_fields = self.dialog.create_integer_inputbox("Enter the total field(s):", 8, 50, "1")
			tuple_to_form = self.utils.generate_tuple_to_form(int(total_fields), "Field Name")
			self.fields = self.dialog.create_form("Enter the field's names:", tuple_to_form, 15, 50, "Field(s)", False)


	def define_telegram_bot_token(self) -> None:
		"""
		Method that defines the Telegram Bot Token.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_bot_token = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)


	def define_telegram_chat_id(self) -> None:
		"""
		Method that defines the Telegram Chat ID.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_chat_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, "-1002365478941"), passphrase)


	def convert_object_to_dict(self) -> dict:
		"""
		Method that converts an object of type AlertRules into a dictionary.

		Returns:
			alert_rule_data_json (dict): Dictionary with the object's data.
		"""
		alert_rule_data_json = {
			"is_custom_rule" : self.is_custom_rule,
			"name" :  self.name,
			"level" :  self.level,
			"index_pattern" : self.index_pattern,
			"timestamp_field" : self.timestamp_field,
			"total_events" : self.total_events,
			"search_time" : self.search_time,
			"range_time" : self.range_time,
			"query" : self.query,
			"use_fields" : self.use_fields
		}

		if self.use_fields:
			alert_rule_data_json.update({"fields" : self.fields})
		alert_rule_data_json.update({"telegram_bot_token" : self.telegram_bot_token, "telegram_chat_id" : self.telegram_chat_id})
		return alert_rule_data_json


	def create_file(self, alert_rule_data: dict) -> None:
		"""
		Method that creates the YAML file corresponding to the alert rule.

		Parameters:
			alert_rule_data (dict): Data to save in the YAML file.
		"""
		try:
			alert_rule_path = f"{self.constants.ALERT_RULES_FOLDER}/{alert_rule_data["name"]}.yaml"
			self.utils.create_yaml_file(alert_rule_data, alert_rule_path)
			self.utils.change_owner(alert_rule_path, self.constants.USER, self.constants.GROUP, "644")
			if path.exists(alert_rule_path):
				self.dialog.create_message(f"\nAlert rule created: {alert_rule_data["name"]}", 7, 50, "Notification Message")
				self.logger.create_log(f"Alert rule created: {alert_rule_data["name"]}", 2, "__createAlertRule", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.create_message("\nError creating alert rule. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createAlertRule", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def convert_dict_to_object(self, alert_rule_data: dict) -> None:
		"""
		Method that converts a dictionary into an object of type AlertRules.

		Parameters:
			alert_rule_data (dict): Dictionary to convert.
		"""
		self.is_custom_rule = alert_rule_data["is_custom_rule"]
		self.name = alert_rule_data["name"]
		self.level = alert_rule_data["level"]
		self.index_pattern = alert_rule_data["index_pattern"]
		self.timestamp_field = alert_rule_data["timestamp_field"]
		self.total_events = alert_rule_data["total_events"]
		unit_time = list(alert_rule_data["search_time"].keys())[0]
		self.search_time = {unit_time : alert_rule_data["search_time"][unit_time]}
		unit_time = list(alert_rule_data["range_time"].keys())[0]
		self.range_time = {unit_time : alert_rule_data["range_time"][unit_time]}
		query_type = list(alert_rule_data["query"]["query_type"][0].keys())[0]
		if query_type == "query_string":
			query_string = alert_rule_data["query"]["query_type"][0]["query_string"]["query"]
			self.query = {"query_type" : [{"query_string" : {"query" : query_string}}]}
		self.use_fields = alert_rule_data["use_fields"]
		if alert_rule_data["use_fields"]:
			self.fields = alert_rule_data["fields"]
		self.telegram_bot_token  = alert_rule_data["telegram_bot_token"]
		self.telegram_chat_id = alert_rule_data["telegram_chat_id"]


	def modify_alert_rule(self) -> None:
		"""
		Method that modifies the configuration of an alert rule.
		"""
		try:
			alert_rules = self.utils.get_yaml_files_in_folder(self.constants.ALERT_RULES_FOLDER)
			if alert_rules:
				alert_rules.sort()
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(alert_rules, "Alert Rule Name")
				option = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Alert Rule(s)")
				options = self.dialog.create_checklist("Select one or more options:", 18, 70, self.constants.ALERT_RULE_FIELDS, "Alert Rule Fields")
				alert_rule_data = self.utils.read_yaml_file(f"{self.constants.ALERT_RULES_FOLDER}/{option}")
				self.convert_dict_to_object(alert_rule_data)
				original_hash = self.utils.get_hash_from_file(f"{self.constants.ALERT_RULES_FOLDER}/{option}")
				if "Name" in options:
					self.modify_name()
				if "Level" in options:
					self.modify_level()
				if "Index" in options:
					self.modify_index_pattern()
				if "Timestamp" in options:
					self.modify_timestamp_field()
				if "Total Events" in options:
					self.modify_total_events()
				if "Search Time" in options:
					self.modify_search_time()
				if "Range Time" in options:
					self.modify_range_time()
				if "Query" in options:
					self.modify_query()
				if "Fields Selection" in options:
					self.modify_fields()
				if "Bot Token" in options:
					self.modify_telegram_bot_token()
				if "Chat ID" in options:
					self.modify_telegram_chat_id()
				alert_rule_data = self.convert_object_to_dict()
				self.utils.create_yaml_file(alert_rule_data, f"{self.constants.ALERT_RULES_FOLDER}/{self.name}.yaml")
				new_hash = self.utils.get_hash_from_file(f"{self.constants.ALERT_RULES_FOLDER}/{self.name}.yaml")
				self.dialog.create_message("\nAlert rule not modified.", 7, 50, "Notification Message") if new_hash == original_hash else self.dialog.create_message("\nAlert rule modified.", 7, 50, "Notification Message")
			else:
				self.dialog.create_message(f"\nNo alert rule(s) in: {self.constants.ALERT_RULES_FOLDER}", 8, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError modifying alert rule configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_modifyAlertRule", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def modify_name(self) -> None:
		"""
		Method that modifies the name of an alert rule.
		"""
		old_name = self.name
		new_name = self.dialog.create_filename_inputbox("Enter the name of the alert rule:", 8, 50, old_name)
		if new_name == old_name:
			self.dialog.create_message("\nThe name cannot be the same as the previous one.", 8, 50, "Notification Message")
		else:
			self.utils.rename_file_or_folder(f"{self.constants.ALERT_RULES_FOLDER}/{old_name}.yaml", f"{self.constants.ALERT_RULES_FOLDER}/{new_name}.yaml")
			self.name = new_name
			self.logger.create_log(f"Alert rule name modified: {new_name}", 3, f"_{old_name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_level(self) -> None:
		"""
		Method that modifies the criticality level of an alert rule.
		"""
		for level in self.constants.ALERT_RULE_LEVEL:
			if level[0] == self.level:
				level[2] = 1
			else:
				level[2] = 0
		self.level = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.ALERT_RULE_LEVEL, "Alert Rule Level")
		self.logger.create_log(f"Alert rule level modified: {self.level}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_index_pattern(self) -> None:
		"""
		Method that modifies the index pattern.
		"""
		self.index_pattern = self.dialog.create_inputbox("Enter the index pattern:", 8, 50, self.index_pattern)
		self.logger.create_log(f"Index pattern modified: {self.index_pattern}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_timestamp_field(self) -> None:
		"""
		Method that modifies the name of the field corresponding to the index timestamp.
		"""
		self.timestamp_field = self.dialog.create_inputbox("Enter the name of the field that corresponds to the index timestamp:", 9, 50, self.timestamp_field)
		self.logger.create_log(f"Timestamp's field modified: {self.timestamp_field}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_total_events(self) -> None:
		"""
		Method that modifies the total number of events to which the alert is sent.
		"""
		self.total_events = int(self.dialog.create_integer_inputbox("Enter the total events to which the alert will be sent:", 9, 50, str(self.total_events)))
		self.logger.create_log(f"Total events modified: {self.total_events}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_search_time(self) -> None:
		"""
		Method that modifies the frequency with which the search is repeated.
		"""
		old_unit_time = list(self.search_time.keys())[0]

		for unit in self.constants.UNIT_TIME:
			if unit[0] == old_unit_time:
				unit[2] = 1
			else:
				unit[2] = 0

		option = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.UNIT_TIME, "Unit Time")
		total_time = self.dialog.create_integer_inputbox(f"Enter the total in {option} that the search will be repeated:", 9, 50, str(self.search_time[old_unit_time]))
		self.search_time = {option : int(total_time)}
		self.logger.create_log(f"Search time modified: {self.search_time}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_range_time(self) -> None:
		"""
		Method that modifies the search time range.
		"""
		old_unit_time = list(self.range_time.keys())[0]

		for unit in self.constants.UNIT_TIME:
			if unit[0] == old_unit_time:
				unit[2] = 1
			else:
				unit[2] = 0

		option = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.UNIT_TIME, "Unit Time")
		size = 9 if option == "minutes" else 8
		total_time = self.dialog.create_integer_inputbox(f"Enter the total in {option} of the search range:", size, 50, str(self.range_time[old_unit_time]))
		self.range_time = {option : int(total_time)}
		self.logger.create_log(f"Range time modified: {self.range_time}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_query(self) -> None:
		"""
		Method that modifies the query used for the search.
		"""
		query_type = list(self.query["query_type"][0].keys())[0]
		if query_type == "query_string":
			query_string = self.dialog.create_inputbox("Enter the query string:", 8, 50, self.query["query_type"][0]["query_string"]["query"])
			self.query = {"query_type" : [{"query_string" : {"query" : query_string}}]}
			self.logger.create_log(f"Query string changed: {query_string}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_fields(self) -> None:
		"""
		Method that modifies the option of using fields for the search response.
		"""
		if self.use_fields:
			option = self.dialog.create_radiolist("Select a option:", 9, 55, self.constants.OPTIONS_FIELDS_TRUE, "Field(s) Option")
			if option == "Disable":
				self.use_fields = False
				self.fields = None
				self.logger.create_log("Field(s) option has been disabled", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			elif option == "Fields":
				option = self.dialog.create_menu("Select a option:", 10, 50, self.constants.FIELDS_OPTIONS, "Field(s) Menu")
				match option:
					case "1":
						total_fields = self.dialog.create_integer_inputbox("Enter the total field(s):", 8, 50, "1")
						tuple_to_form = self.utils.generate_tuple_to_form(int(total_fields), "Field Name")
						fields = self.dialog.create_form("Enter the field's names:", tuple_to_form, 15, 50, "Add Field(s)", False)
						self.fields.extend(fields)
						self.logger.create_log(f"Added field(s): {','.join(fields)}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
					case "2":
						tuple_to_form = self.utils.convert_list_to_tuple(self.fields, "Field Name")
						self.fields = self.dialog.create_form("Enter the field's names:", tuple_to_form, 15, 50, "Modify Field(s)", False)
						self.logger.create_log(f"Modified field(s): {','.join(self.fields)}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
					case "3":
						tuple_to_rc = self.utils.convert_list_to_tuple_rc(self.fields, "Field Name")
						options = self.dialog.create_checklist("Select one or more options:", 15, 50, tuple_to_rc, "Remove Field(s)")
						text = self.utils.get_str_from_list(options, "Selected Field(s):")
						self.dialog.create_scrollbox(text, 15, 60, "Remove Field(s)")
						fields_yn = self.dialog.create_yes_or_no("\nAre you sure to remove the selected field(s)?\n\n** This action cannot be undone.", 9, 50, "Remove Field(s)")
						if fields_yn == "ok":
							[self.fields.remove(option) for option in options]
						self.logger.create_log(f"Removed field(s): {','.join(options)}", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		else:
			option = self.dialog.create_radiolist("Select a option:", 8, 55, self.constants.OPTIONS_FIELDS_FALSE, "Field(s) Option")
			if option == "Enable":
				self.use_fields = True
				total_fields = self.dialog.create_integer_inputbox("Enter the total field(s):", 8, 50, "1")
				tuple_to_form = self.utils.generate_tuple_to_form(int(total_fields), "Field Name")
				self.fields = self.dialog.create_form("Enter the field's names:", tuple_to_form, 15, 50, "Field(s)", False)
				self.logger.create_log("Field(s) option has been enabled", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_telegram_bot_token(self) -> None:
		"""
		Method that modifies the Telegram Bot Token.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_bot_token = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, self.utils.decrypt_data(self.telegram_bot_token, passphrase).decode("utf-8")), passphrase)
		self.logger.create_log("Telegram Bot Token modified.", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_telegram_chat_id(self) -> None:
		"""
		Method that modifies the Telegram Chat ID.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_chat_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, self.utils.decrypt_data(self.telegram_chat_id, passphrase).decode("utf-8")), passphrase)
		self.logger.create_log("Telegram Chat ID modified.", 3, f"_{self.name}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def display_configuration(self) -> None:
		"""
		Method that displays the configuration of an alert rule.
		"""
		try:
			alert_rules = self.utils.get_yaml_files_in_folder(self.constants.ALERT_RULES_FOLDER)
			if alert_rules:
				alert_rules.sort()
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(alert_rules, "Alert Rule Name")
				option = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Alert Rules")
				alert_rule_str = self.utils.convert_yaml_to_str(f"{self.constants.ALERT_RULES_FOLDER}/{option}")
				text = f"\n{option[:-5]}\n\n{alert_rule_str}"
				self.dialog.create_scrollbox(text, 18, 70, "Alert Rule Configuration") 
			else:
				self.dialog.create_message(f"\nNo alert rules in: {self.constants.ALERT_RULES_FOLDER}", 8, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError displaying alert rule configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_displayAlertRuleConfig", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def delete_alert_rules(self) -> None:
		"""
		Method that deletes one or more alert rules.
		"""
		try:
			alert_rules = self.utils.get_yaml_files_in_folder(self.constants.ALERT_RULES_FOLDER)
			if alert_rules:
				alert_rules.sort()
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(alert_rules, "Alert Rule Name")
				options = self.dialog.create_checklist("Select one or more options::", 18, 70, tuple_to_rc, "Delete Alert Rules")
				text = self.utils.get_str_from_list(options, "Alert rules selected to remove:")
				self.dialog.create_scrollbox(text, 14, 50, "Delete Alert Rules")
				delete_alert_rules_yn = self.dialog.create_yes_or_no("\nAre you sure to delete the selected alert rules?\n\n**Note: This action cannot be undone.", 10, 50, "Delete Alert Rules")
				if delete_alert_rules_yn == "ok":
					[self.utils.delete_file(f"{self.constants.ALERT_RULES_FOLDER}/{alert_rule}") for alert_rule in options]
					self.dialog.create_message("\nAlert rule(s) deleted.", 7, 50, "Notification Message")
					self.logger.create_log(f"Alert rule(s) deleted: {','.join(options)}", 3, "_deleteAlertRules", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			else:
				self.dialog.create_message(f"\nNo alert rules in: {self.constants.ALERT_RULES_FOLDER}", 8, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError deleting alert rule(s). For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_deleteAlertRules", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def disable_alert_rule(self)-> None:
		"""
		Method that disables one or more alert rules.
		"""
		try:
			alert_rules = self.utils.get_yaml_files_in_folder(self.constants.ALERT_RULES_FOLDER)
			if alert_rules:
				alert_rules.sort()
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(alert_rules, "Alert Rule Name")
				options = self.dialog.create_checklist("Select one or more options::", 18, 70, tuple_to_rc, "Disable Alert Rules")
				text = self.utils.get_str_from_list(options, "Alert rules selected to disable:")
				self.dialog.create_scrollbox(text, 14, 50, "Disable Alert Rules")
				disable_alert_rules_yn = self.dialog.create_yes_or_no("\nAre you sure to disable the selected alert rules?", 8, 50, "Disable Alert Rules")
				if disable_alert_rules_yn == "ok":
					[self.utils.rename_file_or_folder(f"{self.constants.ALERT_RULES_FOLDER}/{alert_rule}", f"{self.constants.ALERT_RULES_FOLDER}/{alert_rule}.bck") for alert_rule in options]
					self.dialog.create_message("\nAlert rule(s) disabled.", 7, 50, "Notification Message")
					self.logger.create_log(f"Alert rule(s) disabled: {','.join(options)}", 3, "_disableAlertRules", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			else:
				self.dialog.create_message(f"\nNo alert rules in: {self.constants.ALERT_RULES_FOLDER}", 8, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError disabling alert rule(s). For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_disableAlertRules", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def enable_alert_rule(self)-> None:
		"""
		Method that enables one or more alert rules.
		"""
		try:
			alert_rules = self.utils.get_bck_files_in_folder(self.constants.ALERT_RULES_FOLDER)
			if alert_rules:
				alert_rules.sort()
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(alert_rules, "Alert Rule Name")
				options = self.dialog.create_checklist("Select one or more options::", 18, 70, tuple_to_rc, "Enable Alert Rules")
				text = self.utils.get_str_from_list(options, "Alert rules selected to enable:")
				self.dialog.create_scrollbox(text, 14, 50, "Enable Alert Rules")
				enable_alert_rules_yn = self.dialog.create_yes_or_no("\nAre you sure to enable the selected alert rules?", 8, 50, "Enable Alert Rules")
				if enable_alert_rules_yn == "ok":
					[self.utils.rename_file_or_folder(f"{self.constants.ALERT_RULES_FOLDER}/{alert_rule}", f"{self.constants.ALERT_RULES_FOLDER}/{alert_rule[:-4]}") for alert_rule in options]
					self.dialog.create_message("\nAlert rule(s) enabled.", 7, 50, "Notification Message")
					self.logger.create_log(f"Alert rule(s) enabled: {','.join(options)}", 3, "_enableAlertRules", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			else:
				self.dialog.create_message(f"\nNo disabled alert rules in: {self.constants.ALERT_RULES_FOLDER}", 8, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError enabling alert rule(s). For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_enableAlertRules", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def display_alert_rules(self) -> None:
		"""
		Method that shows all created alert rules.
		"""
		try:
			alert_rules = self.utils.get_yaml_files_in_folder(self.constants.ALERT_RULES_FOLDER)
			if alert_rules:
				alert_rules.sort()
				text = "\nAlert Rules\n"
				for alert_rule in alert_rules:
					text += "\n-" + alert_rule[:-5]
				self.dialog.create_scrollbox(text, 18, 70, "Alert Rules")
			else:
				self.dialog.create_message(f"\nNo alert rules in: {self.constants.ALERT_RULES_FOLDER}", 8, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError displaying alert rule(s). For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_deleteAlertRules", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")
