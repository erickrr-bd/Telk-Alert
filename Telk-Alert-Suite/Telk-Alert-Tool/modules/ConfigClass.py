import os
import yaml
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger

"""
Class that allows managing everything related to the Telk-Alert configuration.
"""
class Configuration:

	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Logger type object
	"""
	logger = Logger()

	"""
	Method that allows requesting the data required to create the Telk-Alert configuration file.

	Parameters:
	self -- Instance object.
	form_dialog -- A FormClass class object.
	"""
	def createConfiguration(self, form_dialog):
		data_conf = []
		version_es = form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", "7.10")
		host_es = form_dialog.getDataIP("Enter the ElasticSearch IP address:", "localhost")
		port_es = form_dialog.getDataPort("Enter the ElasticSearch listening port:", "9200")
		folder_rules = form_dialog.getDataNameFolderOrFile("Enter the name of the folder where the alert rules will be hosted:", "alert_rules")
		use_ssl = form_dialog.getDataYesOrNo("Do you want Telk-Alert to connect to ElasticSearch using the SSL/TLS protocol?", "Connection Via SSL/TLS")
		data_conf.append(version_es)
		data_conf.append(host_es)
		data_conf.append(port_es)
		data_conf.append(folder_rules)
		if use_ssl == "ok":
			data_conf.append(True)
			valid_certificates = form_dialog.getDataYesOrNo("Do you want the certificates for SSL/TLS communication to be validated?", "Certificate Validation")
			if valid_certificates == "ok":
				data_conf.append(True)
			else:
				data_conf.append(False)
		else:
			data_conf.append(False)
		http_auth = form_dialog.getDataYesOrNo("Is the use of HTTP authentication required to connect to ElasticSearch?", "HTTP Authentication")
		if http_auth == "ok":
			data_conf.append(True)
			user_http_auth = self.utils.encryptAES(form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
			pass_http_auth = self.utils.encryptAES(form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
			data_conf.append(user_http_auth)
			data_conf.append(pass_http_auth)
		else:
			data_conf.append(False)
		write_index = form_dialog.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", "telkalert")
		max_hits = form_dialog.getDataNumber("Enter the maximum number of hits for the search (maximum 10000):", "10000")
		data_conf.append(write_index)
		data_conf.append(max_hits)
		self.createFileConfiguration(data_conf)
		if os.path.exists(self.utils.getPathTalert("conf") + "/es_conf.yaml"):
			form_dialog.d.msgbox("\nConfiguration file created", 7, 50, title = "Notification message")
			self.logger.createLogTool("Configuration file created", 3)
		else:
			form_dialog.d.msgbox("\nError creating configuration file", 7, 50, title = "Error message")
		form_dialog.mainMenu()

	"""
	Method that allows creating the data request to modify one or more fields of the configuration file.

	Parameters:
	self -- Instance object.
	form_dialog -- A FormClass class object.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def modifyConfiguration(self, form_dialog):
		options_conf_prop = [("Version", "ElasticSearch Version", 0),
							("Host", "ElasticSearch Host", 0),
							("Port", "ElasticSearch Port", 0),
							("Folder name", "Rules Folder", 0),
							("Use SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							("Validate certificates", "Enable or disable certificate validation", 0),
							("Use HTTP auth", "Enable or disable Http authentication", 0),
							("Index name", "Index name for logs", 0),
							("Hits", "Maximum hits in a search", 0)]

		options_ssl_true = [("To disable", "Disable SSL/TLS communication", 0)]

		options_ssl_false = [("Enable", "Enable SSL/TLS communication", 0)]

		options_valid_cert_true = [("To disable", "Disable certificate validation", 0)]

		options_valid_cert_false = [("Enable", "Enable certificate validation", 0)]

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
		bandera_validate_cert = 0
		bandera_http_auth = 0
		bandera_index_name = 0
		bandera_max_hits = 0
		with open(self.utils.getPathTalert('conf') + '/es_conf.yaml', "rU") as f:
			data_conf = yaml.safe_load(f)
		hash_origen = self.utils.getSha256File(self.utils.getPathTalert('conf') + '/es_conf.yaml')
		opt_conf_prop = form_dialog.getDataCheckList("Select one or more options", options_conf_prop, "Update configuration file")
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
			if opt_prop == "Validate certificates":
				bandera_validate_cert = 1
			if opt_prop == "Use HTTP auth":
				bandera_http_auth = 1
			if opt_prop == "Index name":
				bandera_index_name = 1
			if opt_prop == "Hits":
				bandera_max_hits = 1
		try:
			if bandera_version == 1:
				version_es = form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", str(data_conf['es_version']))
				data_conf['es_version'] = str(version_es)
			if bandera_host == 1:
				host_es = form_dialog.getDataIP("Enter the ElasticSearch IP address:", str(data_conf['es_host']))
				data_conf['es_host'] = str(host_es)
			if bandera_port == 1:
				port_es = form_dialog.getDataPort("Enter the ElasticSearch listening port:", str(data_conf['es_port']))
				data_conf['es_port'] = int(port_es)
			if bandera_folder_name == 1:
				folder_rules = form_dialog.getDataNameFolderOrFile("Enter the name of the folder where the alert rules will be hosted:", data_conf['rules_folder'])
				data_conf['rules_folder'] = str(folder_rules)
				if(not os.path.isdir(self.utils.getPathTalert(str(folder_rules)))):
					os.mkdir(self.utils.getPathTalert(str(folder_rules)))
			if bandera_use_ssl == 1:
				if data_conf['use_ssl'] == True:
					opt_ssl_true = form_dialog.getDataRadioList("Select a option:", options_ssl_true, "Connection via SSL/TLS")
					if opt_ssl_true == "To disable":
						data_conf['use_ssl'] = False
				else:
					opt_ssl_false = form_dialog.getDataRadioList("Select a option:", options_ssl_false, "Connection via SSL/TLS")
					if opt_ssl_false == "Enable":
						data_conf['use_ssl'] = True
			if bandera_validate_cert == 1:
				if data_conf['valid_certificates'] == True:
					opt_valid_cert_true = form_dialog.getDataRadioList("Select a option:", options_valid_cert_true, "Certificate Validation")
					if opt_valid_cert_true == "To disable":
						data_conf['valid_certificates'] = False
				else:
					opt_valid_cert_false = form_dialog.getDataRadioList("Select a option:", options_valid_cert_false, "Certificate Validation")
					if opt_valid_cert_false == "Enable":
						data_conf['valid_certificates'] = True
			if bandera_http_auth == 1:
				if data_conf['use_http_auth'] == True:
					opt_http_auth_true = form_dialog.getDataRadioList("Select a option:", options_http_auth_true, "HTTP Authentication")
					if opt_http_auth_true == "To disable":
						del(data_conf['http_auth_user'])
						del(data_conf['http_auth_pass'])
						data_conf['use_http_auth'] = False
					if opt_http_auth_true == "Modify data":
						bandera_http_auth_user = 0
						bandera_http_auth_pass = 0
						opt_mod_http_auth = form_dialog.getDataCheckList("Select one or more options:", options_http_auth_data, "HTTP Authentication")
						for opt_mod in opt_mod_http_auth:
							if opt_mod == "Username":
								bandera_http_auth_user = 1
							if opt_mod == "Password":
								bandera_http_auth_pass = 1
						if bandera_http_auth_user == 1:
							user_http_auth_mod = self.utils.encryptAES(form_dialog.getDataInputText("Enter the username for HTTP authentication:", self.utils.decryptAES(data_conf['http_auth_user']).decode('utf-8')))
							data_conf['http_auth_user'] = user_http_auth_mod.decode('utf-8')
						if bandera_http_auth_pass == 1:
							pass_http_auth_mod = self.utils.encryptAES(form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
							data_conf['http_auth_pass'] = pass_http_auth_mod.decode('utf-8')
				else:
					opt_http_auth_false = form_dialog.getDataRadioList("Select a option:", options_http_auth_false, "HTTP Authentication")
					if opt_http_auth_false == "Enable":
						user_http_auth = self.utils.encryptAES(form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
						pass_http_auth = self.utils.encryptAES(form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
						http_auth_data = {'http_auth_user': user_http_auth.decode('utf-8'), 'http_auth_pass': pass_http_auth.decode('utf-8')}
						data_conf.update(http_auth_data)
						data_conf['use_http_auth'] = True
			if bandera_index_name == 1:
				write_index = form_dialog.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", str(data_conf['writeback_index']))
				data_conf['writeback_index'] = str(write_index)
			if bandera_max_hits == 1:
				max_hits = form_dialog.getDataNumber("Enter the maximum number of hits for the search (maximum 10000):", str(data_conf['max_hits']))
				data_conf['max_hits'] = int(max_hits)
			with open(self.utils.getPathTalert('conf') + '/es_conf.yaml', "w") as file_update:
				yaml.safe_dump(data_conf, file_update, default_flow_style = False)
			hash_modify = self.utils.getSha256File(self.utils.getPathTalert('conf') + '/es_conf.yaml')
			if hash_origen == hash_modify:
				form_dialog.d.msgbox("\nConfiguration file not modified", 7, 50, title = "Notification message")
			else:
				form_dialog.d.msgbox("\nModified configuration file", 7, 50, title = "Notification message")
				self.logger.createLogTool("Modified configuration file", 3)
			form_dialog.mainMenu()	
		except KeyError as exception:
			self.logger.createLogTool("Key Error: " + str(exception), 4)
			form_dialog.d.msgbox("\nKey Error: " + str(exception), 7, 50, title = "Error message")
			form_dialog.mainMenu()	

	"""
	Method that allows creating the configuration file with extension .yaml based on what was entered.

	Parameters:
	self -- Instance object.
	data_conf -- List containing all the data entered for the configuration file.
	"""
	def createFileConfiguration(self, data_conf):
		d = {'es_version': str(data_conf[0]),
			'es_host': str(data_conf[1]),
			'es_port': int(data_conf[2]),
			'rules_folder': str(data_conf[3]),
			'use_ssl': data_conf[4],
			'valid_certificates' : data_conf[5],
			'use_http_auth': data_conf[6]}

		if data_conf[6] == True:
			http_auth_data = {'http_auth_user' : data_conf[7].decode("utf-8"), 'http_auth_pass' : data_conf[8].decode("utf-8")}
			data_aux = {'writeback_index' : str(data_conf[9]), 'max_hits' : int(data_conf[10])}
			d.update(http_auth_data)
		else:
			data_aux = {'writeback_index' : str(data_conf[7]), 'max_hits' : int(data_conf[8])}
		d.update(data_aux)
		try:
			if(not os.path.isdir(self.utils.getPathTalert(str(data_conf[3])))):
			 os.mkdir(self.utils.getPathTalert(str(data_conf[3])))
			with open(self.utils.getPathTalert('conf') + '/es_conf.yaml', 'w') as yaml_file:
				yaml.dump(d, yaml_file, default_flow_style = False)
			self.utils.changeUidGid(Utils.getPathTalert('conf') + '/es_conf.yaml')
			self.utils.changeUidGid(Utils.getPathTalert(str(data_conf[3])))
		except OSError as exception:
			self.logger.createLogTool("Error" + str(exception), 4)