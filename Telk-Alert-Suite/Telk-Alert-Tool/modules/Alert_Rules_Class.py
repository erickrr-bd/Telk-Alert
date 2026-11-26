"""
Class that manages everything related to Alert Rules.
"""
import re
from os import path
from copy import deepcopy
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog, DialogCancelled
from .Constants_Class import Constants

# Only the classes are exported by the libraries' packages, so the validations are defined here.
# Valid name of an ElasticSearch field.
FIELD_REGEX = re.compile(r"^[A-Za-z0-9_@.\-]+$")

# Valid alert rule's name (same rule as libPyDialog.create_filename_inputbox).
FILENAME_REGEX = re.compile(r'^[^\\/?%*:|"<>]+$')

# Telegram Bot Token (<id>:<hash>) and Chat ID (integer, negative for groups, or @channel).
TOKEN_REGEX = re.compile(r"^\d{5,}:[A-Za-z0-9_-]{30,}$")
CHAT_ID_REGEX = re.compile(r"^(-?\d+|@[A-Za-z0-9_]{5,})$")

# Maximum total accepted for each unit of time.
MAX_TOTAL_BY_UNIT = {"minutes": 1440, "hours": 720, "days": 365}

LEVELS = tuple(level for level, _ in Constants.ALERT_RULE_LEVEL)


