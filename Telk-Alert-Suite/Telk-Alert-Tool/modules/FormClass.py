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
	Property that stores an object of the Agent class.
	"""
	agent = None

	"""
	Constructor for the FormDialog class.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def __init__(self):
		self.d = Dialog(dialog = "dialog")
		self.d.set_background_title("TELK-ALERT-TOOL")
		self.utils = Utils(self)
		#self.agent = Agent()

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
			exit(0)

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
	Method that generates the interface for entering data type email address.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_email -- The email address entered.
	"""
	def getDataEmail(self, text, initial_value):
		email_reg_exp = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' )
		while True:
			code_email, tag_email = self.d.inputbox(text, 10, 50, initial_value)
			if code_email == self.d.OK:
				if(not self.utils.validateRegularExpression(email_reg_exp, tag_email)):
					self.d.msgbox("\nInvalid email address", 7, 50, title = "Error message")
				else:
					return tag_email
			if code_email == self.d.CANCEL:
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
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_num -- Number entered.
	"""
	def getDataNumber(self, text, initial_value):
		number_reg_exp = re.compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_num, tag_num = self.d.inputbox(text, 10, 50, initial_value)
			if code_num == self.d.OK:
				if(not self.utils.validateRegularExpression(number_reg_exp, tag_num)):
					self.d.msgbox("\nInvalid number", 7, 50, title = "Error message")
				else:
					return tag_num
			if code_num == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for entering data of the time type.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text that will be shown to the user.
	hour -- Hour entered.
	minutes -- Minutes entered.

	Return:
	tag_time -- Time entered.
	"""
	def getDataTime(self, text, hour, minutes):
		code_time, tag_time = self.d.timebox(text,
											hour = hour,
											minute = minutes,
											second = 00)
		if code_time == self.d.OK:
			return tag_time
		if code_time == self.d.CANCEL:
			self.mainMenu()

	"""
	Method that generates the interface to enter several text type values ​​at the same time.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	list_fields -- List of all the fields that will be entered through the form.
	title -- Title that will be given to the interface and that will be shown to the user.
	text -- Text that will be shown to the user.

	Return:
	tag_nf -- List with the names of the fields with which the search will be restricted.
	"""
	def getFields(self, list_fields, title, text):
		list_new_fields = []
		i = 0
		for field in list_fields:
			list_new_fields.append(("Field " + str(i + 1) + ":", (i + 1), 5, field, (i + 1), 20, 30, 100))
			i += 1
		while True:
			code_nf, tag_nf = self.d.form(text,
										elements = list_new_fields,
										width = 50,
										height = 15,
										form_height = len(list_fields),
										title = title)
			if code_nf == self.d.OK:
				cont = 0
				for tag in tag_nf:
					if tag == "":
						cont += 1
				if cont > 0:
					self.d.msgbox("\nThere cannot be a null or empty field", 7, 50, title = "Error message")
				else:
					return tag_nf
			if code_nf == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for the entry of several values ​​of type email address at the same time.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	list_emails -- List of total emails that will be entered.
	title -- Title that will be given to the interface and that will be shown to the user.
	text -- Text that will be shown to the user.

	Return:
	tag_et -- List of emails entered by the user.
	"""
	def getEmailsTo(self, list_emails, title, text):
		email_reg_exp = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$')
		list_new_emails = []
		i = 0
		for email in list_emails:
			list_new_emails.append(("Email " + str(i + 1) + ":", (i + 1), 5, email, (i + 1), 20, 30, 100))
			i += 1
		while True:
			code_et , tag_et = self.d.form(text,
										elements = list_new_emails,
										width = 50,
										height = 15,
										form_height = len(list_emails),
										title = title)
			if code_et == self.d.OK:
				cont = 0
				for tag in tag_et:
					if(not self.utils.validateRegularExpression(email_reg_exp, tag)):
						cont += 1
				if cont > 0:
					self.d.msgbox("\nThe data entered must correspond to an email", 7, 50, title = "Error message")
				else:
					return tag_et
			if code_et == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates a list with the total of fields that will be entered of type text.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	total_fields -- Total of fields entered by the user.
	
	Return:
	list_new_fields -- The list with the total of fields that will be entered.
	"""
	def getFieldsAdd(self, total_fields):
		list_new_fields = []
		for i in range(int(total_fields)):
			list_new_fields.append("Field " + str(i + 1))
		return list_new_fields

	"""
	Method that generates a list with the total of fields that will be entered of type email address.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	total_emails -- Total number of emails entered by the user.

	Return:
	list_new_emails -- List with the total of emails that will be entered.
	"""
	def getEmailAdd(self, total_emails):
		list_new_emails = []
		for i in range(int(total_emails)):
			list_new_emails.append("Email " + str(i + 1))
		return list_new_emails

	"""
	Method that defines the actions to be carried out around the Telk-Alert configuration.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def defineConfiguration(self):
		options_conf_false = [("Create", "Create the configuration file", 0)]

		options_conf_true = [("Modify", "Modify the configuration file", 0)]
		
		configuration = Configuration(self)
		if not path.exists(configuration.conf_file):
			opt_conf_false = self.getDataRadioList("Select a option:", options_conf_false, "Configuration Options")
			if opt_conf_false == "Create":
				configuration.createConfiguration()
		else:
			opt_conf_true = self.getDataRadioList("Select a option:", options_conf_true, "Configuration Options")
			if opt_conf_true == "Modify":
				configuration.updateConfiguration()

	"""
	Method that defines the action to be performed on the Telk-Alert-Agent configuration file (creation or modification).

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def getAgentConfiguration(self):
		if not os.path.exists(self.utils.getPathTagent('conf') + '/agent_conf.yaml'):
			opt_conf_agent_false = self.getDataRadioList("Select a option:", self.options_conf_false, "Configuration options")
			if opt_conf_agent_false == "Create configuration":
				self.agent.createAgentConfiguration(FormDialogs())
		else:
			opt_conf_agent_true = self.getDataRadioList("Select a option", self.options_conf_true, "Configuration options")
			if opt_conf_agent_true == "Modify configuration":
				self.agent.modifyAgentConfiguration(FormDialogs())

	"""
	Method that defines the menu on the actions to be carried out on the alert rules.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def getMenuRules(self):
		options_mr = [("1", "Create new alert rule"),
					 ("2", "Update alert rule"),
					 ("3", "Delete alert rule(s)"),
					 ("4", "Show all alert rules")]

		if not os.path.exists(self.utils.getPathTalert('conf') + '/es_conf.yaml'):
			self.d.msgbox("\nConfiguration file not found", 7, 50, title = "Error message")
		else:
			option_mr = self.getMenu(options_mr, "Rules Menu")
			self.switchMrules(int(option_mr))

	"""
	Method that defines the menu on the actions to be carried out on Telk-Alert-Agent.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def getMenuAgent(self):
		options_ma = [("1", "Configuration"),
					 ("2", "Telk-Alert Agent Service")]

		option_ma = self.getMenu(options_ma, "Agent Menu")
		self.switchMagent(int(option_ma))

	"""
	Method that defines the menu on the actions to be carried out on the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def getMenuServiceAgent(self):
		options_msa = [("1", "Start Service"),
					  ("2", "Restart Service"),
					  ("3", "Stop Service"),
					  ("4", "Service Status")]

		option_msa = self.getMenu(options_msa, "Telk-Alert-Agent Service")
		self.switchMServiceAgent(int(option_msa))

	"""
	Method that displays a message on the screen with information about the application.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def getAbout(self):
		message = "\nCopyright@2021 Tekium. All rights reserved.\nTelk-Alert v3.1\nAuthor: Erick Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\n" + "License: GPLv3\n\nTelk-Alert is a tool that allows the carrying out of searches\nconfigured in ElasticSearch and the sending of alerts with the\nresults of said search to a Telegram channel, one or more email\naddresses or both."
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
			self.getMenuRules()
		elif option == 3:
			self.serviceMenu()
		elif option == 4:
			self.getMenuAgent()
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
		rules = Rules()
		if option == 1:
			rules.createNewRule(FormDialogs())
		if option == 2:
			rules.getUpdateAlertRules(FormDialogs())
		if option == 3:
			rules.getDeleteRules(FormDialogs())
		if option == 4:
			rules.showAllAlertRules(FormDialogs())

	"""
	Method that launches an action based on the option chosen in the Telk-Alert-Agent menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchMagent(self, option):
		if option == 1:
			self.getAgentConfiguration()
		if option == 2:
			self.getMenuServiceAgent()

	"""
	Method that launches an action based on the option chosen in the Telk-Alert-Agent service menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchMServiceAgent(self, option):
		if option == 1:
			self.agent.startService(FormDialogs())
		if option == 2:
			self.agent.restartService(FormDialogs())
		if option == 3:
			self.agent.stopService(FormDialogs())
		if option == 4:
			self.agent.getStatusService(FormDialogs())

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

		
