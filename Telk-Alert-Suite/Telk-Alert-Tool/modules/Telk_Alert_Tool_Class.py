"""
Class that manages everything related to Telk-Alert-Tool.
"""
from os import path
from sys import exit
from libPyLog import libPyLog
from dataclasses import dataclass
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Alert_Rules_Class import AlertRules
from .Alert_Rules_Class import CustomAlertRule
from libPyConfiguration import libPyConfiguration
from libPyAgentConfiguration import libPyAgentConfiguration

@dataclass
class TelkAlertTool:

	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
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
		Configuration's menu.
		"""
		option = self.dialog.create_menu("Select a option:", 9, 50, self.constants.CONFIGURATION_MENU_OPTIONS, "Configuration Menu")
		self.switch_configuration_menu(int(option))


	def alert_rules_menu(self) -> None:
		"""
		Alert rules' menu.
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


	def service_menu(self) -> None:
		"""
		Service's menu.
		"""
		option = self.dialog.create_menu("Select a option:", 9, 50, self.constants.CONFIGURATION_MENU_OPTIONS, "Service Menu")
		self.switch_service_menu(int(option))


	def telk_alert_service_menu(self) -> None:
		"""
		Telk-Alert's service menu.
		"""
		option = self.dialog.create_menu("Select a option:", 11, 50, self.constants.SERVICE_MENU_OPTIONS, "Telk-Alert Service Menu")
		self.switch_telk_alert_service_menu(int(option))


	def telk_alert_agent_service_menu(self) -> None:
		"""
		Telk-Alert-Agent's service menu.
		"""
		option = self.dialog.create_menu("Select a option:", 11, 50, self.constants.SERVICE_MENU_OPTIONS, "Telk-Alert-Agent Service Menu")
		self.switch_telk_alert_agent_service_menu(int(option))


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
			case 3:
				self.service_menu()
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
		Method that executes an action based on the option chosen in the "Create Alert Rule" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				self.create_alert_rule()
			case 2:
				self.create_custom_alert_rule()


	def switch_disable_enable_alert_rule_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Disable/Enable Alert Rule" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		alert_rule = AlertRules()
		match option:
			case 1:
				alert_rule.disable_alert_rule()
			case 2:
				alert_rule.enable_alert_rule()


	def switch_service_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Service" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		self.telk_alert_service_menu() if option == 1 else self.telk_alert_agent_service_menu()


	def switch_telk_alert_service_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Telk-Alert Service" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				result = self.utils.manage_daemon("telk-alert.service", 1)
				if result == 0:
					self.dialog.create_message("\nTelk-Alert service started.", 7, 50, "Notification Message")
					self.logger.create_log("Telk-Alert service started", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 2:
				result = self.utils.manage_daemon("telk-alert.service", 2)
				if result == 0:
					self.dialog.create_message("\nTelk-Alert service restarted.", 7, 50, "Notification Message")
					self.logger.create_log("Telk-Alert service restarted", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 3:
				result = self.utils.manage_daemon("telk-alert.service", 3)
				if result == 0:
					self.dialog.create_message("\nTelk-Alert service stopped.", 7, 50, "Notification Message")
					self.logger.create_log("Telk-Alert service stopped", 3, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 4:
				service_status = self.utils.get_detailed_status_by_daemon("telk-alert.service", "/tmp/telk_alert.status")
				self.dialog.create_scrollbox(service_status, 18, 70, "Telk-Alert Service")


	def switch_telk_alert_agent_service_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Telk-Alert-Agent Service" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				result = self.utils.manage_daemon("telk-alert-agent.service", 1)
				if result == 0:
					self.dialog.create_message("\nTelk-Alert-Agent service started.", 7, 50, "Notification Message")
					self.logger.create_log("Telk-Alert-Agent service started", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 2:
				result = self.utils.manage_daemon("telk-alert-agent.service", 2)
				if result == 0:
					self.dialog.create_message("\nTelk-Alert-Agent service restarted.", 7, 50, "Notification Message")
					self.logger.create_log("Telk-Alert-Agent service restarted", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 3:
				result = self.utils.manage_daemon("telk-alert-agent.service", 3)
				if result == 0:
					self.dialog.create_message("\nTelk-Alert-Agent service stopped.", 7, 50, "Notification Message")
					self.logger.create_log("Telk-Alert-Agent service stopped", 3, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 4:
				service_status = self.utils.get_detailed_status_by_daemon("telk-alert-agent.service", "/tmp/telk_alert_agent.status")
				self.dialog.create_scrollbox(service_status, 18, 70, "Telk-Alert-Agent Service")


	def define_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the Telk-Alert's configuration.
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
		Method that creates the Telk-Alert's configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.define_es_host()
		telk_alert_data.define_verificate_certificate()
		telk_alert_data.define_use_authentication(self.constants.KEY_FILE)
		telk_alert_data.create_file(telk_alert_data.convert_object_to_dict(), self.constants.TELK_ALERT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify_configuration(self) -> None:
		"""
		Method that updates or modifies the Telk-Alert's configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.modify_configuration(self.constants.TELK_ALERT_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_configuration(self) -> None:
		"""
		Method that displays the Telk-Alert's configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.display_configuration(self.constants.TELK_ALERT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def define_agent_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the Telk-Alert-Agent's configuration.
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
		Method that creates the Telk-Alert-Agent's configuration.
		"""
		telk_alert_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		telk_alert_agent_data.define_frequency_time()
		telk_alert_agent_data.define_telegram_bot_token(self.constants.KEY_FILE)
		telk_alert_agent_data.define_telegram_chat_id(self.constants.KEY_FILE)
		telk_alert_agent_data.create_file(telk_alert_agent_data.convert_object_to_dict(), self.constants.TELK_ALERT_AGENT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify_agent_configuration(self) -> None:
		"""
		Method that updates or modifies the Telk-Alert-Agent's configuration.
		"""
		telk_alert_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		telk_alert_agent_data.modify_agent_configuration(self.constants.TELK_ALERT_AGENT_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_agent_configuration(self) -> None:
		"""
		Method that displays the Telk-Alert's configuration.
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


	def create_custom_alert_rule(self) -> None:
		"""
		Method that creates a new custom alert rule.
		"""
		custom_alert_rule = CustomAlertRule()
		custom_alert_rule.is_custom_rule = True
		custom_alert_rule.define_name()
		custom_alert_rule.define_level()
		custom_alert_rule.define_index_pattern()
		custom_alert_rule.define_timestamp_field()
		custom_alert_rule.define_search_time()
		custom_alert_rule.define_range_time()
		custom_alert_rule.define_custom_type()
		if custom_alert_rule.custom_rule_type == "Brute Force":
			custom_alert_rule.define_total_events()
			custom_alert_rule.define_hostname_field()
			custom_alert_rule.define_username_field()
		custom_alert_rule.define_query_type()
		custom_alert_rule.define_use_fields()
		custom_alert_rule.define_telegram_bot_token()
		custom_alert_rule.define_telegram_chat_id()
		custom_alert_rule.create_file(custom_alert_rule.convert_object_to_dict())


	def display_about(self) -> None:
		"""
		Method that displays the about of the application.
		"""
		try:
			text = "\nAuthor: Erick Roberto Rodríguez Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\nGithub: https://github.com/erickrr-bd/Telk-Alert\nTelk-Alert v4.1 - September 2025" + "\n\nEasy alerting with ElasticSearch and Python."
			self.dialog.create_scrollbox(text, 12, 60, "About")
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error") 
