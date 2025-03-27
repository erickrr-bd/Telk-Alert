from os import path
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

	name: str = None
	level: str = None
	index_pattern: str = None
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
		use_fields_yn = self.dialog.create_yes_or_no("\nIs the selection of specific fields required for the alert?", 8, 50, "Fields Selection")
		if use_fields_yn == "ok":
			self.use_fields = True
			total_fields = self.dialog.create_integer_inputbox("Enter the total fields:", 8, 50, "1")
			tuple_to_form = self.utils.generate_tuple_to_form(int(total_fields), "Field Name")
			self.fields = self.dialog.create_form("Enter the field's names:", tuple_to_form, 15, 50, "Fields", False)


	def define_telegram_bot_token(self, key_file: str) -> None:
		"""
		Method that defines the Telegram Bot Token.
		"""
		passphrase = self.utils.get_passphrase(key_file)
		self.telegram_bot_token = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)


	def define_telegram_chat_id(self, key_file: str) -> None:
		"""
		Method that defines the Telegram Chat ID.
		"""
		passphrase = self.utils.get_passphrase(key_file)
		self.telegram_chat_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, "-1002365478941"), passphrase)


	def convert_object_to_dict(self) -> dict:
		"""
		Method that converts an object of type AlertRules into a dictionary.

		Returns:
			alert_rule_data_json (dict): Dictionary with the object's data.
		"""
		alert_rule_data_json = {
			"name" :  self.name,
			"level" :  self.level,
			"index_pattern" : self.index_pattern,
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


	def create_file(self, alert_rule_data: dict, log_file_name: str, user: str = None, group: str = None) -> None:
		"""
		Method that creates the YAML file corresponding to the alert rule.

		Parameters:
			alert_rule_data (dict): Data to save in the YAML file.
			log_file_name (str): Log file path.
			user (str): Owner user.
			group (str): Owner group.
		"""
		try:
			alert_rule_path = f"{self.constants.ALERT_RULES_FOLDER}/{alert_rule_data["name"]}.yaml"
			self.utils.create_yaml_file(alert_rule_data, alert_rule_path)
			self.utils.change_owner(alert_rule_path, user, group, "644")
			if path.exists(alert_rule_path):
				self.dialog.create_message(f"\nAlert rule created: {alert_rule_data["name"]}", 7, 50, "Notification Message")
				self.logger.create_log(f"Alert rule created: {alert_rule_data["name"]}", 2, "__createAlertRule", use_file_handler = True, file_name = log_file_name, user = user, group = group)
		except Exception as exception:
			self.dialog.create_message("\nError creating alert rule. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createAlertRule", use_file_handler = True, file_name = log_file_name, user = user, group = group)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")