from os import path
from sys import exit
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Alert_Rules_Class import AlertRules
from .Agent_Service_Class import AgentService
from .Telk_Alert_Service_Class import TelkAlertService
from .Agent_Configuration_Class import AgentConfiguration
from .Telk_Alert_Configuration_Class import TelkAlertConfiguration

"""
Class that manages what is related to the interfaces and actions of Telk-Alert-Tool.
"""
class TelkAlertTool:

	def __init__(self):
		"""
		Method that corresponds to the constructor of the class.
		"""
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, self.mainMenu)


	def mainMenu(self):
		"""
		Method that shows the "Main" menu.
		"""
		option_main_menu = self.__dialog.createMenuDialog("Select a option:", 14, 50, self.__constants.OPTIONS_MAIN_MENU, "Main Menu")
		self.__switchMainMenu(int(option_main_menu))


	def __alertRulesMenu(self):
		"""
		Method that shows the "Alert RUles" menu.
		"""
		if path.exists(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE):
			option_alert_rules_menu = self.__dialog.createMenuDialog("Select a option:", 12, 50, self.__constants.OPTIONS_ALERT_RULES_MENU, "Alert Rules Menu")
			self.__switchAlertRulesMenu(int(option_alert_rules_menu))
		else:
			self.__dialog.createMessageDialog("\nTelk-Alert configuration file not found.", 7, 50, "Notification Message")
			self.mainMenu()


	def __serviceTelkAlertMenu(self):
		"""
		Method shows the "Telk-Alert service" menu.
		"""
		if path.exists(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE):
			option_telk_alert_service_menu = self.__dialog.createMenuDialog("Select a option:", 11, 50, self.__constants.OPTIONS_SERVICE_MENU, "Telk-Alert Service Menu")
			self.__switchTelkAlertServiceMenu(int(option_telk_alert_service_menu))
		else:
			self.__dialog.createMessageDialog("\nTelk-Alert configuration file not found.", 7, 50, "Notification Message")
			self.mainMenu()


	def __TelkAlertAgentMenu(self):
		"""
		Method that shows the "Telk-Alert-Agent" menu.
		"""
		option_telk_alert_agent_menu = self.__dialog.createMenuDialog("Select a option:", 10, 50, self.__constants.OPTIONS_TELK_ALERT_AGENT_MENU, "Telk-Alert-Agent Menu")
		self.__switchTelkAlertAgentMenu(int(option_telk_alert_agent_menu))


	def __serviceAgentMenu(self):
		"""
		Method that shows the "Telk-Alert-Agent Service" menu.
		"""
		option_service_agent_menu = self.__dialog.createMenuDialog("Select a option:", 12, 50, self.__constants.OPTIONS_SERVICE_MENU, "Telk-Alert-Agent Service Menu")
		self.__switchAgentServiceMenu(int(option_service_agent_menu))


	def __switchMainMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "Main" menu.

		:arg option: Option number.
		"""
		if option == 1:
			self.__defineTelkAlertConfiguration()
		elif option == 2:
			self.__alertRulesMenu()
		elif option == 3:
			self.__serviceTelkAlertMenu()
		elif option == 4:
			self.__TelkAlertAgentMenu()
		elif option == 5:
			self.__TelkAlertReportMenu()
		elif option == 6:
			self.__showAboutApplication()
		elif option == 7:
			exit(1)


	def __switchAlertRulesMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "Alert Rules" menu.

		:arg option: Option number.
		"""
		alert_rules = AlertRules(self.mainMenu)
		if option == 1:
			alert_rules.createNewAlertRule()
		elif option == 2:
			alert_rules.modifyAlertRule()
		elif option == 3:
			alert_rules.showAlertRuleData()
		elif option == 4:
			alert_rules.deleteAlertRules()
		elif option == 5:
			alert_rules.showAllAlertRules()


	def __switchTelkAlertServiceMenu(self, option):
		"""
		Method executes a certain action based on the number of the option chosen in the "Telk-Alert Service" menu.

		:arg option: Option number.
		"""
		telk_alert_service = TelkAlertService(self.mainMenu)
		if option == 1:
			telk_alert_service.startService()
		elif option == 2:
			telk_alert_service.restartService()
		elif option == 3:
			telk_alert_service.stopService()
		elif option == 4:
			telk_alert_service.getServiceStatus()


	def __switchTelkAlertAgentMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "Telk-Alert-Agent" menu.

		:arg option: Option number.
		"""
		if option == 1:
			self.__defineAgentConfiguration()
		elif option == 2:
			self.__serviceAgentMenu()


	def __switchAgentServiceMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "Telk-Alert-Agent Service" menu.

		:arg option: Option number.
		"""
		agent_service = AgentService(self.mainMenu)
		if option == 1:
			agent_service.startTelkAlertAgentService()
		elif option == 2:
			agent_service.restartTelkAlertAgentService()
		elif option == 3:
			agent_service.stopTelkAlertAgentService()
		elif option == 4:
			agent_service.getStatusTelkAlertAgentService()


	def __defineTelkAlertConfiguration(self):
		"""
		Method that defines the action to perform on the Telk-Alert configuration (create or modify).
		"""
		telk_alert_configuration = TelkAlertConfiguration(self.mainMenu)
		if not path.exists(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE):
			option_configuration_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_FALSE, "Telk-ALert Configuration Options")
			if option_configuration_false == "Create":
				telk_alert_configuration.createConfiguration()
		else:
			option_configuration_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_CONFIGURATION_TRUE, "Telk-Alert Configuration Options")
			if option_configuration_true == "Modify":
				telk_alert_configuration.modifyConfiguration()
			elif option_configuration_true == "Show":
				telk_alert_configuration.showConfigurationData()


	def __defineAgentConfiguration(self):
		"""
		Method that defines the action to perform on the Telk-Alert-Agent configuration (create or modify).
		"""
		agent_configuration = AgentConfiguration(self.mainMenu)
		if not path.exists(self.__constants.PATH_FILE_AGENT_CONFIGURATION):
			option_configuration_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_FALSE, "Configuration Options")
			if option_configuration_false == "Create":
				agent_configuration.createAgentConfiguration()
		else:
			option_configuration_true = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_TRUE, "Configuration Options")
			if option_configuration_true == "Modify":
				agent_configuration.modifyAgentConfiguration()


	def __showAboutApplication(self):
		"""
		Method that displays a message on the screen with information about the application.
		"""
		message_to_display = "\nCopyright@2023 Tekium. All rights reserved.\nTelk-Alert v3.3\nAuthor: Erick Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\n" + "License: GPLv3\n\nEasy alerting with ElasticSearch and Python."
		self.__dialog.createScrollBoxDialog(message_to_display, 12, 60, "About")
		self.mainMenu()