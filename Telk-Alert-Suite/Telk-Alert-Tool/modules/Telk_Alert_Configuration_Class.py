from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages the Telk-Alert configuration file.
"""
class TelkAlertConfiguration:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def create_configuration(self):
		"""
		Method that creates the Telk-Alert configuration file.
		"""
		try:
			telk_alert_data = []
			total_master_nodes = self.dialog.createInputBoxToNumberDialog("Enter the total number of master nodes:", 8, 50, "1")
			list_form = self.utils.createListToDialogForm(int(total_master_nodes), "IP Address")
			es_host = self.dialog.createFormDialog("Enter the IP addresses of the master nodes:", list_form, 15, 50, "ElasticSearch Hosts", True, option_validate = 1)
			telk_alert_data.append(es_host)
			es_port = self.dialog.createInputBoxToPortDialog("Enter the port to communicate with ElasticSearch:", 9, 50, "9200")
			telk_alert_data.append(es_port)
			alert_rules_folder = self.dialog.createFolderOrFileNameDialog("Enter the folder's name where the alert rules will be stored:", 9, 50, "alert_rules_folder")
			telk_alert_data.append(alert_rules_folder)
			use_ssl_tls = self.dialog.createYesOrNoDialog("\nIs the SSL/TLS protocol required for communication between Telk-Alert and ElasticSearch?", 9, 50, "SSL/TLS Connection")
			if use_ssl_tls == "ok":
				telk_alert_data.append(True)
				verificate_certificate_ssl = self.dialog.createYesOrNoDialog("\nIs SSL certificate verification required?", 7, 50, "Certificate Verification")
				if verificate_certificate_ssl == "ok":
					telk_alert_data.append(True)
					certificate_file_path = self.dialog.createFileDialog("/etc/Telk-Alert-Suite/Telk-Alert/certificates", 8, 50, "Select the CA certificate:", ".pem")
					telk_alert_data.append(certificate_file_path)
				else:
					telk_alert_data.append(False)
			else:
				telk_alert_data.append(False)
			use_authentication_method = self.dialog.createYesOrNoDialog("\nIs an authentication method (HTTP Authentication or API Key) required for communication between Telk-Alert and ElasticSearch?", 10, 50, "Authentication Method")
			if use_authentication_method == "ok":
				telk_alert_data.append(True)
				passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
				option_authentication_method = self.dialog.createRadioListDialog("Select a option:", 9, 55, self.constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
				telk_alert_data.append(option_authentication_method)
				if option_authentication_method == "HTTP Authentication":
					http_authentication_user = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter username:", 8, 50, "user_http"), passphrase)
					telk_alert_data.append(http_authentication_user)
					http_authentication_password = self.utils.encryptDataWithAES(self.dialog.createPasswordBoxDialog("Enter the password:", 8, 50, "password", True), passphrase)
					telk_alert_data.append(http_authentication_password)
				elif option_authentication_method == "API Key":
					api_key_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the API Key ID:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
					telk_alert_data.append(api_key_id)
					api_key = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
					telk_alert_data.append(api_key)
			else:
				telk_alert_data.append(False)
			self.create_yaml_file(telk_alert_data)
			if path.exists(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH):
				self.dialog.createMessageDialog("\nTelk-Alert configuration file created.", 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Telk-Alert configuration file created", 1, "__createConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.createMessageDialog("\nError creating Telk-Alert configuration file. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def update_configuration(self):
		"""
		Method that updates one or more values of the Telk-Alert configuration file.
		"""
		try:
			options_telk_alert_configuration_update = self.dialog.createCheckListDialog("Select one or more options:", 12, 65, self.constants.OPTIONS_TELK_ALERT_CONFIGURATION_UPDATE, "Telk-Alert Configuration Fields")
			telk_alert_data = self.utils.readYamlFile(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)
			file_hash_original = self.utils.getHashFunctionOfFile(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)
			if "Host" in options_telk_alert_configuration_update:
				self.update_es_host(telk_alert_data)
			if "Port" in options_telk_alert_configuration_update:
				self.update_es_port(telk_alert_data)
			if "Folder" in options_telk_alert_configuration_update:
				self.update_alert_rules_folder(telk_alert_data)
			if "SSL/TLS" in options_telk_alert_configuration_update:
				self.update_ssl_tls(telk_alert_data)
			if "Authentication" in options_telk_alert_configuration_update:
				self.update_authentication_method(telk_alert_data)
			self.utils.createYamlFile(telk_alert_data, self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)
			files_hash_new = self.utils.getHashFunctionOfFile(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)
			if file_hash_original == files_hash_new:
				self.dialog.createMessageDialog("\nTelk-Alert configuration file not updated.", 7, 50, "Notification Message")
			else:
				self.dialog.createMessageDialog("\nTelk-Alert configuration file updated.", 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Telk-Alert configuration file updated", 2, "__updateConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.createMessageDialog("\nError updating Telk-Alert configuration file. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def display_configuration(self):
		"""
		Method that displays the current configuration of Telk-Alert.
		"""
		try:
			yaml_file_data = self.utils.convertYamlFileToString(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)
			message_to_display = "\nTelk-Alert Configuration:\n\n" + yaml_file_data
			self.dialog.createScrollBoxDialog(message_to_display, 18, 70, "Telk-Alert Configuration")
		except Exception as exception:
			self.dialog.createMessageDialog("\nError displaying Telk-Alert configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__displayConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def create_yaml_file(self, telk_alert_data):
		"""
		Method that creates the YAML file corresponding to the Telk-Alert configuration file.

		:arg telk_alert_data (list): List with the data that will be stored in the YAML file.
		"""
		telk_alert_data_json = {
			"es_host" : telk_alert_data[0],
			"es_port" : int(telk_alert_data[1]),
			"alert_rules_folder" : telk_alert_data[2],
			"use_ssl_tls" : telk_alert_data[3]
		}

		if telk_alert_data[3]:
			telk_alert_data_json.update({"verificate_certificate_ssl" : telk_alert_data[4]})
			if telk_alert_data[4]:
				last_index = 5
				certificate_file_path = self.constants.CERTIFICATE_FILE_PATH + '/' + path.basename(telk_alert_data[5])
				telk_alert_data_json.update({"certificate_file_path" : certificate_file_path})
				self.utils.copyFile(telk_alert_data[5], self.constants.CERTIFICATE_FILE_PATH)
				self.utils.changeFileFolderOwner(certificate_file_path, self.constants.USER, self.constants.GROUP, "640")
			else:
				last_index = 4
		else:
			last_index = 3
		if telk_alert_data[last_index + 1]:
			telk_alert_data_json.update({"use_authentication_method" : telk_alert_data[last_index + 1]})
			if telk_alert_data[last_index + 2] == "HTTP Authentication":
				telk_alert_data_json.update({"authentication_method" : telk_alert_data[last_index + 2], "http_authentication_user" : telk_alert_data[last_index + 3], "http_authentication_password" : telk_alert_data[last_index + 4]})
			elif telk_alert_data[last_index + 2] == "API Key":
				telk_alert_data_json.update({"authentication_method" : telk_alert_data[last_index + 2], "api_key_id" : telk_alert_data[last_index + 3], "api_key" : telk_alert_data[last_index + 4]})
		
		self.utils.createYamlFile(telk_alert_data_json, self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)
		self.utils.changeFileFolderOwner(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH, self.constants.USER, self.constants.GROUP, "640")
		folder_path = self.constants.TELK_ALERT_PATH + '/' + telk_alert_data[2]
		self.utils.createFolder(folder_path)
		self.utils.changeFileFolderOwner(folder_path, self.constants.USER, self.constants.GROUP, "640")


	def update_es_host(self, telk_alert_data):
		"""
		Method that updates the ElasticSearch hosts.

		Returns the dictionary with the updated configuration file data.

		:arg telk_alert_data (dict): Dictionary with the data stored in the configuration file.
		"""
		option_es_host = self.dialog.createMenuDialog("Select a option:", 10, 50, self.constants.OPTIONS_ES_HOST, "ElasticSearch Host Menu")
		if option_es_host == "1":
			total_master_nodes = self.dialog.createInputBoxToNumberDialog("Enter the total number of master nodes:", 8, 50, "1")
			list_form = self.utils.createListToDialogForm(int(total_master_nodes), "IP Address")
			es_host = self.dialog.createFormDialog("Enter the IP addresses of the master nodes:", list_form, 15, 50, "Add ElasticSearch Hosts", True, option_validate = 1)
			telk_alert_data["es_host"].extend(es_host)
		elif option_es_host == "2":
			list_form = self.utils.convertListToDialogForm(telk_alert_data["es_host"], "IP Address")
			es_host = self.dialog.createFormDialog("Enter the IP addresses of the master nodes:", list_form, 15, 50, "Update ElasticSearch Hosts", True, option_validate = 1)
			telk_alert_data["es_host"] = es_host
		elif option_es_host == "3":
			list_checklist_radiolist = self.utils.convertListToDialogList(telk_alert_data["es_host"], "IP Address")
			options_remove_es_host = self.dialog.createCheckListDialog("Select one or more options:", 15, 50, list_checklist_radiolist, "Remove ElasticSearch Hosts")
			message_to_display = self.utils.getStringFromList(options_remove_es_host, "Selected ElasticSearch Hosts:")
			self.dialog.createScrollBoxDialog(message_to_display, 15, 60, "Remove ElasticSearch Hosts")
			remove_es_host = self.dialog.createYesOrNoDialog("\nAre you sure to remove the selected ElasticSearch Hosts?", 8, 50, "Remove ElasticSearch Hosts")
			if remove_es_host == "ok":
				[telk_alert_data["es_host"].remove(item) for item in options_remove_es_host]
		return telk_alert_data


	def update_es_port(self, telk_alert_data):
		"""
		Method that updates the ElasticSearch port.

		Returns the dictionary with the updated configuration file data.

		:arg telk_alert_data (dict): Dictionary with the data stored in the configuration file.
		"""
		es_port = self.dialog.createInputBoxToPortDialog("Enter the port to communicate with ElasticSearch:", 9, 50, str(telk_alert_data["es_port"]))
		telk_alert_data["es_port"] = int(es_port)
		return telk_alert_data


	def update_alert_rules_folder(self, telk_alert_data):
		"""
		Method that updates the folder where the alert rules are stored.

		Returns the dictionary with the updated configuration file data.

		:arg telk_alert_data (dict): Dictionary with the data stored in the configuration file.
		"""
		alert_rules_folder = self.dialog.createFolderOrFileNameDialog("Enter the folder's name where the alert rules will be stored:", 9, 50, telk_alert_data["alert_rules_folder"])
		if not telk_alert_data["alert_rules_folder"] == alert_rules_folder:
			self.utils.renameFileOrFolder(self.constants.TELK_ALERT_PATH + '/' + telk_alert_data["alert_rules_folder"], self.constants.TELK_ALERT_PATH + '/' + alert_rules_folder)
			telk_alert_data["alert_rules_folder"] = alert_rules_folder
		return telk_alert_data


	def update_ssl_tls(self, telk_alert_data):
		"""
		Method that updates the use of SSL/TLS.

		Returns the dictionary with the updated configuration file data.

		:arg telk_alert_data (dict): Dictionary with the data stored in the configuration file.
		"""
		if telk_alert_data["use_ssl_tls"]:
			option_ssl_tls_true = self.dialog.createRadioListDialog("Select a option:", 9, 70, self.constants.OPTIONS_SSL_TLS_TRUE, "SSL/TLS Connection")
			if option_ssl_tls_true == "Disable":
				del telk_alert_data["verificate_certificate_ssl"]
				if "certificate_file_path" in telk_alert_data:
					del telk_alert_data["certificate_file_path"]
				telk_alert_data["use_ssl_tls"] = False
			elif option_ssl_tls_true == "Certificate Verification":
				if telk_alert_data["verificate_certificate_ssl"]:
					option_verificate_certificate_true = self.dialog.createRadioListDialog("Select a option:", 9, 65, self.constants.OPTIONS_VERIFICATE_CERTIFICATE_TRUE, "Certificate Verification")
					if option_verificate_certificate_true == "Disable":
						if "certificate_file_path" in telk_alert_data:
							del telk_alert_data["certificate_file_path"]
						telk_alert_data["verificate_certificate_ssl"] = False
					elif option_verificate_certificate_true == "Certificate File":
						new_certificate_file_path = self.dialog.createFileDialog(telk_alert_data["certificate_file_path"], 8, 50, "Select the CA certificate:", ".pem")
						certificate_file_path = self.constants.CERTIFICATE_FILE_PATH + '/' + path.basename(certificate_file_path)
						telk_alert_data["certificate_file_path"] = certificate_file_path
						self.utils.copyFile(new_certificate_file_path, self.constants.CERTIFICATE_FILE_PATH)
						self.utils.changeFileFolderOwner(certificate_file_path, self.constants.USER, self.constants.GROUP, "640")
				else:
					option_verificate_certificate_false = self.dialog.createRadioListDialog("Select a option:", 8, 70, self.constants.OPTIONS_VERIFICATE_CERTIFICATE_FALSE, "Certificate Verification")
					if option_verificate_certificate_false == "Enable":
						telk_alert_data["verificate_certificate_ssl"] = True
						new_certificate_file_path = self.dialog.createFileDialog(self.constants.CERTIFICATE_FILE_PATH, 8, 50, "Select the CA certificate:", ".pem")			
						certificate_file_path = self.constants.CERTIFICATE_FILE_PATH + '/' + path.basename(new_certificate_file_path)
						telk_alert_data.update({"certificate_file_path" : certificate_file_path})
						self.utils.copyFile(new_certificate_file_path, self.constants.CERTIFICATE_FILE_PATH)
						self.utils.changeFileFolderOwner(certificate_file_path, self.constants.USER, self.constants.GROUP, "640")
		else:
			option_ssl_tls_false = self.dialog.createRadioListDialog("Select a option:", 8, 70, self.constants.OPTIONS_SSL_TLS_FALSE, "SSL/TLS Connection")
			if option_ssl_tls_false == "Enable":
				telk_alert_data["use_ssl_tls"] = True
				verificate_certificate_ssl = self.dialog.createYesOrNoDialog("\nIs SSL certificate verification required?", 7, 50, "Certificate Verification")
				if verificate_certificate_ssl == "ok":
					new_certificate_file_path = self.dialog.createFileDialog(self.constants.CERTIFICATE_FILE_PATH, 8, 50, "Select the CA certificate:", ".pem")
					certificate_file_path = self.constants.CERTIFICATE_FILE_PATH + '/' + path.basename(new_certificate_file_path)
					telk_alert_data.update({"verificate_certificate_ssl" : True, "certificate_file_path" : certificate_file_path})
					self.utils.copyFile(new_certificate_file_path, self.constants.CERTIFICATE_FILE_PATH)
					self.utils.changeFileFolderOwner(certificate_file_path, self.constants.USER, self.constants.GROUP, "640")
				else:
					telk_alert_data.update({"verificate_certificate_ssl" : False})
		return telk_alert_data


	def update_authentication_method(self, telk_alert_data):
		"""
		Method that updates the use of an authentication method

		Returns the dictionary with the updated configuration file data.

		:arg telk_alert_data (dict): Dictionary with the data stored in the configuration file.
		"""
		if telk_alert_data["use_authentication_method"]:
			option_authentication_true = self.dialog.createRadioListDialog("Select a option:", 9, 55, self.constants.OPTIONS_AUTHENTICATION_TRUE, "Authentication Method")
			if option_authentication_true == "Disable":
				telk_alert_data["use_authentication_method"] = False
				if telk_alert_data["authentication_method"] == "HTTP Authentication":
					del telk_alert_data["http_authentication_user"]
					del telk_alert_data["http_authentication_password"]
				elif telk_alert_data["authentication_method"] == "API Key":
					del telk_alert_data["api_key"]
					del telk_alert_data["api_key_id"]
				del telk_alert_data["authentication_method"]
			elif option_authentication_true == "Method":
				passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
				if telk_alert_data["authentication_method"] == "HTTP Authentication":
					option_authentication_method_update = self.dialog.createRadioListDialog("Select a option:", 9, 55, self.constants.OPTIONS_AUTHENTICATION_METHOD_UPDATE, "HTTP Authentication")
					if option_authentication_method_update == "Disable":
						del telk_alert_data["http_authentication_user"]
						del telk_alert_data["http_authentication_password"]
						telk_alert_data["authentication_method"] = "API Key"
						api_key_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the API Key ID:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
						api_key = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
						telk_alert_data.update({"api_key_id" : api_key_id, "api_key" : api_key})
					elif option_authentication_method_update == "Data":
						options_http_authentication_data = self.dialog.createCheckListDialog("Select one or more options:", 9, 55, self.constants.OPTIONS_HTTP_AUTHENTICATION_DATA, "HTTP Authentication")
						if "Username" in options_http_authentication_data:
							http_authentication_user = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter username:", 8, 50, "user_http"), passphrase)
							telk_alert_data["http_authentication_user"] = http_authentication_user
						if "Password" in options_http_authentication_data:
							http_authentication_password = self.utils.encryptDataWithAES(self.dialog.createPasswordBoxDialog("Enter the password:", 8, 50, "password", True), passphrase)
							telk_alert_data["http_authentication_password"] = http_authentication_password
				elif telk_alert_data["authentication_method"] == "API Key":
					option_authentication_method_update = self.dialog.createRadioListDialog("Select a option:", 9, 55, self.constants.OPTIONS_AUTHENTICATION_METHOD_UPDATE, "API Key")
					if option_authentication_method_update == "Disable":
						del telk_alert_data["api_key_id"]
						del telk_alert_data["api_key"]
						telk_alert_data["authentication_method"] = "HTTP Authentication"
						http_authentication_user = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter username:", 8, 50, "user_http"), passphrase)
						http_authentication_password = self.utils.encryptDataWithAES(self.dialog.createPasswordBoxDialog("Enter the password:", 8, 50, "password", True), passphrase)
						telk_alert_data.update({"http_authentication_user" : http_authentication_user, "http_authentication_password" : http_authentication_password})
					elif option_authentication_method_update == "Data":
						options_api_key_data = self.dialog.createCheckListDialog("Select one or more options:", 9, 55, self.constants.OPTIONS_API_KEY_DATA, "API Key")
						if "ID" in options_api_key_data:
							api_key_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the API Key ID:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
							telk_alert_data["api_key_id"] = api_key_id
						if "API Key" in options_api_key_data:
							api_key = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
							telk_alert_data["api_key"] = api_key
		else:
			option_authentication_false = self.dialog.createRadioListDialog("Select a option:", 8, 55, self.constants.OPTIONS_AUTHENTICATION_FALSE, "Authentication Method")
			if option_authentication_false == "Enable":
				passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
				telk_alert_data["use_authentication_method"] = True
				option_authentication_method = self.dialog.createRadioListDialog("Select a option:", 9, 55, self.constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
				telk_alert_data.update({"authentication_method" : option_authentication_method})
				if option_authentication_method == "HTTP Authentication":
					http_authentication_user = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter username:", 8, 50, "user_http"), passphrase)
					http_authentication_password = self.utils.encryptDataWithAES(self.dialog.createPasswordBoxDialog("Enter the password:", 8, 50, "password", True), passphrase)
					telk_alert_data.update({"http_authentication_user" : http_authentication_user, "http_authentication_password" : http_authentication_password})
				elif option_authentication_method == "API Key":
					api_key_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the API Key ID:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
					api_key = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
					telk_alert_data.update({"api_key_id" : api_key_id, "api_key" : api_key})
		return telk_alert_data