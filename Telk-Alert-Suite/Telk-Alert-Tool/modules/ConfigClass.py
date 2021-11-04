from os import path, rename
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
		use_ssl = self.form_dialog.getDataYesOrNo("\nDo you want Snap-Tool to connect to ElasticSearch using the SSL/TLS protocol?", "SSL/TLS Connection")
		if use_ssl == "ok":
			data_conf.append(True)
			valid_certificate = self.form_dialog.getDataYesOrNo("\nDo you want the certificate for SSL/TLS communication to be validated?", "Certificate Validation")
			if valid_certificate == "ok":
				data_conf.append(True)
				path_cert_file = self.form_dialog.getFile("/etc/Telk-Alert-Suite/Telk-Alert", "Select the CA certificate:", ".pem")
				data_conf.append(path_cert_file)
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

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def updateConfiguration(self):
		options_fields_update = [("Version", "ElasticSearch Version", 0),
								("Host", "ElasticSearch Host", 0),
								("Port", "ElasticSearch Port", 0),
								("Folder", "Rules Folder", 0),
								("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
								("HTTP Authentication", "Enable or disable Http authentication", 0),
								("Index", "Index name for logs", 0)]

		options_ssl_true = [("Disable", "Disable SSL/TLS communication", 0),
							("Certificate Validation", "Modify certificate validation", 0)]

		options_ssl_false = [("Enable", "Enable SSL/TLS communication", 0)]

		options_valid_cert_true = [("Disable", "Disable certificate validation", 0),
								   ("Certificate File", "Change certificate file", 0)]

		options_valid_cert_false = [("Enable", "Enable certificate validation", 0)]

		options_http_auth_true = [("Disable", "Disable HTTP Authentication", 0),
								 ("Data", "Modify HTTP Authentication data", 0)]

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
		opt_conf_fields = self.form_dialog.getDataCheckList("Select one or more options:", options_fields_update, "Configuration File Fields")
		for option in opt_conf_fields:
			if option == "Version":
				flag_version = 1
			elif option == "Host":
				flag_host = 1
			elif option == "Port":
				flag_port = 1
			elif option == "Folder":
				flag_folder_name = 1
			elif option == "SSL/TLS":
				flag_use_ssl = 1
			elif option == "HTTP Authentication":
				flag_http_auth = 1
			elif option == "Index":
				flag_index_name = 1
		try:
			data_conf = self.utils.readYamlFile(self.conf_file, 'rU')
			hash_original = self.utils.getHashToFile(self.conf_file)
			if flag_version == 1:
				version_es = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", data_conf['es_version'])
				data_conf['es_version'] = version_es
			if flag_host == 1:
				host_es = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", data_conf['es_host'])
				data_conf['es_host'] = host_es
			if flag_port == 1:
				port_es = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", str(data_conf['es_port']))
				data_conf['es_port'] = int(port_es)
			if flag_folder_name == 1:
				folder_rules = self.form_dialog.getDataNameFolderOrFile("Enter the name of the folder where the alert rules will be hosted:", data_conf['rules_folder'])
				if not data_conf['rules_folder'] == folder_rules:
					rename(self.utils.getPathTelkAlert(data_conf['rules_folder']), self.utils.getPathTelkAlert(folder_rules))
				data_conf['rules_folder'] = folder_rules
			if flag_use_ssl == 1:
				if data_conf['use_ssl'] == True:
					opt_ssl_true = self.form_dialog.getDataRadioList("Select a option:", options_ssl_true, "SSL/TLS Connection")
					if opt_ssl_true == "Disable":
						del data_conf['valid_certificate']
						if 'path_certificate' in data_conf:
							del data_conf['path_certificate']
						data_conf['use_ssl'] = False
					elif opt_ssl_true == "Certificate Validation":
						if data_conf['valid_certificate'] == True:
							opt_valid_cert_true = self.form_dialog.getDataRadioList("Select a option:", options_valid_cert_true, "Certificate Validation")
							if opt_valid_cert_true == "Disable":
								if 'path_certificate' in data_conf:
									del data_conf['path_certificate']
								data_conf['valid_certificate'] = False
							elif opt_valid_cert_true == "Certificate File":
								path_cert_file = self.form_dialog.getFile(data_conf['path_certificate'], "Select the CA certificate:", ".pem")
								data_conf['path_certificate'] = path_cert_file
						else:
							opt_valid_cert_false = self.form_dialog.getDataRadioList("Select a option:", options_valid_cert_false, "Certificate Validation")
							if opt_valid_cert_false == "Enable":
								data_conf['valid_certificate'] = True
								path_cert_file = self.form_dialog.getFile("/etc/Telk-Alert-Suite/Telk-Alert", "Select the CA certificate:", ".pem")
								valid_certificates_json = { 'path_certificate' : path_cert_file }
								data_conf.update(valid_certificates_json)
				else:
					opt_ssl_false = self.form_dialog.getDataRadioList("Select a option:", options_ssl_false, "SSL/TLS Connection")
					if opt_ssl_false == "Enable":
						data_conf['use_ssl'] = True
						valid_certificate = self.form_dialog.getDataYesOrNo("\nDo you want the certificate for SSL/TLS communication to be validated?", "Certificate Validation")
						if valid_certificate == "ok":
							path_cert_file = self.form_dialog.getFile('/etc/Telk-Alert-Suite/Telk-Alert', "Select the CA certificate:", ".pem")
							valid_certificates_json = { 'valid_certificate' : True, 'path_certificate' : path_cert_file }
						else:
							valid_certificates_json = { 'valid_certificate' : False }
						data_conf.update(valid_certificates_json)
			if flag_http_auth == 1:
				if data_conf['use_http_auth'] == True:
					opt_http_auth_true = self.form_dialog.getDataRadioList("Select a option:", options_http_auth_true, "HTTP Authentication")
					if opt_http_auth_true == "Disable":
						del(data_conf['http_auth_user'])
						del(data_conf['http_auth_pass'])
						data_conf['use_http_auth'] = False
					elif opt_http_auth_true == "Data":
						flag_http_auth_user = 0
						flag_http_auth_pass = 0
						opt_mod_http_auth = self.form_dialog.getDataCheckList("Select one or more options:", options_http_auth_data, "HTTP Authentication")
						for opt_mod in opt_mod_http_auth:
							if opt_mod == "Username":
								flag_http_auth_user = 1
							elif opt_mod == "Password":
								flag_http_auth_pass = 1
						if flag_http_auth_user == 1:
							user_http_auth = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
							data_conf['http_auth_user'] = user_http_auth.decode('utf-8')
						if flag_http_auth_pass == 1:
							pass_http_auth = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
							data_conf['http_auth_pass'] = pass_http_auth.decode('utf-8')
				else:
					opt_http_auth_false = self.form_dialog.getDataRadioList("Select a option:", options_http_auth_false, "HTTP Authentication")
					if opt_http_auth_false == "Enable":
						user_http_auth = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
						pass_http_auth = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
						http_auth_data = { 'http_auth_user': user_http_auth.decode('utf-8'), 'http_auth_pass': pass_http_auth.decode('utf-8') }
						data_conf.update(http_auth_data)
						data_conf['use_http_auth'] = True
			if flag_index_name == 1:
				write_index = self.form_dialog.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", data_conf['writeback_index'])
				data_conf['writeback_index'] = write_index
			self.utils.createYamlFile(data_conf, self.conf_file, 'w')
			hash_update = self.utils.getHashToFile(self.conf_file)
			if hash_original == hash_update:
				self.form_dialog.d.msgbox(text = "\nThe configuration file was not modified.", height = 7, width = 50, title = "Notification Message")
			else:
				self.form_dialog.d.msgbox(text = "\nThe configuration file was modified.", height = 7, width = 50, title = "Notification Message")
				self.utils.createTelkAlertToolLog("The configuration file was modified", 2)
			self.form_dialog.mainMenu()	
		except KeyError as exception:
			self.utils.createTelkAlertToolLog("Key Error: " + exception, 3)
			self.form_dialog.d.msgbox(text ="\nError modifying the configuration file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

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