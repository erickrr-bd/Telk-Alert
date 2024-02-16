from os import path
from sys import exit
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Alert_Rules_Class import AlertRules
from .Telk_Alert_Service_Class import TelkAlertService
from .Telk_Alert_Agent_Service_Class import TelkAlertAgentService
from .Telk_Alert_Configuration_Class import TelkAlertConfiguration
from .Telk_Alert_Agent_Configuration_Class import TelkAlertAgentConfiguration

"""
Class that manages Telk-Alert-Tool actions.
"""
class TelkAlertTool:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def main_menu(self):
		"""
		Method that displays the "Main" menu.
		"""
		try:
			option_main_menu = self.dialog.createMenuDialog("Select a option:", 12, 50, self.constants.OPTIONS_MAIN_MENU, "Main Menu")
			self.switch_main_menu(int(option_main_menu))
		except KeyboardInterrupt:
			pass


	def configuration_menu(self):
		"""
		Method that displays the "Configuration" menu.
		"""
		option_configuration_menu = self.dialog.createMenuDialog("Select a option:", 9, 50, self.constants.OPTIONS_TOOLS_MENU, "Configuration Menu")
		self.switch_configuration_menu(int(option_configuration_menu))


	def alert_rules_menu(self):
		"""
		Method that displays the "Alert Rules" menu.
		"""
		option_alert_rules_menu = self.dialog.createMenuDialog("Select a option:", 12, 50, self.constants.OPTIONS_ALERT_RULES_MENU, "Alert Rules Menu")
		self.switch_alert_rules_menu(int(option_alert_rules_menu))


	def service_menu(self):
		"""
		Method that displays the "Service" menu.
		"""
		option_service_menu = self.dialog.createMenuDialog("Select a option:", 9, 50, self.constants.OPTIONS_TOOLS_MENU, "Service Menu")
		self.switch_service_menu(int(option_service_menu))


	def telk_alert_service_menu(self):
		"""
		Method that displays the "Telk-Alert Service" menu.
		"""
		option_telk_alert_service_menu = self.dialog.createMenuDialog("Select a option:", 11, 50, self.constants.OPTIONS_SERVICE_MENU, "Telk-Alert Service Menu")
		self.switch_telk_alert_service_menu(int(option_telk_alert_service_menu))


	def telk_alert_agent_service_menu(self):
		"""
		Method that displays the "Telk-Alert-Agent Service" menu.
		"""
		option_telk_alert_agent_service_menu = self.dialog.createMenuDialog("Select a option:", 11, 50, self.constants.OPTIONS_SERVICE_MENU, "Telk-Alert-Agent Service Menu")
		self.switch_telk_alert_agent_service_menu(int(option_telk_alert_agent_service_menu))


	def switch_main_menu(self, option_main_menu):
		"""
		Method that executes an action based on the option chosen in the "Main" menu.

		:arg option_main_menu (integer): Chosen option.
		"""
		if option_main_menu == 1:
			self.configuration_menu()
		elif option_main_menu == 2:
			self.alert_rules_menu()
		elif option_main_menu == 3:
			self.service_menu()
		elif option_main_menu == 4:
			self.display_about()
		elif option_main_menu == 5:
			exit(1)


	def switch_configuration_menu(self, option_configuration_menu):
		"""
		Method that executes an action based on the option chosen in the "Configuration" menu.

		:arg option_configuration_menu (integer): Chosen option.
		"""
		self.define_telk_alert_configuration() if option_configuration_menu == 1 else self.define_telk_alert_agent_configuration()


	def switch_alert_rules_menu(self, option_alert_rules_menu):
		"""
		Method that executes an action based on the option chosen in the "Alert Rules" menu.

		:arg option_alert_rules_menu (integer): Chosen option.
		"""
		alert_rules = AlertRules()
		if option_alert_rules_menu == 1:
			alert_rules.create_alert_rule()
		elif option_alert_rules_menu == 2:
			alert_rules.update_alert_rule()
		elif option_alert_rules_menu == 3:
			alert_rules.display_alert_rule()
		elif option_alert_rules_menu == 4:
			alert_rules.remove_alert_rules()
		elif option_alert_rules_menu == 5:
			alert_rules.display_all_alert_rules()


	def switch_service_menu(self, option_service_menu):
		"""
		Method that executes an action based on the option chosen in the "Service" menu.

		:arg option_service_menu (integer): Chosen option.
		"""
		self.telk_alert_service_menu() if option_service_menu == 1 else self.telk_alert_agent_service_menu()


	def switch_telk_alert_service_menu(self, option_telk_alert_service_menu):
		"""
		Method that executes an action based on the option chosen in the "Telk-Alert Service" menu.

		:arg option_telk_alert_service_menu (integer): Chosen option.
		"""
		telk_alert_service = TelkAlertService()
		if option_telk_alert_service_menu == 1:
			telk_alert_service.start_service()
		elif option_telk_alert_service_menu == 2:
			telk_alert_service.restart_service()
		elif option_telk_alert_service_menu == 3:
			telk_alert_service.stop_service()
		elif option_telk_alert_service_menu == 4:
			telk_alert_service.get_service_status()


	def switch_telk_alert_agent_service_menu(self, option_telk_alert_agent_service_menu):
		"""
		Method that executes an action based on the option chosen in the "Telk-Alert-Agent Service" menu.

		:arg option_telk_alert_agent_service_menu (integer): Chosen option.
		"""
		telk_alert_agent_service = TelkAlertAgentService()
		if option_telk_alert_agent_service_menu == 1:
			telk_alert_agent_service.start_service()
		elif option_telk_alert_agent_service_menu == 2:
			telk_alert_agent_service.restart_service()
		elif option_telk_alert_agent_service_menu == 3:
			telk_alert_agent_service.stop_service()
		elif option_telk_alert_agent_service_menu == 4:
			telk_alert_agent_service.get_service_status()


	def define_telk_alert_configuration(self):
		"""
		Method that defines the actions to be performed regarding the Telk-Alert configuration.
		"""
		telk_alert_configuration = TelkAlertConfiguration()
		if not path.exists(self.constants.TELK_ALERT_CONFIGURATION_PATH):
			option_configuration_false = self.dialog.createRadioListDialog("Select a option:", 8, 50, self.constants.OPTIONS_CONFIGURATION_FALSE, "Telk-Alert Configuration")
			if option_configuration_false == "Create":
				telk_alert_configuration.create_configuration()
		else:
			option_configuration_true = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_CONFIGURATION_TRUE, "Telk-Alert Configuration")
			telk_alert_configuration.update_configuration() if option_configuration_true == "Update" else telk_alert_configuration.display_configuration()


	def define_telk_alert_agent_configuration(self):
		"""
		Method that defines the actions to be performed regarding the Telk-Alert-Agent configuration.
		"""
		telk_alert_agent_configuration = TelkAlertAgentConfiguration()
		if not path.exists(self.constants.TELK_ALERT_AGENT_CONFIGURATION_PATH):
			option_configuration_false = self.dialog.createRadioListDialog("Select a option:", 8, 50, self.constants.OPTIONS_CONFIGURATION_FALSE, "Telk-Alert-Agent Configuration")
			if option_configuration_false == "Create":
				telk_alert_agent_configuration.create_configuration()
		else:
			option_configuration_true = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_CONFIGURATION_TRUE, "Telk-Alert-Agent Configuration")
			telk_alert_agent_configuration.update_configuration() if option_configuration_true == "Update" else telk_alert_agent_configuration.display_configuration()


	def display_about(self):
		"""
		Method that shows the about of the application.
		"""
		try:
			message_to_display = "\nCopyright@2024 Tekium. All rights reserved.\nAuthor: Erick Roberto Rodríguez Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\nGithub: https://github.com/erickrr-bd/Telk-Alert\nTelk-Alert v3.3 - February 2024" + "\n\nEasy alerting with ElasticSearch and Python."
			self.dialog.createScrollBoxDialog(message_to_display, 13, 60, "About")
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error") 