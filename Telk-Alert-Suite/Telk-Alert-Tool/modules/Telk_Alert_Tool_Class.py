from os import path
from sys import exit
from libPyUtils import libPyUtils
from .Service_Class import Service
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Alert_Rules_Class import AlertRules
from .Configuration_Class import Configuration
from .Agent_Configuration_Class import AgentConfiguration

"""
Class that manages what is related to the interfaces and actions of Telk-Alert-Tool.
"""
class TelkAlertTool:
	"""
	Attribute that stores an object of the libPyUtils class.
	"""
	__utils = None

	"""
	Attribute that stores an object of the libPyDialog class.
	"""
	__dialog = None

	"""
	Attribute that stores an object of the Constants class.
	"""
	__constants = None


	def __init__(self):
		"""
		Method that corresponds to the constructor of the class.
		"""
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, self.mainMenu)


	def mainMenu(self):
		"""
		Method that shows the main menu of the application.
		"""
		option_main_menu = self.__dialog.createMenuDialog("Select a option:", 14, 50, self.__constants.OPTIONS_MAIN_MENU, "Main Menu")
		self.__switchMainMenu(int(option_main_menu))


	def __alertRulesMenu(self):
		"""
		Method that shows the alert rules menu of the application.
		"""
		if path.exists(self.__constants.PATH_FILE_CONFIGURATION):
			option_alert_rules_menu = self.__dialog.createMenuDialog("Select a option:", 12, 50, self.__constants.OPTIONS_ALERT_RULES_MENU, "Alert Rules Menu")
			self.__switchAlertRulesMenu(int(option_alert_rules_menu))
		else:
			self.__dialog.createMessageDialog("\nConfiguration file not found.", 7, 50, "Notification Message")
			self.mainMenu()


	def __serviceMenu(self):
		"""
		Method that shows the "Service" menu of the application.
		"""
		if path.exists(self.__constants.PATH_FILE_CONFIGURATION):
			option_service_menu = self.__dialog.createMenuDialog("Select a option:", 12, 50, self.__constants.OPTIONS_SERVICE_MENU, "Service Menu")
			self.__switchServiceMenu(int(option_service_menu))
		else:
			self.__dialog.createMessageDialog("\nConfiguration file not found.", 7, 50, "Notification Message")
			self.mainMenu()


	def __TelkAlertAgentMenu(self):
		"""
		Method that shows the "Telk-Alert-Agent" menu.
		"""
		option_telk_alert_agent_menu = self.__dialog.createMenuDialog("Select a option:", 10, 50, self.__constants.OPTIONS_TELK_ALERT_AGENT_MENU, "Telk-Alert-Agent Menu")
		self.__switchTelkAlertAgentMenu(int(option_telk_alert_agent_menu))


	def __switchMainMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the Main menu.

		:arg option: Option number.
		"""
		if option == 1:
			self.__defineConfiguration()
		elif option == 2:
			self.__alertRulesMenu()
		elif option == 3:
			self.__serviceMenu()
		elif option == 4:
			self.__TelkAlertAgentMenu()
		elif option == 5:
			self.__showAboutApplication()
		elif option == 6:
			exit(1)


	def __switchAlertRulesMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the Alert Rules menu.

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


	def __switchServiceMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "Service" menu.

		:arg option: Option number.
		"""
		service = Service(self.mainMenu)
		if option == 1:
			service.startTelkAlertService()
		elif option == 2:
			service.restartTelkAlertService()
		elif option == 3:
			service.stopTelkAlertService()
		elif option == 4:
			service.getStatusTelkAlertService()


	def __switchTelkAlertAgentMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "Telk-Alert-Agent" menu.

		:arg option: Option number.
		"""
		service = Service(self.mainMenu)
		if option == 1:
			self.__defineAgentConfiguration()


	def __defineConfiguration(self):
		"""
		Method that defines the action to perform on the Telk-Alert configuration (create or modify).
		"""
		configuration = Configuration(self.mainMenu)
		if not path.exists(self.__constants.PATH_FILE_CONFIGURATION):
			option_configuration_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_FALSE, "Configuration Options")
			if option_configuration_false == "Create":
				configuration.createConfiguration()
		else:
			option_configuration_true = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_TRUE, "Configuration Options")
			if option_configuration_true == "Modify":
				configuration.modifyConfiguration()


	def __defineAgentConfiguration(self):
		"""
		Method that defines the action to perform on the Telk-Alert configuration (create or modify).
		"""
		agent_configuration = AgentConfiguration(self.mainMenu)
		if not path.exists(self.__constants.PATH_FILE_AGENT_CONFIGURATION):
			option_configuration_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_FALSE, "Configuration Options")
			if option_configuration_false == "Create":
				agent_configuration.createAgentConfiguration()
		else:
			option_configuration_true = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_TRUE, "Configuration Options")
			if option_configuration_true == "Modify":
				configuration.modifyConfiguration()


	def __showAboutApplication(self):
		"""
		Method that displays a message on the screen with information about the application.
		"""
		message_to_display = "\nCopyright@2022 Tekium. All rights reserved.\nTelk-Alert v3.2\nAuthor: Erick Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\n" + "License: GPLv3\n\nEasy alerting with ElasticSearch and Python."
		self.__dialog.createScrollBoxDialog(message_to_display, 12, 60, "About")
		self.mainMenu()