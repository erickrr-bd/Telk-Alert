from os import path
from sys import exit
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Telk_Alert_Configuration_Class import TelkAlertConfiguration

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
		option_configuration_menu = self.dialog.createMenuDialog("Select a option:", 9, 50, self.constants.OPTIONS_CONFIGURATION_MENU, "Configuration Menu")
		self.switch_configuration_menu(int(option_configuration_menu))


	def switch_main_menu(self, option_main_menu):
		"""
		Method that executes an action based on the option chosen in the "Main" menu.

		:arg option_main_menu (integer): Chosen option.
		"""
		if option_main_menu == 1:
			self.configuration_menu()
		elif option_main_menu == 5:
			exit(1)


	def switch_configuration_menu(self, option_configuration_menu):
		"""
		Method that executes an action based on the option chosen in the "Configuration" menu.

		:arg option_configuration_menu (integer): Chosen option.
		"""
		self.define_telk_alert_configuration() if option_configuration_menu == 1 else print("Hola 2")


	def define_telk_alert_configuration(self):
		"""
		Method that defines actions to perform on the Telk-Alert configuration.
		"""
		telk_alert_configuration = TelkAlertConfiguration()
		if not path.exists(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH):
			option_configuration_false = self.dialog.createRadioListDialog("Select a option:", 8, 50, self.constants.OPTIONS_CONFIGURATION_FALSE, "Telk-Alert Configuration Options")
			if option_configuration_false == "Create":
				telk_alert_configuration.create_configuration()
		else:
			option_configuration_true = self.dialog.createRadioListDialog("Select a option:", 9, 50, self.constants.OPTIONS_CONFIGURATION_TRUE, "Telk-Alert Configuration Options")
			telk_alert_configuration.update_configuration() if option_configuration_true == "Update" else telk_alert_configuration.display_configuration()