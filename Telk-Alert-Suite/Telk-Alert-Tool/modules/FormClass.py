from os import path
from sys import exit
from pathlib import Path
from dialog import Dialog
from re import compile as re_compile
from modules.UtilsClass import Utils
from modules.RulesClass import Rules
from modules.AgentClass import Agent
from modules.ServiceClass import Service
from modules.ConfigurationClass import Configuration 

"""
Class that allows managing the graphical interfaces of Telk-Alert-Tool.
"""
class FormDialog:
	"""
	Property that stores an object of class Dialog.
	"""
	d = None

	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Property that stores an object of the Configuration class.
	"""
	configuration = None

	"""
	List with the options to show when the Telk-Alert configuration file is not created.
	"""
	list_configuration_false = [("Create", "Create the configuration file", 0)]

	"""
	List with the options to show when the Telk-Alert configuration file is created.
	"""
	list_configuration_true = [("Modify", "Modify the configuration file", 0)]

	"""
	Constructor for the FormDialog class.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def __init__(self):
		self.d = Dialog(dialog = "dialog")
		self.d.set_background_title("TELK-ALERT-TOOL")
		self.utils = Utils(self)
		self.configuration = Configuration(self)

	"""
	Method that generates the menu interface.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	options -- List of options that make up the menu.
	title -- Title displayed on the interface.

	Return:
	tag_menu -- Chosen option.
	"""
	def getMenu(self, text, options, title):
		code_menu, tag_menu = self.d.menu(text = text, choices = options, title = title)
		if code_menu == self.d.OK:
			return tag_menu
		if code_menu == self.d.CANCEL:
			self.mainMenu()	

	"""
	Method that generates an interface with several available options, and where only one of them can be chosen.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	options -- List of options that make up the interface.
	title -- Title displayed on the interface.

	Return:
	tag_radiolist -- Chosen option.
	"""
	def getDataRadioList(self, text, options, title):
		while True:
			code_radiolist, tag_radiolist = self.d.radiolist(text = text, width = 65, choices = options, title = title)
			if code_radiolist == self.d.OK:
				if len(tag_radiolist) == 0:
					self.d.msgbox(text = "\nSelect at least one option.", height = 7, width = 50, title = "Error Message")
				else:
					return tag_radiolist
			elif code_radiolist == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface with several available options, and where you can choose one or more of them.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	options -- List of options that make up the interface.
	title -- Title displayed on the interface.

	Return:
	tag_checklist -- List with the chosen options.
	"""
	def getDataCheckList(self, text, options, title):
		while True:
			code_checklist, tag_checklist = self.d.checklist(text = text, width = 75, choices = options, title = title)
			if code_checklist == self.d.OK:
				if len(tag_checklist) == 0:
					self.d.msgbox(text = "\nSelect at least one option.", height = 7, width = 50, title = "Error Message")
				else:
					return tag_checklist
			elif code_checklist == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter text.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Text entered.
	"""
	def getDataInputText(self, text, initial_value):
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text, height = 10, width = 50, init = initial_value)
			if code_inputbox == self.d.OK:
				if tag_inputbox == "":
					self.d.msgbox(text = "\nInvalid data entered. Required value (not empty).", height = 8, width = 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter a password.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_passwordbox -- Password entered.
	"""
	def getDataPassword(self, text, initial_value):
		while True:
			code_passwordbox, tag_passwordbox = self.d.passwordbox(text = text, height = 10, width = 50, init = initial_value, insecure = True)
			if code_passwordbox == self.d.OK:
				if tag_passwordbox == "":
					self.d.msgbox(text = "\nInvalid data entered. Required value (not empty).", height = 8, width = 50, title = "Error Message")
				else:
					return tag_passwordbox
			elif code_passwordbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for entering integer data.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_num -- Number entered.
	"""
	def getDataNumber(self, text, initial_value):
		number_reg_exp = re_compile(r'^\d+$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text, height = 10, width = 50, init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(number_reg_exp, tag_inputbox)):
					self.d.msgbox(text = "\nInvalid data entered. Required value (integer number).", height = 8, width = 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for entering decimal or floating type data.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Decimal or float value entered.
	"""
	def getDataNumberDecimal(self, text, initial_value):
		decimal_reg_exp = re_compile(r'^[1-9](\.[0-9]+)?$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text, height = 10, width = 50, init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(decimal_reg_exp, tag_inputbox)):
					self.d.msgbox(text = "\nInvalid data entered. Required value (decimal or float).", height = 8, width = 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter an IP address.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- IP address entered.
	"""
	def getDataIP(self, text, initial_value):
		ip_reg_exp = re_compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text, height = 10, width = 50, init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(ip_reg_exp, tag_inputbox)):
					self.d.msgbox(text = "\nInvalid data entered. Required value (IP address).", height = 8, width = 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter a port.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Port entered.
	"""
	def getDataPort(self, text, initial_value):
		port_reg_exp = re_compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text, height = 10, width = 50, init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(port_reg_exp, tag_inputbox)):
					self.d.msgbox(text = "\nInvalid data entered. Required value (0 - 65535).", height = 8, width = 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()
	
	"""
	Method that generates the interface for entering directory or file name data.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- File or directory name entered.
	"""
	def getDataNameFolderOrFile(self, text, initial_value):
		name_file_reg_exp = re_compile(r'^[^\\/?%*:|"<>]+$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text, height = 10, width = 50, init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(name_file_reg_exp, tag_inputbox)):
					self.d.msgbox(text = "\nInvalid data entered. Required data (File or directory name).", height = 8, width = 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for entering data of the time type.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text that will be shown to the user.
	hour -- Hour entered.
	minutes -- Minutes entered.

	Return:
	tag_timebox -- Time entered.
	"""
	def getDataTime(self, text, hour, minutes):
		code_timebox, tag_timebox = self.d.timebox(text = text, hour = hour, minute = minutes, second = 00)
		if code_timebox == self.d.OK:
			return tag_timebox
		if code_timebox == self.d.CANCEL:
			self.mainMenu()

	"""
	Method that generates an interface to select a file.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	initial_path -- Initial path in the interface.
	title -- Title displayed on the interface.
	extension_file -- Allowed file extension.

	Return:
	tag_fselect -- Path of the selected file.
	"""
	def getFile(self, initial_path, title, extension_file):
		while True:
			code_fselect, tag_fselect = self.d.fselect(filepath = initial_path, height = 8, width = 50, title = title)
			if code_fselect == self.d.OK:
				if tag_fselect == "":
					self.d.msgbox(text = "\nSelect a file. Required value: " + extension_file + " file.", height = 7, width = 50, title = "Error Message")
				else:
					ext_file = Path(tag_fselect).suffix
					if not ext_file == extension_file:
						self.d.msgbox(text = "\nSelect a file. Required value: " + extension_file + " file.", height = 7, width = 50, title = "Error Message")
					else:
						return tag_fselect
			elif code_fselect == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface of a form.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text that will be shown to the user.
	list_to_elements -- List of elements displayed on the interface.
	title -- Title displayed on the interface.

	Return:
	tag_form -- Values entered in the form.
	"""
	def getForm(self, text, list_to_elements, title):
		while True:
			code_form, tag_form = self.d.form(text = text, elements = list_to_elements, height = 15, width = 50, form_height = len(list_to_elements), title = title)
			if code_form == self.d.OK:
				cont = 0
				for tag in tag_form:
					if tag == "":
						cont += 1
				if cont > 0:
					self.d.msgbox(text = "\nThere should be no empty or null fields.", height = 7, width = 50, title = "Error Message")
				else:
					return tag_form
			elif code_form == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates a decision-making interface (yes / no).

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	title -- Title displayed on the interface.

	Return:
	tag_yesno -- Chosen option (yes or no).
	"""
	def getDataYesOrNo(self, text, title):
		tag_yesno = self.d.yesno(text = text, height = 10, width = 50, title = title)
		return tag_yesno

	"""
	Method that generates an interface with scroll box.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	title -- Title displayed on the interface.
	"""
	def getScrollBox(self, text, title):
		code_scrollbox = self.d.scrollbox(text = text, height = 15, width = 70, title = title)

	"""
	Method that defines the actions to be carried out around the Telk-Alert configuration.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def defineConfiguration(self):
		if not path.exists(self.configuration.path_configuration_file):
			option_configuration_false = self.getDataRadioList("Select a option:", self.list_configuration_false, "Configuration Options")
			if option_configuration_false == "Create":
				self.configuration.createConfiguration()
		else:
			option_configuration_true = self.getDataRadioList("Select a option:", self.list_configuration_true, "Configuration Options")
			if option_configuration_true == "Modify":
				self.configuration.updateConfiguration()

	"""
	Method that obtains the list of alert rules to update one of them.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	rules -- Rules class object.
	"""
	def updateAlertRules(self, rules):
		list_alert_rules_aux = rules.getAllAlertRules()
		if len(list_alert_rules_aux) == 0:
			self.d.msgbox(text = "\nNo alert rules found in: " + rules.path_folder_rules, height = 7, width = 50, title = "Notification Message")
		else:
			list_alert_rules = self.utils.convertListToCheckOrRadioList(list_alert_rules_aux, "Alert Rule")
			option_alert_rules = self.getDataRadioList("Select a option:", list_alert_rules, "Alert Rules")
			rules.updateAlertRule(option_alert_rules)

	"""
	Method that removes one or more alert rules from Telk-Alert.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	rules -- Rules class object.
	"""
	def deleteAlertRules(self, rules):
		list_alert_rules_aux = rules.getAllAlertRules()
		if len(list_alert_rules_aux) == 0:
			self.d.msgbox(text = "\nNo alert rules found in: " + rules.path_folder_rules, height = 7, width = 50, title = "Notification Message")
		else:
			list_alert_rules = self.utils.convertListToCheckOrRadioList(list_alert_rules_aux, "Alert Rule")
			options_alert_rules = self.getDataCheckList("Select one or more options:", list_alert_rules, "Alert Rules")
			confirmation_delete_alert_rules = self.getDataYesOrNo("\nAre you sure to delete the following alert rules?\n\n** This action cannot be undone.", "Delete Alert Rules")
			if confirmation_delete_alert_rules == "ok":
				message_to_display = "\nAlert rules removed:\n"
				for option in options_alert_rules:
					rules.deleteAlertRule(option)
					message_to_display += "\n- " + option
				self.getScrollBox(message_to_display, "Delete Alert Rules")
		self.mainMenu()

	"""
	Method that shows all alert rules created so far.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	rules -- Rules class object.
	"""
	def showAllAlertRules(self, rules):
		list_alert_rules = rules.getAllAlertRules()
		if len(list_alert_rules) == 0:
			self.d.msgbox(text = "\nNo alert rules found in: " + rules.path_folder_rules, height = 7, width = 50, title = "Notification Message")
		else:
			message_to_display = "\nAlert rules in: " + rules.path_folder_rules + '\n'
			for alert_rule in list_alert_rules:
				message_to_display += "\n- " + alert_rule
			self.getScrollBox(message_to_display, "Alert Rules")
		self.mainMenu()
	
	"""
	Method that defines the actions to be carried out around the Telk-Alert Agent configuration.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def defineAgentConfiguration(self):
		agent = Agent(self)
		if not path.exists(agent.path_configuration_file):
			option_configuration_false = self.getDataRadioList("Select a option:", self.list_configuration_false, "Configuration Options")
			if option_configuration_false == "Create":
				agent.createAgentConfiguration()
		else:
			option_configuration_true = self.getDataRadioList("Select a option:", self.list_configuration_true, "Configuration Options")
			if option_configuration_true == "Modify":
				agent.updateAgentConfiguration()

	"""
	Method that displays a message on the screen with information about the application.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def getAbout(self):
		message = "\nCopyright@2022 Tekium. All rights reserved.\nTelk-Alert v3.1\nAuthor: Erick Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\n" + "License: GPLv3\n\nTelk-Alert is a tool that allows the carrying out of searches\nconfigured in ElasticSearch and the sending of alerts with the\nresults of said search to a Telegram channel, one or more email\naddresses or both."
		self.getScrollBox(message, "About")
		self.mainMenu()

	"""
	Method that launches an action based on the option chosen in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchMmenu(self, option):
		if option == 1:
			self.defineConfiguration()
		elif option == 2:
			self.rulesMenu()
		elif option == 3:
			self.serviceMenu()
		elif option == 4:
			self.menuAgent()
		elif option == 5:
			self.getAbout()
		elif option == 6:
			exit(0)

	"""
	Method that launches an action based on the option chosen in the alert rules menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchMrules(self, option):
		rules = Rules(self)
		if option == 1:
			rules.createNewRule()
		elif option == 2:
			self.updateAlertRules(rules)
		elif option == 3:
			self.deleteAlertRules(rules)
		elif option == 4:
			self.showAllAlertRules(rules)

	"""
	Method that launches an action based on the option chosen in the Telk-Alert-Agent menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchMagent(self, option):
		if option == 1:
			self.defineAgentConfiguration()
		if option == 2:
			self.menuServiceAgent()

	"""
	Method that launches an action based on the option chosen in the Telk-Alert-Agent service menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchMServiceAgent(self, option):
		agent = Agent(self)
		if option == 1:
			agent.startService()
		elif option == 2:
			agent.restartService()
		elif option == 3:
			agent.stopService()
		elif option == 4:
			agent.getStatusService()

	"""
	Method that launches an action based on the option chosen in the Telk-Alert service menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchMService(self, option):
		service = Service(self)
		if option == 1:
			service.startService()
		elif option == 2:
			service.restartService()
		elif option == 3:
			service.stopService()
		elif option == 4:
			service.getStatusService()

	"""
	Method that defines the menu on the actions to be carried out in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def mainMenu(self):
		options_mm = [("1", "Telk-Alert Configuration"),
					  ("2", "Alert Rules"),
					  ("3", "Telk-Alert Service"),
					  ("4", "Telk-Alert Agent"),
					  ("5", "About"),
					  ("6", "Exit")]

		option_mm = self.getMenu("Select a option:", options_mm, "Main Menu")
		self.switchMmenu(int(option_mm))

	"""
	Method that defines the menu on the actions to be carried out on the alert rules.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def rulesMenu(self):
		options_mr = [("1", "Create new alert rule"),
					 ("2", "Update alert rule"),
					 ("3", "Delete alert rule(s)"),
					 ("4", "Show all alert rules")]

		if not path.exists(self.configuration.path_configuration_file):
			self.d.msgbox(text = "\nConfiguration file not found.", height = 7, width = 50, title = "Notification Message")
		else:
			option_mr = self.getMenu("Select  a option:", options_mr, "Alert Rules Menu")
			self.switchMrules(int(option_mr))

	"""
	Method that defines the menu on the actions to be carried out on the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def serviceMenu(self):
		options_ms = [("1", "Start Service"),
					  ("2", "Restart Service"),
					  ("3", "Stop Service"),
					  ("4", "Service Status")]

		option_ms = self.getMenu("Select a option:", options_ms, "Telk-Alert Service")
		self.switchMService(int(option_ms))

	"""
	Method that defines the menu on the actions to be carried out on Telk-Alert-Agent.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def menuAgent(self):
		options_ma = [("1", "Configuration"),
					  ("2", "Telk-Alert Agent Service")]

		option_ma = self.getMenu("Select a option:", options_ma, "Telk-Alert-Agent Menu")
		self.switchMagent(int(option_ma))

	"""
	Method that defines the menu on the actions to be carried out on the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def menuServiceAgent(self):
		options_msa = [("1", "Start Service"),
					  ("2", "Restart Service"),
					  ("3", "Stop Service"),
					  ("4", "Service Status")]

		option_msa = self.getMenu("Select a option:", options_msa, "Telk-Alert-Agent Service")
		self.switchMServiceAgent(int(option_msa))