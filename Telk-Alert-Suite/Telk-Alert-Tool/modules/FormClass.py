import sys
import os
import re
import yaml
from dialog import Dialog
sys.path.append('./modules')
from UtilsClass import Utils
from CreateConfClass import Configuration 
from LoggerClass import Logger
from RulesClass import Rules

class FormDialogs:

	d = Dialog(dialog = "dialog")
	d.set_background_title("TELK-ALERT CONFIG TOOL")

	button_names = {d.OK:	  "OK",
					d.CANCEL: "Cancel",
					d.HELP:	  "Help",
					d.EXTRA:  "Extra"}

	utils = Utils()
	create_conf = Configuration()
	logger = Logger()
	rules = Rules()

	def getMenu(self, options, title):
		code_mm, tag_mm = self.d.menu("Choose an option", choices=options,title=title)
		if code_mm == self.d.OK:
			return tag_mm
		if code_mm == self.d.CANCEL:
			sys.exit(0)

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

	def getDataNumberDecimal(self, text, initial_value):
		decimal_reg_exp = re.compile(r'^[1-9](\.[0-9]+)?$')
		while True:
			code_nd, tag_nd = self.d.inputbox(text, 10, 50, initial_value)
			if code_nd == self.d.OK:
				if(not Utils.validateRegularExpression(decimal_reg_exp, tag_nd)):
					self.d.msgbox("Invalid value", 5, 50, title = "Error message")
				else:
					if(float(tag_nd) <= 7.0):
						self.d.msgbox("ElasticSearch version not supported", 5, 50, title = "Error message")
					else:
						return tag_nd
			if code_nd == self.d.CANCEL:
				self.mainMenu()

	def getDataIP(self, text, initial_value):
		ip_reg_exp = re.compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
		while True:
			code_ip, tag_ip = self.d.inputbox(text, 10, 50, initial_value)
			if code_ip == self.d.OK:
				if(not Utils.validateRegularExpression(ip_reg_exp, tag_ip)):
					self.d.msgbox("Invalid IP address", 5, 50, title = "Error message")
				else:
					return tag_ip
			if code_ip == self.d.CANCEL:
				self.mainMenu()

	def getDataPort(self, text, initial_value):
		port_reg_exp = re.compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_port, tag_port = self.d.inputbox(text, 10, 50, initial_value)
			if code_port == self.d.OK:
				if(not Utils.validateRegularExpression(port_reg_exp, tag_port)):
					self.d.msgbox("Invalid port", 5 , 50, title = "Error message")
				else:
					return tag_port
		if code_port == self.d.CANCEL:
			self.mainMenu()
	
	def getDataNameFolderOrFile(self, text, initial_value):
		name_file_reg_exp = re.compile(r'^[^\\/?%*:|"<>]+$')
		while True:
			code_fname, tag_fname = self.d.inputbox(text, 10, 50, initial_value)
			if code_fname == self.d.OK:
				if(not Utils.validateRegularExpression(name_file_reg_exp, tag_fname)):
					self.d.msgbox("Invalid name", 5, 50, title = "Error message")
				else:
					return tag_fname
			if code_fname == self.d.CANCEL:
				self.mainMenu()

	def getDataYesOrNo(self, text, title):
		tag_yesorno = self.d.yesno(text, 10, 50, title = title)
		return tag_yesorno

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

	def getDataNumber(self, text, initial_value):
		number_reg_exp = re.compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_num, tag_num = self.d.inputbox(text, 10, 50, initial_value)
			if code_num == self.d.OK:
				if(not Utils.validateRegularExpression(number_reg_exp, tag_num)):
					self.d.msgbox("Invalid number", 5, 50, title = "Error message")
				else:
					return tag_num
			if code_num == self.d.CANCEL:
				self.mainMenu()

	def createConfiguration(self):
		data_conf = []
		version_es = self.getDataNumberDecimal("Enter the ElasticSearch version:", "7.10")
		host_es = self.getDataIP("Enter the ElasticSearch IP address:", "localhost")
		port_es = self.getDataPort("Enter the ElasticSearch listening port:", "9200")
		folder_rules = self.getDataNameFolderOrFile("Enter the name of the folder where the alert rules will be hosted:", "alert_rules")
		use_ssl = self.getDataYesOrNo("Do you want Telk-Alert to connect to ElasticSearch using the SSL/TLS protocol?", "Connection via SSL/TLS")
		http_auth = self.getDataYesOrNo("Is the use of HTTP authentication required to connect to ElasticSearch?", "HTTP authentication")
		data_conf.append(version_es)
		data_conf.append(host_es)
		data_conf.append(port_es)
		data_conf.append(folder_rules)
		if use_ssl == "ok":
			data_conf.append(True)
		else:
			data_conf.append(False)
		if http_auth == "ok":
			data_conf.append(True)
			user_http_auth = self.utils.encryptAES(self.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
			pass_http_auth = self.utils.encryptAES(self.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
			data_conf.append(user_http_auth)
			data_conf.append(pass_http_auth)
		else:
			data_conf.append(False)
		write_index = self.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", "telkalert")
		max_hits = self.getDataNumber("Enter the maximum number of hits for the search (maximum 10000):", "10000")
		data_conf.append(write_index)
		data_conf.append(max_hits)
		self.create_conf.createFileConfiguration(data_conf)
		if os.path.exists(self.utils.getPathTalert("conf") + "/es_conf.yaml"):
			self.d.msgbox("\nConfiguration file created", 7, 50, title = "Notification message")
		else:
			self.d.msgbox("\nError creating configuration file", 7, 50, title = "Error message")
		self.mainMenu()

	def modifyConfiguration(self):
		options_conf_prop = [("Version", "ElasticSearch Version", 0),
							("Host", "ElasticSearch Host", 0),
							("Port", "ElasticSearch Port", 0),
							("Folder name", "Rules Folder", 0),
							("Use SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							("Use HTTP auth", "Enable or disable Http authentication", 0),
							("Index name", "Index name for logs", 0),
							("Hits", "Maximum hits in a search", 0)]

		options_ssl_true = [("To disable", "Disable SSL/TLS communication", 0)]

		options_ssl_false = [("Enable", "Enable SSL/TLS communication", 0)]

		options_http_auth_true = [("To disable", "Disable HTTP Authentication", 0),
								 ("Modify data", "Modify HTTP Authentication data", 0)]

		options_http_auth_false = [("Enable", "Enable HTTP Authentication", 0)]

		options_http_auth_data = [("Username", "Username for HTTP Authentication", 0),
								 ("Password", "User password", 0)]

		bandera_version = 0
		bandera_host = 0
		bandera_port = 0
		bandera_folder_name = 0
		bandera_use_ssl = 0
		bandera_http_auth = 0
		bandera_index_name = 0
		bandera_max_hits = 0
		with open(self.utils.getPathTalert('conf') + '/es_conf.yaml', "rU") as f:
			data_conf = yaml.safe_load(f)
		hash_origen = self.utils.getSha256File(self.utils.getPathTalert('conf') + '/es_conf.yaml')
		opt_conf_prop = self.getDataCheckList("Select one or more options", options_conf_prop, "Update configuration file")
		for opt_prop in opt_conf_prop:
			if opt_prop == "Version":
				bandera_version = 1
			if opt_prop == "Host":
				bandera_host = 1
			if opt_prop == "Port":
				bandera_port = 1
			if opt_prop == "Folder name":
				bandera_folder_name = 1
			if opt_prop == "Use SSL/TLS":
				bandera_use_ssl = 1
			if opt_prop == "Use HTTP auth":
				bandera_http_auth = 1
			if opt_prop == "Index name":
				bandera_index_name = 1
			if opt_prop == "Hits":
				bandera_max_hits = 1
		if bandera_version == 1:
			version_es = self.getDataNumberDecimal("Enter the ElasticSearch version:", str(data_conf['es_version']))
			data_conf['es_version'] = str(version_es)
		if bandera_host == 1:
			host_es = self.getDataIP("Enter the ElasticSearch IP address:", str(data_conf['es_host']))
			data_conf['es_host'] = str(host_es)
		if bandera_port == 1:
			port_es = self.getDataPort("Enter the ElasticSearch listening port:", str(data_conf['es_port']))
			data_conf['es_port'] = int(port_es)
		if bandera_folder_name == 1:
			folder_rules = self.getDataNameFolderOrFile("Enter the name of the folder where the alert rules will be hosted:", data_conf['rules_folder'])
			data_conf['rules_folder'] = str(folder_rules)
			if(not os.path.isdir(self.utils.getPathTalert(str(folder_rules)))):
				os.mkdir(self.utils.getPathTalert(str(folder_rules)))
		if bandera_use_ssl == 1:
			if data_conf['use_ssl'] == True:
				opt_ssl_true = self.getDataRadioList("Select a option:", options_ssl_true, "Connection via SSL/TLS")
				if opt_ssl_true == "To disable":
					data_conf['use_ssl'] = False
			else:
				opt_ssl_false = self.getDataRadioList("Select a option:", options_ssl_false, "Connection via SSL/TLS")
				if opt_ssl_false == "Enable":
					data_conf['use_ssl'] = True
		if bandera_http_auth == 1:
			if data_conf['use_http_auth'] == True:
				opt_http_auth_true = self.getDataRadioList("Select a option:", options_http_auth_true, "HTTP Authentication")
				if opt_http_auth_true == "To disable":
					del(data_conf['http_auth_user'])
					del(data_conf['http_auth_pass'])
					data_conf['use_http_auth'] = False
				if opt_http_auth_true == "Modify data":
					bandera_http_auth_user = 0
					bandera_http_auth_pass = 0
					opt_mod_http_auth = self.getDataCheckList("Select one or more options:", options_http_auth_data, "HTTP Authentication")
					for opt_mod in opt_mod_http_auth:
						if opt_mod == "Username":
							bandera_http_auth_user = 1
						if opt_mod == "Password":
							bandera_http_auth_pass = 1
					if bandera_http_auth_user == 1:
						user_http_auth_mod = self.utils.encryptAES(self.getDataInputText("Enter the username for HTTP authentication:", self.utils.decryptAES(data_conf['http_auth_user']).decode('utf-8')))
						data_conf['http_auth_user'] = user_http_auth_mod.decode('utf-8')
					if bandera_http_auth_pass == 1:
						pass_http_auth_mod = self.utils.encryptAES(self.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
						data_conf['http_auth_pass'] = pass_http_auth_mod.decode('utf-8')
			else:
				opt_http_auth_false = self.getDataRadioList("Select a option:", options_http_auth_false, "HTTP Authentication")
				if opt_http_auth_false == "Enable":
					user_http_auth = self.utils.encryptAES(self.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
					pass_http_auth = self.utils.encryptAES(self.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
					http_auth_data = {'http_auth_user': user_http_auth.decode('utf-8'), 'http_auth_pass': pass_http_auth.decode('utf-8')}
					data_conf.update(http_auth_data)
					data_conf['use_http_auth'] = True
		if bandera_index_name == 1:
			write_index = self.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", str(data_conf['writeback_index']))
			data_conf['writeback_index'] = str(write_index)
		if bandera_max_hits == 1:
			max_hits = self.getDataNumber("Enter the maximum number of hits for the search (maximum 10000):", str(data_conf['max_hits']))
			data_conf['max_hits'] = int(max_hits)
		with open(self.utils.getPathTalert('conf') + '/es_conf.yaml', "w") as file_update:
			yaml.safe_dump(data_conf, file_update, default_flow_style = False)
		hash_modify = self.utils.getSha256File(self.utils.getPathTalert('conf') + '/es_conf.yaml')
		if hash_origen == hash_modify:
			self.d.msgbox("\nConfiguration file not modified", 7, 50, title = "Notification message")
		else:
			self.d.msgbox("\nModified configuration file", 7, 50, title = "Notification message")
			self.logger.createLogTool("Modified configuration file", 3)
		self.mainMenu()

	def getDataConf(self):
		options_conf_false = [("Create configuration", "Create the configuration file", 0)]

		options_conf_true = [("Modify configuration", "Modify the configuration file", 0)]

		if not os.path.exists(self.utils.getPathTalert("conf") + "/es_conf.yaml"):
			opt_conf_false = self.getDataRadioList("Select a option", options_conf_false, "Configuration options")
			if opt_conf_false == "Create configuration":
				self.createConfiguration()
		else:
			opt_conf_true = self.getDataRadioList("Select a option", options_conf_true, "Configuration options")
			if opt_conf_true == "Modify configuration":
				self.modifyConfiguration()

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

	def switchMmenu(self, option):
		if option == 1:
			self.getDataConf()
		if option == 2:
			self.getMenuRules()

	def switchMrules(self, option):
		if option == 1:
			self.rules.createNewRule(FormDialogs())

	def mainMenu(self):
		options_mm = [("1", "Telk-Alert Configuration"),
					  ("2", "Alert Rules"),
					  ("3", "Telk-Alert Service"),
					  ("4", "Telk-Alert Agent"),
					  ("5", "Exit")]

		option_mm = self.getMenu(options_mm, "Main Menu")
		self.switchMmenu(int(option_mm))

		
