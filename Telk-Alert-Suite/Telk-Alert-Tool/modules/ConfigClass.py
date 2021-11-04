from os import path
from modules.UtilsClass import Utils

"""
Class that allows managing everything related to the Telk-Alert configuration.
"""
class Configuration:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Property that stores an object of the FormDialog class.
	"""
	form_dialog = None

	"""
	Property that stores the path of the Telk-Alert configuration file.
	"""
	conf_file = None

	"""
	Constructor for the Configuration class.

	Parameters:
	self -- An instantiated object of the Configuration class.
	form_dialog -- FormDialog class object.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		self.conf_file = self.utils.getPathTelkAlert('conf') + "/telk_alert_conf.yaml"

	"""
	Method that requests the data for the creation of the Telk-Alert configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def createConfiguration(self):
		data_conf = []
		version_es = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", "7.15")
		data_conf.append(version_es)
		host_es = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", "localhost")
		data_conf.append(host_es)
		port_es = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", "9200")
		data_conf.append(port_es)
		folder_rules = self.form_dialog.getDataNameFolderOrFile("Enter the name of the folder where the alert rules will be hosted:", "alert_rules")
		data_conf.append(folder_rules)
		use_ssl = self.form_dialog.getDataYesOrNo("\nDo you want Telk-Alert to connect to ElasticSearch using the SSL/TLS protocol?", "Connection Via SSL/TLS")
		if use_ssl == "ok":
			data_conf.append(True)
			valid_certificate = self.form_dialog.getDataYesOrNo("\nDo you want the certificates for SSL/TLS communication to be validated?", "Certificate Validation")
			if valid_certificate == "ok":
				data_conf.append(True)
				cert_file = self.form_dialog.getFile("/etc/Telk-Alert-Suite/Telk-Alert", "Select the CA certificate:", ".pem")
				data_conf.append(cert_file)
			else:
				data_conf.append(False)
		else:
			data_conf.append(False)
		http_auth = self.form_dialog.getDataYesOrNo("\nIs the use of HTTP authentication required to connect to ElasticSearch?", "HTTP Authentication")
		if http_auth == "ok":
			data_conf.append(True)
			user_http_auth = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
			data_conf.append(user_http_auth.decode('utf-8'))
			pass_http_auth = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
			data_conf.append(pass_http_auth.decode('utf-8'))
		else:
			data_conf.append(False)
		write_index = self.form_dialog.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", "telk-alert")
		data_conf.append(write_index)
		self.createFileConfiguration(data_conf)
		if path.exists(self.conf_file):
			self.form_dialog.d.msgbox(text = "\nConfiguration file created.", height = 7, width = 50, title = "Notification Message")
			self.utils.createTelkAlertToolLog("Configuration file created", 1)
		else:
			self.form_dialog.d.msgbox(text = "\nError creating configuration file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that modifies one or more fields of the Telk-Alert configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	form_dialog -- A FormDialogs class object.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def modifyConfiguration(self, form_dialog):
		options_conf_prop = [("Version", "ElasticSearch Version", 0),
							("Host", "ElasticSearch Host", 0),
							("Port", "ElasticSearch Port", 0),
							("Folder name", "Rules Folder", 0),
							("Use SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							("Use HTTP auth", "Enable or disable Http authentication", 0),
							("Index name", "Index name for logs", 0),
							("Hits", "Maximum hits in a search", 0)]

		options_ssl_true = [("To disable", "Disable SSL/TLS communication", 0),
							("Modify", "Modify certificate validation", 0)]

		options_ssl_false = [("Enable", "Enable SSL/TLS communication", 0)]

		options_valid_cert_true = [("To disable", "Disable certificate validation", 0),
									("Modify", "Change certificate file", 0)]

		options_valid_cert_false = [("Enable", "Enable certificate validation", 0)]

		options_http_auth_true = [("To disable", "Disable HTTP Authentication", 0),
								 ("Modify data", "Modify HTTP Authentication data", 0)]

		options_http_auth_false = [("Enable", "Enable HTTP Authentication", 0)]

		options_http_auth_data = [("Username", "Username for HTTP Authentication", 0),
								 ("Password", "User password", 0)]

		flag_version = 0
		flag_host = 0
		flag_port = 0
		flag_folder_name = 0
		flag_use_ssl = 0
		flag_http_auth = 0
		flag_index_name = 0
		flag_max_hits = 0
		opt_conf_prop = form_dialog.getDataCheckList("Select one or more options", options_conf_prop, "Update configuration file")
		for opt_prop in opt_conf_prop:
			if opt_prop == "Version":
				flag_version = 1
			if opt_prop == "Host":
				flag_host = 1
			if opt_prop == "Port":
				flag_port = 1
			if opt_prop == "Folder name":
				flag_folder_name = 1
			if opt_prop == "Use SSL/TLS":
				flag_use_ssl = 1
			if opt_prop == "Validate certificates":
				flag_validate_cert = 1
			if opt_prop == "Use HTTP auth":
				flag_http_auth = 1
			if opt_prop == "Index name":
				flag_index_name = 1
			if opt_prop == "Hits":
				flag_max_hits = 1
		try:
			with open(self.utils.getPathTalert('conf') + '/es_conf.yaml', "rU") as f:
				data_conf = yaml.safe_load(f)
			hash_origen = self.utils.getSha256File(self.utils.getPathTalert('conf') + '/es_conf.yaml', form_dialog)
			if flag_version == 1:
				version_es = form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", str(data_conf['es_version']))
				data_conf['es_version'] = str(version_es)
			if flag_host == 1:
				host_es = form_dialog.getDataIP("Enter the ElasticSearch IP address:", str(data_conf['es_host']))
				data_conf['es_host'] = str(host_es)
			if flag_port == 1:
				port_es = form_dialog.getDataPort("Enter the ElasticSearch listening port:", str(data_conf['es_port']))
				data_conf['es_port'] = int(port_es)
			if flag_folder_name == 1:
				folder_rules = form_dialog.getDataNameFolderOrFile("Enter the name of the folder where the alert rules will be hosted:", data_conf['rules_folder'])
				data_conf['rules_folder'] = str(folder_rules)
				if(not os.path.isdir(self.utils.getPathTalert(str(folder_rules)))):
					os.mkdir(self.utils.getPathTalert(str(folder_rules)))
					self.utils.changeUidGid(self.utils.getPathTalert(str(folder_rules)))
			if flag_use_ssl == 1:
				if data_conf['use_ssl'] == True:
					opt_ssl_true = form_dialog.getDataRadioList("Select a option:", options_ssl_true, "Connection via SSL/TLS")
					if opt_ssl_true == "To disable":
						del data_conf['valid_certificates']
						if 'path_cert' in data_conf:
							del data_conf['path_cert']
						data_conf['use_ssl'] = False
					if opt_ssl_true == "Modify":
						if data_conf['valid_certificates'] == True:
							opt_valid_cert_true = form_dialog.getDataRadioList("Select a option:", options_valid_cert_true, "Certificate Validation")
							if opt_valid_cert_true == "To disable":
								if 'path_cert' in data_conf:
									del data_conf['path_cert']
								data_conf['valid_certificates'] = False
							if opt_valid_cert_true == "Modify":
								cert_file = form_dialog.getFileOrDirectory(data_conf['path_cert'], "Select the CA certificate:")
								data_conf['path_cert'] = str(cert_file)
						else:
							opt_valid_cert_false = form_dialog.getDataRadioList("Select a option:", options_valid_cert_false, "Certificate Validation")
							if opt_valid_cert_false == "Enable":
								data_conf['valid_certificates'] = True
								cert_file = form_dialog.getFileOrDirectory('/etc/Telk-Alert-Suite/Telk-Alert', "Select the CA certificate:")
								cert_file_json = { 'path_cert' : str(cert_file) }
								data_conf.update(cert_file_json)
				else:
					opt_ssl_false = form_dialog.getDataRadioList("Select a option:", options_ssl_false, "Connection via SSL/TLS")
					if opt_ssl_false == "Enable":
						data_conf['use_ssl'] = True
						valid_certificates = form_dialog.getDataYesOrNo("\nDo you want the certificates for SSL/TLS communication to be validated?", "Certificate Validation")
						if valid_certificates == "ok":
							cert_file = form_dialog.getFileOrDirectory('/etc/Telk-Alert-Suite/Telk-Alert', "Select the CA certificate:")
							valid_certificates_json = { 'valid_certificates' : True, 'path_cert' : str(cert_file) }
						else:
							valid_certificates_json = { 'valid_certificates' : False }
						data_conf.update(valid_certificates_json)
			if flag_http_auth == 1:
				if data_conf['use_http_auth'] == True:
					opt_http_auth_true = form_dialog.getDataRadioList("Select a option:", options_http_auth_true, "HTTP Authentication")
					if opt_http_auth_true == "To disable":
						del(data_conf['http_auth_user'])
						del(data_conf['http_auth_pass'])
						data_conf['use_http_auth'] = False
					if opt_http_auth_true == "Modify data":
						flag_http_auth_user = 0
						flag_http_auth_pass = 0
						opt_mod_http_auth = form_dialog.getDataCheckList("Select one or more options:", options_http_auth_data, "HTTP Authentication")
						for opt_mod in opt_mod_http_auth:
							if opt_mod == "Username":
								flag_http_auth_user = 1
							if opt_mod == "Password":
								flag_http_auth_pass = 1
						if flag_http_auth_user == 1:
							user_http_auth_mod = self.utils.encryptAES(form_dialog.getDataInputText("Enter the username for HTTP authentication:", self.utils.decryptAES(data_conf['http_auth_user'], form_dialog).decode('utf-8')), form_dialog)
							data_conf['http_auth_user'] = user_http_auth_mod.decode('utf-8')
						if flag_http_auth_pass == 1:
							pass_http_auth_mod = self.utils.encryptAES(form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"), form_dialog)
							data_conf['http_auth_pass'] = pass_http_auth_mod.decode('utf-8')
				else:
					opt_http_auth_false = form_dialog.getDataRadioList("Select a option:", options_http_auth_false, "HTTP Authentication")
					if opt_http_auth_false == "Enable":
						user_http_auth = self.utils.encryptAES(form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"), form_dialog)
						pass_http_auth = self.utils.encryptAES(form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"), form_dialog)
						http_auth_data = {'http_auth_user': user_http_auth.decode('utf-8'), 'http_auth_pass': pass_http_auth.decode('utf-8')}
						data_conf.update(http_auth_data)
						data_conf['use_http_auth'] = True
			if flag_index_name == 1:
				write_index = form_dialog.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", str(data_conf['writeback_index']))
				data_conf['writeback_index'] = str(write_index)
			if flag_max_hits == 1:
				max_hits = form_dialog.getDataNumber("Enter the maximum number of hits for the search (maximum 10000):", str(data_conf['max_hits']))
				data_conf['max_hits'] = int(max_hits)
			with open(self.utils.getPathTalert('conf') + '/es_conf.yaml', "w") as file_update:
				yaml.safe_dump(data_conf, file_update, default_flow_style = False)
			hash_modify = self.utils.getSha256File(self.utils.getPathTalert('conf') + '/es_conf.yaml', form_dialog)
			if hash_origen == hash_modify:
				form_dialog.d.msgbox("\nConfiguration file not modified", 7, 50, title = "Notification message")
			else:
				form_dialog.d.msgbox("\nModified configuration file", 7, 50, title = "Notification message")
				self.utils.createLogTool("Modified configuration file", 2)
			form_dialog.mainMenu()	
		except KeyError as exception:
			self.utils.createLogTool("Key not found in configuration file: " + str(exception), 4)
			form_dialog.d.msgbox("\nKey not found in configuration file: " + str(exception), 7, 50, title = "Error message")
			form_dialog.mainMenu()
		except OSError as exception:
			self.utils.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nError opening the configuration file. For more details, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()

	"""
	Method that creates the YAML file with the data entered for the Telk-Alert configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	data_conf -- Object that contains the data to create the configuration file.
	"""
	def createFileConfiguration(self, data_conf):
		data_json = {'es_version': data_conf[0],
					'es_host': data_conf[1],
					'es_port': int(data_conf[2]),
					'rules_folder': data_conf[3],
					'use_ssl': data_conf[4]}

		if data_conf[4] == True:
			if data_conf[5] == True:
				valid_certificate_json = { 'valid_certificate' : data_conf[5] , 'path_certificate' : data_conf[6] }
				last_index = 6
			else:
				valid_certificate_json = { 'valid_certificate' : data_conf[5] }
				last_index = 5
			data_json.update(valid_certificate_json)
		else:
			last_index = 4
		if data_conf[last_index + 1] == True:
			http_auth_json = { 'use_http_auth' : data_conf[last_index + 1], 'http_auth_user' : data_conf[last_index + 2], 'http_auth_pass' : data_conf[last_index + 3], 'writeback_index' : data_conf[last_index + 4] }
		else:
			http_auth_json = { 'use_http_auth' : data_conf[last_index + 1], 'writeback_index' : data_conf[last_index + 2] }
		data_json.update(http_auth_json)
		
		self.utils.createYamlFile(data_json, self.conf_file, 'w')
		self.utils.createNewFolder(self.utils.getPathTelkAlert(data_conf[3]))