from os import path
from sys import exit
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Configuration_Class import Configuration

"""
Class that manages what is related to the interfaces and actions of Telk-Alert-Tool.
"""
class TelkAlertTool:

	__utils = None

	__dialog = None

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


	def __switchMainMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the Main menu.

		:arg option: Option number.
		"""
		if option == 1:
			self.__defineConfiguration()
		elif option == 2:
			self.__inventoriesMenu()
		elif option == 3:
			self.__serviceMenu()
		elif option == 4:
			self.__showApplicationAbout()
		elif option == 6:
			exit(1)


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
				print("Modificar")
				#configuration.modifyConfiguration()