from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related to the configuration of Telk-Alert.
"""
class TelkAlertConfiguration:

	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel: Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def createConfiguration(self):
		"""
		Method that collects the information for the creation of the Telk-Alert configuration file.
		"""
		telk_alert_data = []
		try:
			number_master_nodes_es = self.__dialog.createInputBoxToNumberDialog("Enter the total number of master nodes to enter:", 9, 50, "1")
			list_to_form_dialog = self.__utils.createListToDialogForm(int(number_master_nodes_es), "IP Address")
			es_hosts = self.__dialog.createFormDialog("Enter IP addresses of the ElasticSearch master nodes:", list_to_form_dialog, 15, 50, "ElasticSearch Hosts")
			telk_alert_data.append(es_hosts)
			es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, "9200")
			telk_alert_data.append(es_port)
			folder_rules_name = self.__dialog.createFolderOrFileNameDialog("Enter the folder's name where the alert rules will be stored:", 9, 50, "folder_alert_rules")
			telk_alert_data.append(folder_rules_name)
			use_ssl_tls = self.__dialog.createYesOrNoDialog("\nDo you require that Telk-Alert communicates with ElasticSearch using the SSL/TLS protocol?", 8, 50, "SSL/TLS Connection")
			if use_ssl_tls == "ok":
				telk_alert_data.append(True)
				verificate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require that Telk-Alert verificates the SSL certificate?", 8, 50, "Certificate Verification")
				if verificate_certificate_ssl == "ok":
					telk_alert_data.append(True)
					path_certificate_file = self.__dialog.createFileDialog("/etc/Telk-Alert-Suite/Telk-Alert/configuration", 8, 50, "Select the CA certificate:", ".pem")
					telk_alert_data.append(path_certificate_file)
				else:
					telk_alert_data.append(False)
			else:
				telk_alert_data.append(False)
			use_authentication_method = self.__dialog.createYesOrNoDialog("\nDo you require that Telk-Alert uses an authentication method (HTTP Authentication or API Key) to connect with ElasticSearch?", 9, 50, "Authentication Method")
			if use_authentication_method == "ok":
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telk_alert_data.append(True)
				option_authentication_method = self.__dialog.createRadioListDialog("Select a option:", 9, 55, self.__constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
				telk_alert_data.append(option_authentication_method)
				if option_authentication_method == "HTTP Authentication":
					user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
					telk_alert_data.append(user_http_authentication.decode("utf-8"))
					password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 9, 50, "password", True), passphrase)
					telk_alert_data.append(password_http_authentication.decode("utf-8"))
				elif option_authentication_method == "API Key":
					api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
					telk_alert_data.append(api_key_id.decode("utf-8"))
					api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
					telk_alert_data.append(api_key.decode("utf-8"))
			else:
				telk_alert_data.append(False)
			self.__createYamlFileConfiguration(telk_alert_data)
			if path.exists(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE):
				self.__dialog.createMessageDialog("\nTelk-Alert configuration file created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Telk-Alert configuration file created", 1, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nIncorrect data. For more information, see the logs.", 7, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\nI/O Error. For more information, see the logs.", 7, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def modifyConfiguration(self):
		"""
		Method that allows to modify one or more values in the Telk-Alert configuration file.
		"""
		options_fields_update = self.__dialog.createCheckListDialog("Select one or more options:", 12, 70, self.__constants.OPTIONS_FIELDS_UPDATE, "Configuration Fields")
		try:
			data_configuration = self.__utils.readYamlFile(self.__constants.PATH_FILE_CONFIGURATION)
			hash_file_configuration_original = self.__utils.getHashFunctionToFile(self.__constants.PATH_FILE_CONFIGURATION)
			if "Host" in options_fields_update:
				es_host = self.__dialog.createInputBoxToIPDialog("Enter the ElasticSearch IP address:", 8, 50, data_configuration['es_host'])
				data_configuration['es_host'] = es_host
			if "Port" in options_fields_update:
				es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, data_configuration['es_port'])
				data_configuration['es_port'] = int(es_port)
			if "Folder" in options_fields_update:
				name_folder_rules = self.__dialog.createFolderOrFileNameDialog("Enter the name of the directory where the alert rules will be saved:", 10, 50, data_configuration['name_folder_rules'])
				if not data_configuration['name_folder_rules'] == name_folder_rules:
					self.__utils.renameFileOrFolder(self.__constants.PATH_BASE_TELK_ALERT + '/' + data_configuration['name_folder_rules'], self.__constants.PATH_BASE_TELK_ALERT + '/' + name_folder_rules)
					data_configuration['name_folder_rules'] = name_folder_rules
			if 'SSL/TLS' in options_fields_update:
				if data_configuration['use_ssl_tls'] == True:
					option_ssl_tls_true = self.__dialog.createRadioListDialog("Select a option:", 10, 70, self.__constants.OPTIONS_SSL_TLS_TRUE, "SSL/TLS Connection")
					if option_ssl_tls_true == "Disable":
						del data_configuration['validate_certificate_ssl']
						if 'path_certificate_file' in data_configuration:
							del data_configuration['path_certificate_file']
						data_configuration['use_ssl_tls'] = False
					elif option_ssl_tls_true == "Certificate Validation":
						if data_configuration['validate_certificate_ssl'] == True:
							option_validate_certificate_true = self.__dialog.createRadioListDialog("Select a option:", 10, 70, self.__constants.OPTIONS_VALIDATE_CERTIFICATE_TRUE, "Certificate Validation")
							if option_validate_certificate_true == "Disable":
								if 'path_certificate_file' in data_configuration:
									del data_configuration['path_certificate_file']
								data_configuration['validate_certificate_ssl'] = False
							elif data_configuration['validate_certificate_ssl'] == "Certificate File":
								path_certificate_file = self.__dialog.createFileDialog(data_configuration['path_certificate_file'], 8, 50, "Select the CA certificate:", ".pem")
								data_configuration['path_certificate_file'] = path_certificate_file
						else:
							option_validate_certificate_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_VALIDATE_CERTIFICATE_FALSE, "Certificate Validation")
							if option_validate_certificate_false == "Enable":
								data_configuration['validate_certificate_ssl'] = True
								path_certificate_file = self.__dialog.createFileDialog("/etc", 8, 50, "Select the CA certificate:", ".pem")
								validate_certificate_ssl_json = {'path_certificate_file' : path_certificate_file}
								data_configuration.update(validate_certificate_ssl_json)
				else:
					option_ssl_tls_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_SSL_TLS_FALSE, "SSL/TLS Connection")
					data_configuration['use_ssl_tls'] = True
					validate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require VS-Monitor to validate the SSL certificate?", 8, 50, "Certificate Validation")
					if validate_certificate_ssl == "ok":
						path_certificate_file = self.__dialog.createFileDialog("/etc", 8, 50, "Select the CA certificate:", ".pem")
						validate_certificate_ssl_json = {'validate_certificate_ssl' : True, 'path_certificate_file' : path_certificate_file}
					else:
						validate_certificate_ssl_json = {'validate_certificate_ssl' : False}
					data_configuration.update(validate_certificate_ssl_json)
			if 'HTTP Authentication' in options_fields_update:
				if data_configuration['use_http_authentication'] == True:
					option_http_authentication_true = self.__dialog.createRadioListDialog("Select a option:", 10, 70, self.__constants.OPTIONS_HTTP_AUTHENTICATION_TRUE, "HTTP Authentication")
					if option_http_authentication_true == "Disable":
						del data_configuration['user_http_authentication']
						del data_configuration['password_http_authentication']
						data_configuration['use_http_authentication'] = False
					elif option_http_authentication_true == "Data":
						passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
						options_http_authentication_data = self.__dialog.createCheckListDialog("Select one or more options:", 10, 70, self.__constants.OPTIONS_HTTP_AUTHENTICATION_DATA, "HTTP Authentication")
						if 'Username' in options_http_authentication_data:
							user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
							data_configuration['user_http_authentication'] = user_http_authentication.decode('utf-8')
						if 'Password' in options_http_authentication_data:
							password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
							data_configuration['password_http_authentication'] = password_http_authentication.decode('utf-8')
				else:
					option_http_authentication_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_HTTP_AUTHENTICATION_FALSE, "HTTP Authentication")
					if option_http_authentication_false == "Enable":
						passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
						user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
						password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
						http_authentication_json = {'user_http_authentication' : user_http_authentication.decode('utf-8'), 'password_http_authentication' : password_http_authentication.decode('utf-8')}
						data_configuration.update(http_authentication_json)
						data_configuration['use_http_authentication'] = True
			self.__utils.createYamlFile(data_configuration, self.__constants.PATH_FILE_CONFIGURATION)
			hash_file_configuration_new = self.__utils.getHashFunctionToFile(self.__constants.PATH_FILE_CONFIGURATION)
			if hash_file_configuration_original == hash_file_configuration_new:
				self.__dialog.createMessageDialog("\nConfiguration file not modified.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nModified configuration file.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Modified configuration file", 2, "__configuration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__configuration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except (IOError, FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\n", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__configuration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG,user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()


	def __createYamlFileConfiguration(self, telk_alert_data):
		""" 	
		Method that creates the YAML file corresponding to the Telk-Alert configuration.

		:arg telk_alert_data: Data to be stored in the configuration file.
		"""
		telk_alert_data_json = {
			"es_hosts" : telk_alert_data[0],
			"es_port" : int(telk_alert_data[1]),
			"folder_rules_name" : telk_alert_data[2],
			"use_ssl_tls" : telk_alert_data[3]
		}

		if telk_alert_data[3] == True:
			if telk_alert_data[4] == True:
				verificate_certificate_ssl_json = {"verificate_certificate_ssl" : telk_alert_data[4], "path_certificate_file" : telk_alert_data[5]}
				last_index = 5
			else:
				verificate_certificate_ssl_json = {"verificate_certificate_ssl" : telk_alert_data[4]}
				last_index = 4
			telk_alert_data_json.update(verificate_certificate_ssl_json)
		else:
			last_index = 3
		if telk_alert_data[last_index + 1] == True:
			if telk_alert_data[last_index + 2] == "HTTP Authentication":
				http_authentication_json = {"use_authentication_method" : telk_alert_data[last_index + 1], "authentication_method" : telk_alert_data[last_index + 2], "user_http_authentication" : telk_alert_data[last_index + 3], "password_http_authentication" : telk_alert_data[last_index + 4]}
				telk_alert_data_json.update(http_authentication_json)
			elif telk_alert_data[last_index + 2] == "API Key":
				api_key_json = {"use_authentication_method" : telk_alert_data[last_index + 1], "authentication_method" : telk_alert_data[last_index + 2], "api_key_id" : telk_alert_data[last_index + 3], "api_key" : telk_alert_data[last_index + 4]}
				telk_alert_data_json.update(api_key_json)
		else:
			authentication_method_json = {"use_authentication_method" : telk_alert_data[last_index + 1]}
			telk_alert_data_json.update(authentication_method_json)

		self.__utils.createYamlFile(telk_alert_data_json, self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE)
		self.__utils.createNewFolder(self.__constants.PATH_BASE_TELK_ALERT + '/' + telk_alert_data[2])
		self.__utils.changeOwnerToPath(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE, self.__constants.USER, self.__constants.GROUP)
		self.__utils.changeOwnerToPath(self.__constants.PATH_BASE_TELK_ALERT + '/' + telk_alert_data[2], self.__constants.USER, self.__constants.GROUP)