class AlertRules:

	def __init__(self, dialog: libPyDialog, logger: libPyLog, utils: libPyUtils) -> None:
		"""
		Class constructor.

		Parameters:
			dialog (libPyDialog): Shared dialog instance.
			logger (libPyLog): Shared logger instance.
			utils (libPyUtils): Shared utilities instance.
		"""
		self.dialog = dialog
		self.logger = logger
		self.utils = utils
		self.name = None
		self.level = None
		self.index_pattern = None
		self.timestamp_field = None
		self.total_events = 0
		self.search_time = {}
		self.range_time = {}
		self.query = {}
		self.use_fields = False
		self.fields = []
		self.telegram_bot_token = ()
		self.telegram_chat_id = ()


	# --- Internal helpers ----------------------------------------------------------------------
	def _log(self, message, detail: str = "", level: int = 3, tag: str = "_modifyAlertRule") -> None:
		"""
		Method that writes an entry in the log file (fixed tag: one logger, one file handler).
		"""
		text = f"{message}: {detail}" if detail else message
		self.logger.create_log(text, level, tag, use_file_handler = True, file_name = Constants.LOG_FILE, user = Constants.USER, group = Constants.GROUP)


	def _error(self, text: str, tag: str, exception: Exception) -> None:
		"""
		Method that displays an error message and writes the exception in the log file.
		"""
		self.dialog.create_message(text, 8, 50, "Error Message")
		self._log(exception, level = 4, tag = tag)


	@staticmethod
	def _choices(options: tuple, selected: str) -> list:
		"""
		Method that builds radiolist choices marking the selected option (the constants are never modified).
		"""
		return [(tag, description, 1 if tag == selected else 0) for tag, description in options]


	@staticmethod
	def _rule_file(name: str) -> str:
		return path.join(Constants.ALERT_RULES_FOLDER, f"{name}.yaml")


	def _rule_exists(self, name: str) -> bool:
		"""
		Method that checks whether an alert rule (enabled or disabled) already exists.
		"""
		rule_file = self._rule_file(name)
		return path.exists(rule_file) or path.exists(rule_file + ".disabled")


	@staticmethod
	def _valid_name(name) -> bool:
		return (isinstance(name, str) and FILENAME_REGEX.fullmatch(name) is not None
			and name not in (".", "..") and len(name) <= 200 and not any(ord(char) < 32 for char in name))


	def _list_rules(self, disabled: bool = False) -> list:
		"""
		Method that returns the sorted alert rules (or shows a message if there are none).
		"""
		folder = Constants.ALERT_RULES_FOLDER
		rules = sorted(self.utils.get_disabled_files_in_folder(folder) if disabled else self.utils.get_yaml_files_in_folder(folder))
		if not rules:
			self.dialog.create_message(f"\nNo {'disabled ' if disabled else ''}alert rules in: {folder}", 8, 50, "Notification Message")
		return rules


	def _select_rule(self, title: str) -> str | None:
		"""
		Method that asks for one alert rule (file name).
		"""
		rules = self._list_rules()
		if not rules:
			return None
		return self.dialog.create_radiolist("Select a option:", 18, 70, self.utils.convert_list_to_tuple_rc(rules, "Alert Rule's Name"), title)


	def _confirm_selection(self, items: list, item_text: str, title: str, question: str) -> list:
		"""
		Method that asks for one or more items, shows them and asks for confirmation.

		Returns:
			selected (list): Confirmed items (empty if the user said "No").
		"""
		selected = self.dialog.create_checklist("Select one or more options:", 18, 70, self.utils.convert_list_to_tuple_rc(items, item_text), title)
		self.dialog.create_scrollbox(self.utils.get_str_from_list(selected, "Selected:"), 14, 60, title)
		return list(selected) if self.dialog.create_yes_or_no(question, 10, 50, title) else []


	def _ask_time(self, prompt: str, selected_unit: str = "minutes", current_total: int = 1) -> dict:
		"""
		Method that asks for a unit of time and its total (with limits).
		"""
		unit = self.dialog.create_radiolist("Select a option:", 10, 50, self._choices(Constants.UNIT_TIME, selected_unit), "Unit Time")
		maximum = MAX_TOTAL_BY_UNIT[unit]
		total = self.dialog.create_integer_inputbox(f"{prompt} ({unit}, 1-{maximum}):", 10, 50, str(min(max(current_total, 1), maximum)), min_value = 1, max_value = maximum)
		return {unit: total}


	def _seconds(self, time_value: dict) -> int:
		unit, total = next(iter(time_value.items()))
		return self.utils.convert_time_to_seconds(unit, total)


	def _ensure_range_time(self) -> None:
		"""
		Method that makes sure the range time is not shorter than the search time (otherwise events are lost).
		"""
		while self._seconds(self.range_time) < self._seconds(self.search_time):
			self.dialog.create_message("\nThe range time must be greater than or equal to the search time.", 8, 55, "Error Message")
			unit, total = next(iter(self.range_time.items()))
			self.range_time = self._ask_time("Enter the total of the search range", unit, total)


	def _ask_fields(self, title: str, current: list | None = None) -> list:
		"""
		Method that asks for field names (new ones or editing the current ones). Duplicates are removed.
		"""
		if current is None:
			total = self.dialog.create_integer_inputbox(f"Enter the total field(s) (1-{Constants.MAX_FIELDS}):", 8, 50, "1", min_value = 1, max_value = Constants.MAX_FIELDS)
			tuple_to_form = self.utils.generate_tuple_to_form(total, "Field's Name")
		else:
			tuple_to_form = self.utils.convert_list_to_tuple(current, "Field's Name")
		fields = self.dialog.create_form("Enter the field's names:", tuple_to_form, 15, 50, title, validator = lambda value: FIELD_REGEX.fullmatch(value) is not None, error_message = "Invalid field name.")
		return list(dict.fromkeys(fields))


	def _encrypt_secret(self, prompt: str, title: str, field: str, validator, error_message: str) -> tuple:
		"""
		Method that asks for a secret (hidden input, no default value) and returns it encrypted.
		The passphrase and the plaintext are wiped from memory afterwards.
		"""
		value = self.dialog.create_passwordbox(prompt, 9, 60, True, title = title, validator = validator, error_message = error_message)
		buffer = bytearray(value.encode("utf-8"))
		passphrase = None
		try:
			passphrase = self.utils.get_passphrase(Constants.KEY_FILE, owner = Constants.USER)
			return self.utils.encrypt_data(buffer, passphrase, context = f"{Constants.CTX_ALERT_RULE}:{field}")
		finally:
			self.utils.zeroize(buffer)
			if passphrase is not None:
				self.utils.zeroize(passphrase)


	@staticmethod
	def _encrypted(data: dict, field: str):
		value = data.get(field)
		if not isinstance(value, (list, tuple)) or len(value) != 4 or not all(isinstance(item, bytes) for item in value):
			raise ValueError(f"Invalid {field}.")
		return value


	@staticmethod
	def _time_value(data: dict, key: str) -> dict:
		value = data.get(key)
		if not isinstance(value, dict) or len(value) != 1:
			raise ValueError(f"Invalid {key}.")
		unit, total = next(iter(value.items()))
		if unit not in MAX_TOTAL_BY_UNIT or isinstance(total, bool) or not isinstance(total, int) or not 1 <= total <= MAX_TOTAL_BY_UNIT[unit]:
			raise ValueError(f"Invalid {key}.")
		return {unit: total}


	@staticmethod
	def _query_value(data: dict) -> dict:
		try:
			query_string = data["query"]["query_type"][0]["query_string"]["query"]
		except (KeyError, IndexError, TypeError) as exception:
			raise ValueError("Invalid query.") from exception
		if not isinstance(query_string, str) or not query_string.strip():
			raise ValueError("Invalid query.")
		return {"query_type": [{"query_string": {"query": query_string}}]}


	# --- Definition ----------------------------------------------------------------------------
	def define_name(self) -> None:
		"""
		Method that defines the alert rule's name (it can't match an existing rule).
		"""
		while True:
			name = self.dialog.create_filename_inputbox("Enter the alert rule's name:", 8, 50, "rule1")
			if not self._rule_exists(name):
				self.name = name
				return
			self.dialog.create_message("\nAn alert rule with that name already exists.", 8, 50, "Error Message")


	def define_level(self) -> None:
		self.level = self.dialog.create_radiolist("Select a option:", 10, 50, self._choices(Constants.ALERT_RULE_LEVEL, "Low"), "Alert Rule Level")


	def define_index_pattern(self) -> None:
		self.index_pattern = self.dialog.create_inputbox("Enter the index pattern:", 8, 50, "winlogbeat-*")


	def define_timestamp_field(self) -> None:
		self.timestamp_field = self.dialog.create_inputbox("Enter the field's name that corresponds to the index timestamp:", 9, 50, "@timestamp")


	def define_total_events(self) -> None:
		self.total_events = self.dialog.create_integer_inputbox(f"Enter the total events to which the alert will be sent (1-{Constants.MAX_TOTAL_EVENTS}):", 9, 50, "1", min_value = 1, max_value = Constants.MAX_TOTAL_EVENTS)


	def define_search_time(self) -> None:
		self.search_time = self._ask_time("Enter the total that the search will be repeated")


	def define_range_time(self) -> None:
		self.range_time = self._ask_time("Enter the total of the search range")
		self._ensure_range_time()


	def define_query_type(self) -> None:
		option = self.dialog.create_radiolist("Select a option:", 8, 50, self._choices(Constants.QUERY_TYPE, "query_string"), "Query Type")
		if option == "query_string":
			query_string = self.dialog.create_inputbox("Enter the query string:", 8, 50, "event.code: 4625")
			self.query = {"query_type": [{"query_string": {"query": query_string}}]}


	def define_use_fields(self) -> None:
		if self.dialog.create_yes_or_no("\nIs the selection of specific fields required for the alert?", 8, 50, "Fields Selection"):
			self.fields = self._ask_fields("Fields")
			self.use_fields = True
		else:
			self.use_fields = False
			self.fields = []


	def define_telegram_bot_token(self) -> None:
		self.telegram_bot_token = self._encrypt_secret("Enter the Telegram Bot Token:", "Bot Token", "telegram_bot_token", lambda value: TOKEN_REGEX.fullmatch(value) is not None, "Invalid Telegram Bot Token (<id>:<hash>).")


	def define_telegram_chat_id(self) -> None:
		self.telegram_chat_id = self._encrypt_secret("Enter the Telegram Chat ID:", "Chat ID", "telegram_chat_id", lambda value: CHAT_ID_REGEX.fullmatch(value) is not None, "Invalid Telegram Chat ID (integer, negative for groups, or @channel).")


	# --- Conversion ----------------------------------------------------------------------------
	def convert_object_to_dict(self) -> dict:
		"""
		Method that converts an AlertRules's object into a dictionary.

		Returns:
			alert_rule_data_json (dict): Dictionary with the object's data.
		"""
		alert_rule_data_json = {
			"name": self.name,
			"level": self.level,
			"index_pattern": self.index_pattern,
			"timestamp_field": self.timestamp_field,
			"total_events": self.total_events,
			"search_time": self.search_time,
			"range_time": self.range_time,
			"query": self.query,
			"use_fields": self.use_fields,
			"telegram_bot_token": self.telegram_bot_token,
			"telegram_chat_id": self.telegram_chat_id
		}
		if self.use_fields:
			alert_rule_data_json["fields"] = self.fields
		return alert_rule_data_json


	def convert_dict_to_object(self, alert_rule_data: dict) -> None:
		"""
		Method that converts a dictionary into an AlertRules' object (the data is validated).

		Parameters:
			alert_rule_data (dict): Object that contains the alert rule's configuration data.
		"""
		if not isinstance(alert_rule_data, dict):
			raise ValueError("Invalid alert rule file.")
		if not self._valid_name(alert_rule_data.get("name")):
			raise ValueError("Invalid alert rule name.")
		if alert_rule_data.get("level") not in LEVELS:
			raise ValueError("Invalid level.")
		for key in ("index_pattern", "timestamp_field"):
			if not isinstance(alert_rule_data.get(key), str) or not alert_rule_data[key].strip():
				raise ValueError(f"Invalid {key}.")
		total_events = alert_rule_data.get("total_events")
		if isinstance(total_events, bool) or not isinstance(total_events, int) or not 0 <= total_events <= Constants.MAX_TOTAL_EVENTS:
			raise ValueError("Invalid total_events.")
		use_fields = alert_rule_data.get("use_fields")
		if not isinstance(use_fields, bool):
			raise ValueError("Invalid use_fields.")
		fields = alert_rule_data.get("fields") if use_fields else []
		if use_fields and (not isinstance(fields, list) or not fields or not all(isinstance(item, str) and item.strip() for item in fields)):
			raise ValueError("Invalid fields.")
		search_time = self._time_value(alert_rule_data, "search_time")
		range_time = self._time_value(alert_rule_data, "range_time")
		query = self._query_value(alert_rule_data)
		telegram_bot_token = self._encrypted(alert_rule_data, "telegram_bot_token")
		telegram_chat_id = self._encrypted(alert_rule_data, "telegram_chat_id")
		self.name = alert_rule_data["name"]
		self.level = alert_rule_data["level"]
		self.index_pattern = alert_rule_data["index_pattern"]
		self.timestamp_field = alert_rule_data["timestamp_field"]
		self.total_events = total_events
		self.search_time = search_time
		self.range_time = range_time
		self.query = query
		self.use_fields = use_fields
		self.fields = fields
		self.telegram_bot_token = telegram_bot_token
		self.telegram_chat_id = telegram_chat_id


	# --- File management -----------------------------------------------------------------------
	def create_file(self, alert_rule_data: dict) -> None:
		"""
		Method that creates the YAML file corresponding to the alert rule (an existing rule is never overwritten).

		Parameters:
			alert_rule_data (dict): Object that contains the alert rule's configuration data.
		"""
		try:
			name = alert_rule_data["name"]
			if self._rule_exists(name):
				self.dialog.create_message("\nAn alert rule with that name already exists.", 8, 50, "Error Message")
				return
			rule_file = self._rule_file(name)
			self.utils.create_yaml_file(alert_rule_data, rule_file)
			self.utils.change_owner(rule_file, Constants.USER, Constants.GROUP, "640")
			self._log("Alert rule created", name, level = 2, tag = "_createAlertRule")
			self.dialog.create_message(f"\nAlert rule created: {name}", 7, 50, "Notification Message")
		except DialogCancelled:
			pass
		except Exception as exception:
			self._error("\nError creating alert rule. For more information, see the logs.", "_createAlertRule", exception)


	def modify_alert_rule(self) -> None:
		"""
		Method that modifies the alert rule's configuration.
		"""
		try:
			option = self._select_rule("Alert Rule(s)")
			if option is None:
				return
			rule_file = path.join(Constants.ALERT_RULES_FOLDER, option)
			original_data = self.utils.read_yaml_file(rule_file)
			self._modify(rule_file, option, original_data)
		except DialogCancelled:
			pass
		except Exception as exception:
			self._error("\nError modifying alert rule's configuration. For more information, see the logs.", "_modifyAlertRule", exception)


	def _modify(self, rule_file: str, option: str, original_data: dict) -> None:
		"""
		Method that applies the chosen modifications and saves the rule only if something changed.
		The path is always built from the selected file, never from the YAML content.
		"""
		self.convert_dict_to_object(deepcopy(original_data))
		self.name = option.removesuffix(".yaml")
		options = self.dialog.create_checklist("Select one or more options:", 18, 70, Constants.ALERT_RULE_FIELDS, "Alert Rule's Fields")
		self.modify_rule_configuration(options)
		new_data = self.convert_object_to_dict()
		if new_data == original_data:
			self.dialog.create_message("\nAlert rule not modified.", 7, 50, "Notification Message")
			return
		new_file = self._rule_file(self.name)
		self.utils.create_yaml_file(new_data, new_file)
		self.utils.change_owner(new_file, Constants.USER, Constants.GROUP, "640")
		if new_file != rule_file:
			self.utils.delete_file(rule_file)
		self._log("Alert rule modified", self.name)
		self.dialog.create_message("\nAlert rule modified.", 7, 50, "Notification Message")


	# --- Modification --------------------------------------------------------------------------
	def _modify_actions(self) -> dict:
		"""
		Method that maps each checklist option to its modification method.
		"""
		return {
			"Name": self.modify_name,
			"Level": self.modify_level,
			"Index": self.modify_index_pattern,
			"Timestamp": self.modify_timestamp_field,
			"Total Events": self.modify_total_events,
			"Search Time": self.modify_search_time,
			"Range Time": self.modify_range_time,
			"Query": self.modify_query,
			"Fields Selection": self.modify_fields,
			"Bot Token": self.modify_telegram_bot_token,
			"Chat ID": self.modify_telegram_chat_id
		}


	def modify_rule_configuration(self, options: list) -> None:
		"""
		Method that modifies the Alert Rule's configuration.

		Parameters:
			options (list): Chosen options.
		"""
		for tag, action in self._modify_actions().items():
			if tag in options:
				action()
		if "Search Time" in options or "Range Time" in options:
			self._ensure_range_time()


	def modify_name(self) -> None:
		"""
		Method that modifies the alert rule's name (the file is renamed when the rule is saved).
		"""
		new_name = self.dialog.create_filename_inputbox("Enter the alert rule's name:", 8, 50, self.name)
		if new_name == self.name:
			self.dialog.create_message("\nThe name cannot be the same as the previous one.", 8, 50, "Notification Message")
			return
		if self._rule_exists(new_name):
			self.dialog.create_message("\nAn alert rule with that name already exists.", 8, 50, "Error Message")
			return
		self._log("Alert rule's name modified", f"{self.name} -> {new_name}")
		self.name = new_name


	def modify_level(self) -> None:
		self.level = self.dialog.create_radiolist("Select a option:", 10, 50, self._choices(Constants.ALERT_RULE_LEVEL, self.level), "Alert Rule's Level")
		self._log("Alert rule's level modified", f"{self.name}: {self.level}")


	def modify_index_pattern(self) -> None:
		self.index_pattern = self.dialog.create_inputbox("Enter the index pattern:", 8, 50, self.index_pattern)
		self._log("Index pattern modified", f"{self.name}: {self.index_pattern}")


	def modify_timestamp_field(self) -> None:
		self.timestamp_field = self.dialog.create_inputbox("Enter the field's name that corresponds to the index timestamp:", 9, 50, self.timestamp_field)
		self._log("Timestamp's field modified", f"{self.name}: {self.timestamp_field}")


	def modify_total_events(self) -> None:
		self.total_events = self.dialog.create_integer_inputbox(f"Enter the total events to which the alert will be sent (1-{Constants.MAX_TOTAL_EVENTS}):", 9, 50, str(max(self.total_events, 1)), min_value = 1, max_value = Constants.MAX_TOTAL_EVENTS)
		self._log("Total events modified", f"{self.name}: {self.total_events}")


	def modify_search_time(self) -> None:
		unit, total = next(iter(self.search_time.items()))
		self.search_time = self._ask_time("Enter the total that the search will be repeated", unit, total)
		self._log("Search time modified", f"{self.name}: {self.search_time}")


	def modify_range_time(self) -> None:
		unit, total = next(iter(self.range_time.items()))
		self.range_time = self._ask_time("Enter the total of the search range", unit, total)
		self._log("Range time modified", f"{self.name}: {self.range_time}")


	def modify_query(self) -> None:
		query_type = next(iter(self.query["query_type"][0]))
		match query_type:
			case "query_string":
				query_string = self.dialog.create_inputbox("Enter the query string:", 8, 50, self.query["query_type"][0]["query_string"]["query"])
				self.query = {"query_type": [{"query_string": {"query": query_string}}]}
				self._log("Query string changed", f"{self.name}: {query_string}")


	def modify_fields(self) -> None:
		"""
		Method that modifies the option of using fields for the search response.
		"""
		if not self.use_fields:
			self.dialog.create_radiolist("Select a option:", 8, 55, Constants.OPTIONS_FIELDS_FALSE, "Field(s) Option")
			self.fields = self._ask_fields("Field(s)")
			self.use_fields = True
			self._log("Field(s) option has been enabled", self.name)
			return

		option = self.dialog.create_radiolist("Select a option:", 9, 55, Constants.OPTIONS_FIELDS_TRUE, "Field(s) Option")
		if option == "Disable":
			self.use_fields = False
			self.fields = []
			self._log("Field(s) option has been disabled", self.name)
			return

		option = self.dialog.create_menu("Select a option:", 10, 50, Constants.FIELDS_OPTIONS, "Field(s) Menu")
		match option:
			case "1":
				new_fields = [item for item in self._ask_fields("Add Field(s)") if item not in self.fields]
				if not new_fields:
					self.dialog.create_message("\nThe fields entered already exist.", 7, 50, "Notification Message")
					return
				self.fields.extend(new_fields)
				self._log("Added field(s)", f"{self.name}: {','.join(new_fields)}")
			case "2":
				self.fields = self._ask_fields("Modify Field(s)", self.fields)
				self._log("Modified field(s)", f"{self.name}: {','.join(self.fields)}")
			case "3":
				selected = self._confirm_selection(self.fields, "Field's Name", "Remove Field(s)", "\nAre you sure to remove the selected field(s)?\n\n** This action cannot be undone.")
				if not selected:
					return
				remaining = [item for item in self.fields if item not in selected]
				if not remaining:
					self.dialog.create_message("\nAt least one field is required. Disable the option instead.", 8, 50, "Error Message")
					return
				self.fields = remaining
				self._log("Removed field(s)", f"{self.name}: {','.join(selected)}")


	def modify_telegram_bot_token(self) -> None:
		"""
		Method that modifies the Telegram Bot Token (the current value is never decrypted or displayed).
		"""
		self.define_telegram_bot_token()
		self._log("Telegram Bot Token modified", self.name)


	def modify_telegram_chat_id(self) -> None:
		"""
		Method that modifies the Telegram Chat ID (the current value is never decrypted or displayed).
		"""
		self.define_telegram_chat_id()
		self._log("Telegram Chat ID modified", self.name)


	# --- Display / delete / enable / disable ---------------------------------------------------
	def display_configuration(self) -> None:
		"""
		Method that displays the alert rule's configuration (sensitive data masked).
		"""
		try:
			option = self._select_rule("Alert Rules")
			if option is None:
				return
			alert_rule_str = self.utils.convert_yaml_to_str(path.join(Constants.ALERT_RULES_FOLDER, option))
			self.dialog.create_scrollbox(f"\n{option.removesuffix('.yaml')}\n\n{alert_rule_str}", 18, 70, "Alert Rule's Configuration")
		except DialogCancelled:
			pass
		except Exception as exception:
			self._error("\nError displaying alert rule's configuration. For more information, see the logs.", "_displayAlertRuleConf", exception)


	def delete_alert_rules(self) -> None:
		"""
		Method that deletes one or more alert rules.
		"""
		try:
			rules = self._list_rules()
			if not rules:
				return
			selected = self._confirm_selection(rules, "Alert rule's name", "Delete Alert Rule(s)", "\nAre you sure to delete the selected alert rule(s)?\n\n**Note: This action cannot be undone.")
			if not selected:
				return
			for alert_rule in selected:
				self.utils.delete_file(path.join(Constants.ALERT_RULES_FOLDER, alert_rule))
			self._log("Alert rule(s) deleted", ",".join(selected), tag = "_deleteAlertRules")
			self.dialog.create_message("\nAlert rule(s) deleted.", 7, 50, "Notification Message")
		except DialogCancelled:
			pass
		except Exception as exception:
			self._error("\nError deleting alert rule(s). For more information, see the logs.", "_deleteAlertRules", exception)


	def disable_alert_rule(self) -> None:
		"""
		Method that disables one or more alert rules.
		"""
		try:
			rules = self._list_rules()
			if not rules:
				return
			selected = self._confirm_selection(rules, "Alert rule's name", "Disable Alert Rule(s)", "\nAre you sure to disable the selected alert rule(s)?")
			if not selected:
				return
			skipped = []
			for alert_rule in selected:
				source = path.join(Constants.ALERT_RULES_FOLDER, alert_rule)
				if path.exists(source + ".disabled"):
					skipped.append(alert_rule)
					continue
				self.utils.rename_file_or_folder(source, source + ".disabled")
			self._report(selected, skipped, "disabled", "_disableAlertRules")
		except DialogCancelled:
			pass
		except Exception as exception:
			self._error("\nError disabling alert rule(s). For more information, see the logs.", "_disableAlertRules", exception)


	def enable_alert_rule(self) -> None:
		"""
		Method that enables one or more alert rules (an enabled rule with the same name is never overwritten).
		"""
		try:
			rules = self._list_rules(disabled = True)
			if not rules:
				return
			selected = self._confirm_selection(rules, "Alert rule's name", "Enable Alert Rule(s)", "\nAre you sure to enable the selected alert rule(s)?")
			if not selected:
				return
			skipped = []
			for alert_rule in selected:
				target = path.join(Constants.ALERT_RULES_FOLDER, alert_rule.removesuffix(".disabled"))
				if path.exists(target):
					skipped.append(alert_rule)
					continue
				self.utils.rename_file_or_folder(path.join(Constants.ALERT_RULES_FOLDER, alert_rule), target)
			self._report(selected, skipped, "enabled", "_enableAlertRules")
		except DialogCancelled:
			pass
		except Exception as exception:
			self._error("\nError enabling alert rule(s). For more information, see the logs.", "_enableAlertRules", exception)


	def _report(self, selected: list, skipped: list, action: str, tag: str) -> None:
		"""
		Method that logs and shows the result of enabling/disabling rules.
		"""
		done = [item for item in selected if item not in skipped]
		if done:
			self._log(f"Alert rule(s) {action}", ",".join(done), tag = tag)
		text = f"\nAlert rule(s) {action}: {len(done)}."
		if skipped:
			text += "\n\nSkipped (a rule with the same name already exists):\n" + "\n".join(skipped)
			self.dialog.create_scrollbox(text, 14, 60, "Notification Message")
		else:
			self.dialog.create_message(text, 7, 50, "Notification Message")


	def display_alert_rules(self) -> None:
		"""
		Method that displays all alert rules.
		"""
		try:
			rules = self._list_rules()
			if rules:
				self.dialog.create_scrollbox(self.utils.get_str_from_list([rule.removesuffix(".yaml") for rule in rules], "Alert Rule(s)"), 18, 70, "Alert Rule(s)")
		except DialogCancelled:
			pass
		except Exception as exception:
			self._error("\nError displaying alert rule(s). For more information, see the logs.", "_displayAlertRules", exception)