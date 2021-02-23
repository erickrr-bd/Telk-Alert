import sys
import os
import re
from dialog import Dialog
from modules.UtilsClass import Utils
from modules.ConfigClass import Configuration 
from modules.RulesClass import Rules
from modules.AgentClass import Agent
from modules.ServiceClass import Service

"""
Class that allows managing the graphical interfaces of Telk-Alert-Tool.
"""
class FormDialogs:

	"""
	Object of type Dialog.
	"""
	d = Dialog(dialog = "dialog")

	"""
	The title that will appear in the background of Telk-Alert-Tool is assigned.
	"""
	d.set_background_title("TELK-ALERT CONFIG TOOL")

	"""
	Property that contains the options for the graphical interface buttons.
	"""
	button_names = {d.OK:	  "OK",
					d.CANCEL: "Cancel",
					d.HELP:	  "Help",
					d.EXTRA:  "Extra"}
	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Configuration type object.
	"""
	create_conf = Configuration()

	"""
	Rules type object.
	"""
	rules = Rules()

	"""
	Agent type object.
	"""
	agent = Agent()

	"""
	Service type object.
	"""
	service = Service()

	"""
	Property that contains the options when the configuration file is not created.
	"""
	options_conf_false = [("Create configuration", "Create the configuration file", 0)]

	"""
	Property that contains the options when the configuration file is created.
	"""
	options_conf_true = [("Modify configuration", "Modify the configuration file", 0)]

	"""
	Method that allows generating the menu interface.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	options -- List of options that make up the menu.
	title -- Title that will be given to the interface and that will be shown to the user.

	Return:
	tag_mm -- The option chosen by the user.
	"""
	def getMenu(self, options, title):
		code_mm, tag_mm = self.d.menu("Choose an option", choices=options,title=title)
		if code_mm == self.d.OK:
			return tag_mm
		if code_mm == self.d.CANCEL:
			sys.exit(0)

	"""
	Method that allows displaying a message to the user in a scroll box.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	title -- Title that will be given to the interface and that will be shown to the user.
	"""
	def getScrollBox(self, text, title):
		code_sb = self.d.scrollbox(text, 15, 70, title = title)
		if code_sb == self.d.OK:
			self.mainMenu()

	"""
	Method that allows to generate an interface where you can only choose one option from among several.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	options -- List of options that make up the interface.
	title -- Title that will be given to the interface and that will be shown to the user.

	Return:
	tag_rl -- The option chosen by the user.
	"""
	def getDataRadioList(self, text, options, title):
		while True:
			code_rl, tag_rl = self.d.radiolist(
					  text,
					  width = 65,
					  choices = options,
					  title = title)
			if code_rl == self.d.OK:
				if len(tag_rl) == 0:
					self.d.msgbox("Select at least one option", 5, 50, title = "Error Message")
				else:
					return tag_rl
			if code_rl == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows generating an interface where you can only choose several options at the same time.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	options -- List of options that make up the interface.
	title -- Title that will be given to the interface and that will be shown to the user.

	Return:
	tag_cl -- List with the chosen options.
	"""
	def getDataCheckList(self, text, options, title):
		while True:
			code_cl, tag_cl = self.d.checklist(
					 text,
					 width = 75,
					 choices = options,
					 title = title)
			if code_cl == self.d.OK:
				if len(tag_cl) == 0:
					self.d.msgbox("Select at least one option", 5, 50, title = "Error message")
				else:
					return tag_cl
			if code_cl == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows validating that an entered value corresponds to a decimal value.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_nd -- Decimal value entered.
	"""
	def getDataNumberDecimal(self, text, initial_value):
		decimal_reg_exp = re.compile(r'^[1-9](\.[0-9]+)?$')
		while True:
			code_nd, tag_nd = self.d.inputbox(text, 10, 50, initial_value)
			if code_nd == self.d.OK:
				if(not self.utils.validateRegularExpression(decimal_reg_exp, tag_nd)):
					self.d.msgbox("Invalid value", 5, 50, title = "Error message")
				else:
					if(float(tag_nd) <= 7.0):
						self.d.msgbox("ElasticSearch version not supported", 5, 50, title = "Error message")
					else:
						return tag_nd
			if code_nd == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows validating that an entered value corresponds to an IP address.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_ip -- IP address entered.
	"""
	def getDataIP(self, text, initial_value):
		ip_reg_exp = re.compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
		while True:
			code_ip, tag_ip = self.d.inputbox(text, 10, 50, initial_value)
			if code_ip == self.d.OK:
				if(not self.utils.validateRegularExpression(ip_reg_exp, tag_ip)):
					self.d.msgbox("Invalid IP address", 5, 50, title = "Error message")
				else:
					return tag_ip
			if code_ip == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows to validate an entered value that corresponds to a port.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_port -- Port entered.
	"""
	def getDataPort(self, text, initial_value):
		port_reg_exp = re.compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_port, tag_port = self.d.inputbox(text, 10, 50, initial_value)
			if code_port == self.d.OK:
				if(not self.utils.validateRegularExpression(port_reg_exp, tag_port)):
					self.d.msgbox("Invalid port", 5 , 50, title = "Error message")
				else:
					return tag_port
		if code_port == self.d.CANCEL:
			self.mainMenu()
	
	"""
	Method that allows to validate an entered value that corresponds to a name of a file or directory.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_fname -- File or directory name entered.
	"""
	def getDataNameFolderOrFile(self, text, initial_value):
		name_file_reg_exp = re.compile(r'^[^\\/?%*:|"<>]+$')
		while True:
			code_fname, tag_fname = self.d.inputbox(text, 10, 50, initial_value)
			if code_fname == self.d.OK:
				if(not self.utils.validateRegularExpression(name_file_reg_exp, tag_fname)):
					self.d.msgbox("Invalid name", 5, 50, title = "Error message")
				else:
					return tag_fname
			if code_fname == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows the user to enter an email and validate it.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_email -- The email address entered.
	"""
	def getDataEmail(self, text, initial_value):
		email_reg_exp = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
		while True:
			code_email, tag_email = self.d.inputbox(text, 10, 50, initial_value)
			if code_email == self.d.OK:
				if(not self.utils.validateRegularExpression(email_reg_exp, tag_email)):
					self.d.msgbox("Invalid email address", 5, 50, title = "Error message")
				else:
					return tag_email
			if code_email == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows creating an interface where the only options available are yes or no.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	title -- Title that will be given to the interface and that will be shown to the user.

	Return:
	tag_yesorno -- Chosen option (yes or no).
	"""
	def getDataYesOrNo(self, text, title):
		tag_yesorno = self.d.yesno(text, 10, 50, title = title)
		return tag_yesorno

	"""
	Method that allows creating an interface to enter a text string without restrictions.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_input -- Text entered.
	"""
	def getDataInputText(self, text, initial_value):
		while True:
			code_input, tag_input = self.d.inputbox(text, 10, 50, initial_value)
			if code_input == self.d.OK:
				if tag_input == "":
					self.d.msgbox("The value cannot be empty", 5, 50, title = "Error message")
				else:
					return tag_input
			if code_input == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows creating an interface to enter a password.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_pass -- Password entered.
	"""
	def getDataPassword(self, text, initial_value):
		while True:
			code_pass, tag_pass = self.d.passwordbox(text, 10, 50, initial_value, insecure = True)
			if code_pass == self.d.OK:
				if tag_pass == "":
					self.d.msgbox("Password cannot be empty", 5, 50, title = "Error message")
				else:
					return tag_pass
			if code_pass == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows creating an interface to enter an integer type number.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
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
					self.d.msgbox("Invalid number", 5, 50, title = "Error message")
				else:
					return tag_num
			if code_num == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows to obtain an hour with minutes.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
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
	Method that allows creating the form where more than one value will be entered at the same time.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
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
					self.d.msgbox("There cannot be a null or empty field", 5, 50, title = "Error message")
				else:
					return tag_nf
			if code_nf == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows generating the form where the emails to which the alert will be sent will be entered.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	list_emails -- List of total emails that will be entered.
	title -- Title that will be given to the interface and that will be shown to the user.
	text -- Text that will be shown to the user.

	Return:
	tag_et -- List of emails entered by the user.
	"""
	def getEmailsTo(self, list_emails, title, text):
		email_reg_exp = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
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
					self.d.msgbox("The data entered must correspond to an email", 5, 50, title = "Error message")
				else:
					return tag_et
			if code_et == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that allows generating a list with the total number of fields entered by the user.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
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
	Method that allows generating a list with the total number of emails entered by the user.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
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
	Method that allows defining if the configuration file should be created or modified.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def getDataConf(self):
		if not os.path.exists(self.utils.getPathTalert("conf") + "/es_conf.yaml"):
			opt_conf_false = self.getDataRadioList("Select a option", self.options_conf_false, "Configuration options")
			if opt_conf_false == "Create configuration":
				self.create_conf.createConfiguration(FormDialogs())
		else:
			opt_conf_true = self.getDataRadioList("Select a option", self.options_conf_true, "Configuration options")
			if opt_conf_true == "Modify configuration":
				self.create_conf.modifyConfiguration(FormDialogs())

	"""
	Method that allows managing whether the Telk-Alert-Agent configuration is created or modified.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
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
	Method that allows creating the menu interface for the operations that can be performed with the alert rules.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def getMenuRules(self):
		options_mr = [("1", "Create new alert rule"),
					 ("2", "Update alert rule"),
					 ("3", "Delete alert rule(s)"),
					 ("4", "Show all alert rules")]

		if not os.path.exists(self.utils.getPathTalert('conf') + '/es_conf.yaml'):
			self.d.msgbox("\nConfiguration file not found", 5, 50, title = "Error message")
		else:
			option_mr = self.getMenu(options_mr, "Rules Menu")
			self.switchMrules(int(option_mr))

	"""
	Method that allows creating the interface for the Telk-Alert-Agent options menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def getMenuAgent(self):
		options_ma = [("1", "Configuration"),
					 ("2", "Telk-Alert Agent Service")]

		option_ma = self.getMenu(options_ma, "Agent Menu")
		self.switchMagent(int(option_ma))

	"""
	Method that allows creating the menu interface of the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def getMenuService(self):
		options_ms = [("1", "Start Service"),
					  ("2", "Restart Service"),
					  ("3", "Stop Service"),
					  ("4", "Service Status")]

		option_ms = self.getMenu(options_ms, "Telk-Alert Service")
		self.switchMService(int(option_ms))

	"""
	Method that allows creating the menu interface of the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def getMenuServiceAgent(self):
		options_msa = [("1", "Start Service"),
					  ("2", "Restart Service"),
					  ("3", "Stop Service"),
					  ("4", "Service Status")]

		option_msa = self.getMenu(options_msa, "Telk-Alert-Agent Service")
		self.switchMServiceAgent(int(option_msa))

	"""
	Method that allows interacting with the main menu options.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	option -- Chosen option.
	"""
	def switchMmenu(self, option):
		if option == 1:
			self.getDataConf()
		if option == 2:
			self.getMenuRules()
		if option == 3:
			self.getMenuService()
		if option == 4:
			self.getMenuAgent()
		if option == 5:
			sys.exit(0)

	"""
	Method that allows interacting with the options of the alert rules menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	option -- Chosen option.
	"""
	def switchMrules(self, option):
		if option == 1:
			self.rules.createNewRule(FormDialogs())
		if option == 2:
			self.rules.getUpdateAlertRules(FormDialogs())
		if option == 3:
			self.rules.getDeleteRules(FormDialogs())
		if option == 4:
			self.rules.showAllAlertRules(FormDialogs())

	"""
	Method that allows interacting with the options of the Telk-Alert-Agent service menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	option -- Chosen option.
	"""
	def switchMagent(self, option):
		if option == 1:
			self.getAgentConfiguration()
		if option == 2:
			self.getMenuServiceAgent()

	"""
	Method that allows interacting with the options of the Telk-Alert-Agent service menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
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
	Method that allows interacting with the options of the Telk-Alert service menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	option -- Chosen option.
	"""
	def switchMService(self, option):
		if option == 1:
			self.service.startService(FormDialogs())
		if option == 2:
			self.service.restartService(FormDialogs())
		if option == 3:
			self.service.stopService(FormDialogs())
		if option == 4:
			self.service.getStatusService(FormDialogs())

	"""
	Method that allows creating the interface with the main menu options.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def mainMenu(self):
		options_mm = [("1", "Telk-Alert Configuration"),
					  ("2", "Alert Rules"),
					  ("3", "Telk-Alert Service"),
					  ("4", "Telk-Alert Agent"),
					  ("5", "Exit")]

		option_mm = self.getMenu(options_mm, "Main Menu")
		self.switchMmenu(int(option_mm))

		
