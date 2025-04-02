from os import path
from sys import exit
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from dataclasses import dataclass, field
from .Alert_Rules_Class import AlertRules
from libPyConfiguration import libPyConfiguration
from libPyAgentConfiguration import libPyAgentConfiguration

@dataclass
class TelkAlertTool:
	"""
	Class that manages the Telk-Alert-Tool functionality.
	"""

	def __init__(self):
		"""
		Class constructor.
		"""
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def main_menu(self) -> None:
		"""
		Main menu.
    	"""
		try:
			option = self.dialog.create_menu("Select a option:", 12, 50, self.constants.MAIN_MENU_OPTIONS, "Main Menu")
			self.switch_main_menu(int(option))
		except KeyboardInterrupt:
			pass


	def configuration_menu(self) -> None:
		"""
		Configuration menu.
		"""
		option = self.dialog.create_menu("Select a option:", 9, 50, self.constants.CONFIGURATION_MENU_OPTIONS, "Configuration Menu")
		self.switch_configuration_menu(int(option))


	def alert_rules_menu(self) -> None:
		"""
		Alert rules menu.
		"""
		option = self.dialog.create_menu("Select a option:", 13, 50, self.constants.ALERT_RULES_MENU_OPTIONS, "Alert Rules Menu")
		self.switch_alert_rules_menu(int(option))


	def create_alert_rule_menu(self) -> None:
		"""
		Create Alert Rule menu.
		"""
		option = self.dialog.create_menu("Select a option:", 10, 50, self.constants.CREATE_ALERT_RULE_MENU_OPTIONS, "Create Alert Rule Menu")
		self.switch_create_alert_rule_menu(int(option))


	def disable_enable_alert_rule_menu(self) -> None:
		"""
		Disable/Enable Alert Rule menu.
		"""
		option = self.dialog.create_menu("Select a option:", 9, 50, self.constants.DISABLE_ENABLE_MENU_OPTIONS, "Disable/Enable Alert Rule Menu")
		self.switch_disable_enable_alert_rule_menu(int(option))


	def switch_main_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Main" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				self.configuration_menu()
			case 2:
				self.alert_rules_menu()
			case 4:
				self.display_about()
			case 5:
				exit(1)


	def switch_configuration_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Configuration" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		self.define_configuration() if option == 1 else self.define_agent_configuration()


	def switch_alert_rules_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Alert Rules" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		alert_rule = AlertRules()
		match option:
			case 1:
				self.create_alert_rule_menu()
			case 2:
				alert_rule.modify_alert_rule()
			case 3:
				alert_rule.display_configuration()
			case 4:
				alert_rule.delete_alert_rules()
			case 5:
				self.disable_enable_alert_rule_menu()
			case 6:
				alert_rule.display_alert_rules()


	def switch_create_alert_rule_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Create alert rule" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				self.create_alert_rule()


	def switch_disable_enable_alert_rule_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Create alert rule" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		alert_rule = AlertRules()
		match option:
			case 1:
				alert_rule.disable_alert_rule()
			case 2:
				alert_rule.enable_alert_rule()


	def define_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the Telk-Alert configuration.
		"""
		if not path.exists(self.constants.TELK_ALERT_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "Telk-Alert Configuration")
			if option == "Create":
				self.create_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "Telk-Alert Configuration")
			self.modify_configuration() if option == "Modify" else self.display_configuration()


	def create_configuration(self) -> None:
		"""
		Method that creates the Telk-Alert configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.define_es_host()
		telk_alert_data.define_verificate_certificate()
		telk_alert_data.define_use_authentication(self.constants.KEY_FILE)
		telk_alert_data.create_file(telk_alert_data.convert_object_to_dict(), self.constants.TELK_ALERT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify_configuration(self) -> None:
		"""
		Method that updates or modifies the Telk-Alert configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.modify_configuration(self.constants.TELK_ALERT_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_configuration(self) -> None:
		"""
		Method that displays the Telk-Alert configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.display_configuration(self.constants.TELK_ALERT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def define_agent_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the Telk-Alert-Agent configuration.
		"""
		if not path.exists(self.constants.TELK_ALERT_AGENT_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "Telk-Alert-Agent Configuration")
			if option == "Create":
				self.create_agent_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "Telk-Alert-Agent Configuration")
			self.modify_agent_configuration() if option == "Modify" else self.display_agent_configuration()


	def create_agent_configuration(self) -> None:
		"""
		Method that creates the Telk-Alert-Agent configuration.
		"""
		telk_alert_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		telk_alert_agent_data.define_frequency_time()
		telk_alert_agent_data.define_telegram_bot_token(self.constants.KEY_FILE)
		telk_alert_agent_data.define_telegram_chat_id(self.constants.KEY_FILE)
		telk_alert_agent_data.create_file(telk_alert_agent_data.convert_object_to_dict(), self.constants.TELK_ALERT_AGENT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify_agent_configuration(self) -> None:
		"""
		Method that updates or modifies the Telk-Alert-Agent configuration.
		"""
		telk_alert_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		telk_alert_agent_data.modify_agent_configuration(self.constants.TELK_ALERT_AGENT_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_agent_configuration(self) -> None:
		"""
		Method that displays the Telk-Alert configuration.
		"""
		telk_alert_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		telk_alert_agent_data.display_agent_configuration(self.constants.TELK_ALERT_AGENT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def create_alert_rule(self) -> None:
		"""
		Method that creates a new alert rule.
		"""
		alert_rule = AlertRules()
		alert_rule.define_name()
		alert_rule.define_level()
		alert_rule.define_index_pattern()
		alert_rule.define_timestamp_field()
		alert_rule.define_total_events()
		alert_rule.define_search_time()
		alert_rule.define_range_time()
		alert_rule.define_query_type()
		alert_rule.define_use_fields()
		alert_rule.define_telegram_bot_token()
		alert_rule.define_telegram_chat_id()
		alert_rule.create_file(alert_rule.convert_object_to_dict())


	def display_about(self) -> None:
		"""
		Method that displays the about of the application.
		"""
		try:
			text = "\nAuthor: Erick Roberto Rodríguez Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\nGithub: https://github.com/erickrr-bd/Telk-Alert\nTelk-Alert v4.0 - April 2025" + "\n\nEasy alerting with ElasticSearch and Python."
			self.dialog.create_scrollbox(text, 12, 60, "About")
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error") 
