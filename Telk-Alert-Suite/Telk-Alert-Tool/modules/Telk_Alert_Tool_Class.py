from os import path
from sys import exit
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Alert_Rules_Class import AlertRules
from .Configuration_Class import Configuration

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
			self.__showApplicationAbout()
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
			alert_rules.deleteAlertRules()


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