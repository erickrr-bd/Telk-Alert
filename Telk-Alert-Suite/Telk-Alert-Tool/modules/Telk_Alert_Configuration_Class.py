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

		:arg action_to_cancel (object): Method to be called when the user chooses the cancel option.
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
			self.__dialog.createMessageDialog("\nValue Error. For more information, see the logs.", 7, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def modifyConfiguration(self):
		"""
		Method that allows to modify one or more values in the Telk-Alert configuration file.
		"""
		options_configuration_telk_alert_update = self.__dialog.createCheckListDialog("Select one or more options:", 12, 70, self.__constants.OPTIONS_CONFIGURATION_TELK_ALERT_UPDATE, "Telk-Alert Configuration Fields")
		try:
			telk_alert_data = self.__utils.readYamlFile(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE)
			hash_file_configuration_original = self.__utils.getHashFunctionToFile(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE)
			if "Host" in options_configuration_telk_alert_update:
				option_es_hosts_update = self.__dialog.createMenuDialog("Select a option:", 10, 50, self.__constants.OPTIONS_ES_HOSTS_UPDATE, "ELasticSearch Hosts Menu")
				if option_es_hosts_update == "1":
					number_master_nodes_es = self.__dialog.createInputBoxToNumberDialog("Enter the total number of master nodes to enter:", 9, 50, "1")
					list_to_form_dialog = self.__utils.createListToDialogForm(int(number_master_nodes_es), "IP Address")
					es_hosts = self.__dialog.createFormDialog("Enter IP addresses of the ElasticSearch master nodes:", list_to_form_dialog, 15, 50, "Add ElasticSearch Hosts")
					telk_alert_data["es_hosts"].extend(es_hosts)
				elif option_es_hosts_update == "2":
					list_to_form_dialog = self.__utils.convertListToDialogForm(telk_alert_data["es_hosts"], "IP Address")
					es_hosts = self.__dialog.createFormDialog("Enter IP addresses of the ElasticSearch master nodes:", list_to_form_dialog, 15, 50, "Update ElasticSearch Hosts")
					telk_alert_data["es_hosts"] = es_hosts
				elif option_es_hosts_update == "3":
					list_to_dialog = self.__utils.convertListToDialogList(telk_alert_data["es_hosts"], "IP Address")
					options_remove_es_hosts = self.__dialog.createCheckListDialog("Select one or more options:", 15, 50, list_to_dialog, "Remove ElasticSearch Hosts")
					for option in options_remove_es_hosts:
						telk_alert_data["es_hosts"].remove(option)
			if "Port" in options_configuration_telk_alert_update:
				es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, str(telk_alert_data['es_port']))
				telk_alert_data['es_port'] = int(es_port)
			if "Folder" in options_configuration_telk_alert_update:
				folder_rules_name = self.__dialog.createFolderOrFileNameDialog("Enter the folder's name where the alert rules will be stored:", 9, 50, telk_alert_data["folder_rules_name"])
				if not telk_alert_data["folder_rules_name"] == folder_rules_name:
					self.__utils.renameFileOrFolder(self.__constants.PATH_BASE_TELK_ALERT + '/' + telk_alert_data["folder_rules_name"], self.__constants.PATH_BASE_TELK_ALERT + '/' + folder_rules_name)
					telk_alert_data["folder_rules_name"] = folder_rules_name
			if "SSL/TLS" in options_configuration_telk_alert_update:
				if telk_alert_data["use_ssl_tls"] == True:
					option_ssl_tls_true = self.__dialog.createRadioListDialog("Select a option:", 10, 70, self.__constants.OPTIONS_SSL_TLS_TRUE, "SSL/TLS Connection")
					if option_ssl_tls_true == "Disable":
						del telk_alert_data['verificate_certificate_ssl']
						if "path_certificate_file" in telk_alert_data:
							del telk_alert_data["path_certificate_file"]
						telk_alert_data["use_ssl_tls"] = False
					elif option_ssl_tls_true == "Certificate Verification":
						if telk_alert_data["verificate_certificate_ssl"] == True:
							option_verificate_certificate_true = self.__dialog.createRadioListDialog("Select a option:", 10, 70, self.__constants.OPTIONS_VERIFICATE_CERTIFICATE_TRUE, "Certificate Verification")
							if option_verificate_certificate_true == "Disable":
								if "path_certificate_file" in telk_alert_data:
									del telk_alert_data["path_certificate_file"]
								telk_alert_data["verificate_certificate_ssl"] = False
							elif option_verificate_certificate_true == "Certificate File":
								path_certificate_file = self.__dialog.createFileDialog(telk_alert_data["path_certificate_file"], 8, 50, "Select the CA certificate:", ".pem")
								telk_alert_data["path_certificate_file"] = path_certificate_file
						else:
							option_verificate_certificate_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_VERIFICATE_CERTIFICATE_FALSE, "Certificate Verification")
							if option_verificate_certificate_false == "Enable":
								telk_alert_data["verificate_certificate_ssl"] = True
								path_certificate_file = self.__dialog.createFileDialog("/etc/Telk-Alert-Suite/Telk-Alert/configuration", 8, 50, "Select the CA certificate:", ".pem")
								verificate_certificate_ssl_json = {"path_certificate_file" : path_certificate_file}
								telk_alert_data.update(verificate_certificate_ssl_json)
				else:
					option_ssl_tls_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_SSL_TLS_FALSE, "SSL/TLS Connection")
					telk_alert_data['use_ssl_tls'] = True
					verificate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require that Telk-Alert verificates the SSL certificate?", 8, 50, "Certificate Verification")
					if verificate_certificate_ssl == "ok":
						path_certificate_file = self.__dialog.createFileDialog("/etc/Telk-Alert-Suite/Telk-Alert/configuration", 8, 50, "Select the CA certificate:", ".pem")
						verificate_certificate_ssl = {"verificate_certificate_ssl" : True, "path_certificate_file" : path_certificate_file}
					else:
						verificate_certificate_ssl = {"verificate_certificate_ssl" : False}
					telk_alert_data.update(verificate_certificate_ssl)
			if "Authentication" in options_configuration_telk_alert_update:
				if telk_alert_data["use_authentication_method"] == True:
					option_authentication_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_AUTHENTICATION_TRUE, "Authentication Method")
					if option_authentication_true == "Data":
						if telk_alert_data["authentication_method"] == "HTTP Authentication":
							option_authentication_method_true = self.__dialog.createRadioListDialog("Select a option:", 9, 60, self.__constants.OPTIONS_AUTHENTICATION_METHOD_TRUE, "HTTP Authentication")
							if option_authentication_method_true == "Data":
								options_http_authentication_data = self.__dialog.createCheckListDialog("Select one or more options:", 9, 60, self.__constants.OPTIONS_HTTP_AUTHENTICATION_DATA, "HTTP Authentication")	
								if "Username" in options_http_authentication_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)									
									telk_alert_data["user_http_authentication"] = user_http_authentication.decode("utf-8")
								if "Password" in options_http_authentication_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
									telk_alert_data["password_http_authentication"] = password_http_authentication.decode("utf-8")
							elif option_authentication_method_true == "Disable":
								passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
								api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
								api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
								del telk_alert_data["user_http_authentication"]
								del telk_alert_data["password_http_authentication"]
								telk_alert_data["authentication_method"] = "API Key"
								api_key_json = {"api_key_id" : api_key_id.decode("utf-8"), "api_key" : api_key.decode("utf-8")}
								telk_alert_data.update(api_key_json)
						elif telk_alert_data["authentication_method"] == "API Key":
							option_authentication_method_true = self.__dialog.createRadioListDialog("Select a option:", 9, 60, self.__constants.OPTIONS_AUTHENTICATION_METHOD_TRUE, "API Key")
							if option_authentication_method_true == "Data":
								options_api_key_data = self.__dialog.createCheckListDialog("Select one or more options:", 9, 50, self.__constants.OPTIONS_API_KEY_DATA, "API Key")
								if "API Key ID" in options_api_key_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
									telk_alert_data["api_key_id"] = api_key_id.decode("utf-8")
								if "API Key" in options_api_key_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
									telk_alert_data["api_key"] = api_key.decode("utf-8")
							elif option_authentication_method_true == "Disable":
								passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
								user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
								password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
								del telk_alert_data["api_key_id"]
								del telk_alert_data["api_key"]
								telk_alert_data["authentication_method"] = "HTTP Authentication"
								http_authentication_json = {"user_http_authentication" : user_http_authentication.decode("utf-8"), "password_http_authentication" : password_http_authentication.decode("utf-8")}
								telk_alert_data.update(http_authentication_json)
					elif option_authentication_true == "Disable":
						telk_alert_data["use_authentication_method"] = False
						if telk_alert_data["authentication_method"] == "HTTP Authentication":
							del telk_alert_data["user_http_authentication"]
							del telk_alert_data["password_http_authentication"]
						elif telk_alert_data["authentication_method"] == "API Key":
							del telk_alert_data["api_key_id"]
							del telk_alert_data["api_key"]
						del telk_alert_data["authentication_method"]
				else:
					option_authentication_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_AUTHENTICATION_FALSE, "Authentication Method")
					if option_authentication_false == "Enable":
						telk_alert_data["use_authentication_method"] = True
						option_authentication_method = self.__dialog.createRadioListDialog("Select a option:", 10, 55, self.__constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
						if option_authentication_method == "HTTP Authentication":
							passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
							user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
							password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
							http_authentication_json = {"authentication_method" : "HTTP Authentication", "user_http_authentication" : user_http_authentication.decode("utf-8"), "password_http_authentication" : password_http_authentication.decode("utf-8")}
							telk_alert_data.update(http_authentication_json)
						elif option_authentication_method == "API Key":
							passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
							api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
							api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
							api_key_json = {"authentication_method" : "API Key", "api_key_id" : api_key_id.decode("utf-8"), "api_key" : api_key.decode("utf-8")}
							telk_alert_data.update(api_key_json)
			self.__utils.createYamlFile(telk_alert_data, self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE)
			hash_file_configuration_new = self.__utils.getHashFunctionToFile(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE)
			if hash_file_configuration_original == hash_file_configuration_new:
				self.__dialog.createMessageDialog("\nTelk-Alert configuration file not modified.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nTelk-Alert configuration file modified.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Telk-Alert configuration file modified", 2, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nValue Error. For more information, see the logs.", 7, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 7, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def showConfigurationData(self):
		"""
		Method that displays the data stored in the Telk-Alert configuration file.
		"""
		try:
			telk_alert_data = self.__utils.convertDataYamlFileToString(self.__constants.PATH_TELK_ALERT_CONFIGURATION_FILE)
			message_to_display = "\nTelk-Alert Configuration:\n\n" + telk_alert_data
			self.__dialog.createScrollBoxDialog(message_to_display, 18, 70, "Telk-Alert Configuration")
		except (FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 7, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__showConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def __createYamlFileConfiguration(self, telk_alert_data):
		""" 	
		Method that creates the YAML file corresponding to the Telk-Alert configuration.

		:arg telk_alert_data (dict): Data to be stored in the configuration file.
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