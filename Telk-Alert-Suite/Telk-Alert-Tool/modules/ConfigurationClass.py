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
	path_configuration_file = None

	"""
	Constructor for the Configuration class.

	Parameters:
	self -- An instantiated object of the Configuration class.
	form_dialog -- FormDialog class object.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		self.path_configuration_file = self.utils.getPathTelkAlert('conf') + "/telk_alert_conf.yaml"

	"""
	Method that requests the data for the creation of the Telk-Alert configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def createConfiguration(self):
		data_configuration = []
		es_version = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", "7.15")
		data_configuration.append(es_version)
		es_host = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", "localhost")
		data_configuration.append(es_host)
		es_port = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", "9200")
		data_configuration.append(es_port)
		name_folder_rules = self.form_dialog.getDataNameFolderOrFile("Enter the name of the directory where the alert rules will be saved:", "alert_rules")
		data_configuration.append(name_folder_rules)
		use_ssl_tls = self.form_dialog.getDataYesOrNo("\nDo you require Telk-Alert to communicate with ElasticSearch using the SSL/TLS protocol?", "SSL/TLS Connection")
		if use_ssl_tls == "ok":
			data_configuration.append(True)
			validate_certificate_ssl = self.form_dialog.getDataYesOrNo("\nDo you require Telk-Alert to validate the SSL certificate?", "Certificate Validation")
			if validate_certificate_ssl == "ok":
				data_configuration.append(True)
				path_certificate_file = self.form_dialog.getFile("/etc/Telk-Alert-Suite/Telk-Alert", "Select the CA certificate:", ".pem")
				data_configuration.append(path_certificate_file)
			else:
				data_configuration.append(False)
		else:
			data_configuration.append(False)
		use_http_authentication = self.form_dialog.getDataYesOrNo("\nIs the use of HTTP authentication required to connect to ElasticSearch?", "HTTP Authentication")
		if use_http_authentication == "ok":
			data_configuration.append(True)
			user_http_authentication = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
			data_configuration.append(user_http_authentication.decode('utf-8'))
			password_http_authentication = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
			data_configuration.append(password_http_authentication.decode('utf-8'))
		else:
			data_configuration.append(False)
		write_index_name = self.form_dialog.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", "telk-alert")
		data_configuration.append(write_index_name)
		self.createFileConfiguration(data_configuration)
		if path.exists(self.path_configuration_file):
			self.form_dialog.d.msgbox(text = "\nConfiguration file created.", height = 7, width = 50, title = "Notification Message")
			self.utils.createTelkAlertToolLog("Configuration file created", 1)
		else:
			self.form_dialog.d.msgbox(text = "\nError creating configuration file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that modifies one or more values of the Telk-Alert configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def updateConfiguration(self):
		list_fields_update = [("Version", "ElasticSearch Version", 0),
							  ("Host", "ElasticSearch Host", 0),
							  ("Port", "ElasticSearch Port", 0),
							  ("Folder", "Rules Folder", 0),
							  ("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							  ("HTTP Authentication", "Enable or disable Http authentication", 0),
							  ("Index", "Index name for logs", 0)]

		list_ssl_tls_true = [("Disable", "Disable SSL/TLS communication", 0),
							 ("Certificate Validation", "Modify certificate validation", 0)]

		list_ssl_tls_false = [("Enable", "Enable SSL/TLS communication", 0)]

		list_validate_certificate_true = [("Disable", "Disable certificate validation", 0),
								   		  ("Certificate File", "Change certificate file", 0)]

		list_validate_certificate_false = [("Enable", "Enable certificate validation", 0)]

		list_http_authentication_true = [("Disable", "Disable HTTP Authentication", 0),
								 		 ("Data", "Modify HTTP Authentication data", 0)]

		list_http_authentication_false = [("Enable", "Enable HTTP Authentication", 0)]

		list_http_authentication_data = [("Username", "Username for HTTP Authentication", 0),
								 		 ("Password", "User password", 0)]

		flag_es_version = 0
		flag_es_host = 0
		flag_es_port = 0
		flag_name_folder_rules = 0
		flag_use_ssl_tls = 0
		flag_use_http_authentication = 0
		flag_write_index_name = 0
		options_fields_update = self.form_dialog.getDataCheckList("Select one or more options:", list_fields_update, "Configuration Fields")
		for option in options_fields_update:
			if option == "Version":
				flag_es_version = 1
			elif option == "Host":
				flag_es_host = 1
			elif option == "Port":
				flag_es_port = 1
			elif option == "Folder":
				flag_name_folder_rules = 1
			elif option == "SSL/TLS":
				flag_use_ssl_tls = 1
			elif option == "HTTP Authentication":
				flag_use_http_authentication = 1
			elif option == "Index":
				flag_write_index_name = 1
		try:
			data_configuration = self.utils.readYamlFile(self.path_configuration_file, 'rU')
			hash_configuration_file_original = self.utils.getHashToFile(self.path_configuration_file)
			if flag_es_version == 1:
				es_version = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", data_configuration['es_version'])
				data_configuration['es_version'] = es_version
			if flag_es_host == 1:
				es_host = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", data_configuration['es_host'])
				data_configuration['es_host'] = es_host
			if flag_es_port == 1:
				es_port = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", str(data_configuration['es_port']))
				data_configuration['es_port'] = int(es_port)
			if flag_name_folder_rules == 1:
				name_folder_rules = self.form_dialog.getDataNameFolderOrFile("Enter the name of the directory where the alert rules will be saved:", data_configuration['name_folder_rules'])
				if not data_configuration['name_folder_rules'] == name_folder_rules:
					self.utils.renameFileOrDirectory(self.utils.getPathTelkAlert(data_configuration['name_folder_rules']), self.utils.getPathTelkAlert(name_folder_rules))
				data_configuration['name_folder_rules'] = name_folder_rules
			if flag_use_ssl_tls == 1:
				if data_configuration['use_ssl_tls'] == True:
					option_ssl_tls_true = self.form_dialog.getDataRadioList("Select a option:", list_ssl_tls_true, "SSL/TLS Connection")
					if option_ssl_tls_true == "Disable":
						del data_configuration['validate_certificate_ssl']
						if 'path_certificate_file' in data_configuration:
							del data_configuration['path_certificate_file']
						data_configuration['use_ssl_tls'] = False
					elif option_ssl_tls_true == "Certificate Validation":
						if data_configuration['validate_certificate_ssl'] == True:
							option_validate_certificate_true = self.form_dialog.getDataRadioList("Select a option:", list_validate_certificate_true, "Certificate Validation")
							if option_validate_certificate_true == "Disable":
								if 'path_certificate_file' in data_configuration:
									del data_configuration['path_certificate_file']
								data_configuration['validate_certificate_ssl'] = False
							elif option_validate_certificate_true == "Certificate File":
								path_certificate_file = self.form_dialog.getFile(data_configuration['path_certificate_file'], "Select the CA certificate:", ".pem")
								data_configuration['path_certificate_file'] = path_certificate_file
						else:
							option_validate_certificate_false = self.form_dialog.getDataRadioList("Select a option:", list_validate_certificate_false, "Certificate Validation")
							if option_validate_certificate_false == "Enable":
								data_configuration['validate_certificate_ssl'] = True
								path_certificate_file = self.form_dialog.getFile("/etc/Telk-Alert-Suite/Telk-Alert", "Select the CA certificate:", ".pem")
								validate_certificate_ssl_json = { 'path_certificate' : path_certificate_file }
								data_configuration.update(validate_certificate_ssl_json)
				else:
					option_ssl_tls_false = self.form_dialog.getDataRadioList("Select a option:", list_ssl_tls_false, "SSL/TLS Connection")
					if option_ssl_tls_false == "Enable":
						data_configuration['use_ssl_tls'] = True
						validate_certificate_ssl = self.form_dialog.getDataYesOrNo("\nDo you require Telk-Alert to validate the SSL certificate?", "Certificate Validation")
						if validate_certificate_ssl == "ok":
							path_certificate_file = self.form_dialog.getFile('/etc/Telk-Alert-Suite/Telk-Alert', "Select the CA certificate:", ".pem")
							validate_certificate_ssl_json = { 'validate_certificate_ssl' : True, 'path_certificate_file' : path_certificate_file }
						else:
							validate_certificate_ssl_json = { 'validate_certificate_ssl' : False }
						data_configuration.update(validate_certificate_ssl_json)
			if flag_use_http_authentication == 1:
				if data_configuration['use_http_authentication'] == True:
					option_http_authentication_true = self.form_dialog.getDataRadioList("Select a option:", list_http_authentication_true, "HTTP Authentication")
					if option_http_authentication_true == "Disable":
						del(data_configuration['use_http_authentication'])
						del(data_configuration['password_http_authentication'])
						data_configuration['use_http_authentication'] = False
					elif option_http_authentication_true == "Data":
						flag_http_authentication_user = 0
						flag_http_authentication_password = 0
						options_http_authentication_data = self.form_dialog.getDataCheckList("Select one or more options:", list_http_authentication_data, "HTTP Authentication")
						for option in options_http_authentication_data:
							if option == "Username":
								flag_http_authentication_user = 1
							elif option == "Password":
								flag_http_authentication_password = 1
						if flag_http_authentication_user == 1:
							user_http_authentication = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
							data_configuration['user_http_authentication'] = user_http_authentication.decode('utf-8')
						if flag_http_authentication_password == 1:
							password_http_authentication = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
							data_configuration['password_http_authentication'] = password_http_authentication.decode('utf-8')
				else:
					option_http_authentication_false = self.form_dialog.getDataRadioList("Select a option:", list_http_authentication_false, "HTTP Authentication")
					if option_http_authentication_false == "Enable":
						user_http_authentication = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
						password_http_authentication = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
						http_authentication_json = { 'user_http_authentication': user_http_authentication.decode('utf-8'), 'password_http_authentication': password_http_authentication.decode('utf-8') }
						data_configuration.update(http_authentication_json)
						data_configuration['use_http_authentication'] = True
			if flag_write_index_name == 1:
				write_index_name = self.form_dialog.getDataInputText("EEnter the name of the index that will be created in ElasticSearch:", data_configuration['write_index_name'])
				data_configuration['write_index_name'] = write_index_name
			self.utils.createYamlFile(data_configuration, self.path_configuration_file, 'w')
			hash_configuration_file_new = self.utils.getHashToFile(self.path_configuration_file)
			if hash_configuration_file_original == hash_configuration_file_new:
				self.form_dialog.d.msgbox(text = "\nThe configuration file was not modified.", height = 7, width = 50, title = "Notification Message")
			else:
				self.utils.createTelkAlertToolLog("The configuration file was modified", 2)
				self.form_dialog.d.msgbox(text = "\nThe configuration file was modified.", height = 7, width = 50, title = "Notification Message")	
			self.form_dialog.mainMenu()	
		except KeyError as exception:
			self.utils.createTelkAlertToolLog("Key Error: " + str(exception), 3)
			self.form_dialog.d.msgbox(text ="\nError modifying the configuration file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that creates the YAML file with the data entered for the Telk-Alert configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	data_configuration -- Object that contains the data to create the configuration file.
	"""
	def createFileConfiguration(self, data_configuration):
		data_configuration_json = {'es_version': data_configuration[0],
								   'es_host': data_configuration[1],
								   'es_port': int(data_configuration[2]),
								   'name_folder_rules': data_configuration[3],
								   'use_ssl_tls': data_configuration[4]}

		if data_configuration[4] == True:
			if data_configuration[5] == True:
				validate_certificate_ssl_json = { 'validate_certificate_ssl' : data_configuration[5] , 'path_certificate_file' : data_configuration[6] }
				last_index = 6
			else:
				validate_certificate_ssl_json = { 'validate_certificate_ssl' : data_configuration[5] }
				last_index = 5
			data_configuration_json.update(validate_certificate_ssl_json)
		else:
			last_index = 4
		if data_configuration[last_index + 1] == True:
			http_authentication_json = { 'use_http_authentication' : data_configuration[last_index + 1], 'user_http_authentication' : data_configuration[last_index + 2], 'password_http_authentication' : data_configuration[last_index + 3], 'write_index_name' : data_configuration[last_index + 4] }
		else:
			http_authentication_json = { 'use_http_authentication' : data_configuration[last_index + 1], 'write_index_name' : data_configuration[last_index + 2] }
		data_configuration_json.update(http_authentication_json)
		
		self.utils.createYamlFile(data_configuration_json, self.path_configuration_file, 'w')
		self.utils.createNewFolder(self.utils.getPathTelkAlert(data_configuration[3]))