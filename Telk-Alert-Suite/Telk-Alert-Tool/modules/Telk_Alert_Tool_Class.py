from os import path
from sys import exit
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from dataclasses import dataclass, field
from .Alert_Rules_Class import AlertRules
from .Telk_Alert_Configuration import TelkAlertConfiguration

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
		option = self.dialog.create_menu("Select a option:", 12, 50, self.constants.ALERT_RULES_MENU_OPTIONS, "Alert Rules Menu")
		self.switch_alert_rules_menu(int(option))


	def create_alert_rule_menu(self) -> None:
		"""
		Create Alert Rule menu.
		"""
		option = self.dialog.create_menu("Select a option:", 10, 50, self.constants.CREATE_ALERT_RULE_MENU_OPTIONS, "Create Alert Rule Menu")
		self.switch_create_alert_rule_menu(int(option))


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
		match option:
			case 1:
				self.create_alert_rule_menu()
			case 2:
				print("Hola2")
			case 3:
				print("Hola 3")
			case 4:
				print("Hola 4")
			case 5:
				print("Hola 5")


	def switch_create_alert_rule_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Create alert rule" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				self.create_alert_rule()


	def define_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the Telk-Alert configuration.
		"""
		configuration = TelkAlertConfiguration()
		if not path.exists(self.constants.TELK_ALERT_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "Telk-Alert Configuration")
			if option == "Create":
				configuration.create()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "Telk-Alert Configuration")
			configuration.modify() if option == "Modify" else configuration.display()


	def create_alert_rule(self) -> None:
		"""
		Method that creates a new alert rule.
		"""
		alert_rule = AlertRules()
		alert_rule.define_name()
		alert_rule.define_level()
		alert_rule.define_index_pattern()
		alert_rule.define_total_events()
		alert_rule.define_search_time()
		alert_rule.define_range_time()
		alert_rule.define_query_type()
		alert_rule.define_use_fields()
		alert_rule.define_telegram_bot_token(self.constants.KEY_FILE)
		alert_rule.define_telegram_chat_id(self.constants.KEY_FILE)
		alert_rule.create_file(alert_rule.convert_object_to_dict(), self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)