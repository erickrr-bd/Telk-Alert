from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related to the configuration of Telk-Alert-Report.
"""
class ReportConfiguration:
	"""
	Attribute that stores an object of the libPyUtils class.
	"""
	__utils = None

	"""
	Attribute that stores an object of the libPyDialog class.
	"""
	__dialog = None

	"""
	Attribute that stores an object of the libPyLog class.
	"""
	__logger = None

	"""
	Attribute that stores an object of the Constants class.
	"""
	__constants = None

	"""
	Attribute that stores the method to be called when the user chooses the cancel option.
	"""
	__action_to_cancel = None


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


	def createReportConfiguration(self):
		"""
		Method that collects the information for the creation of the Telk-Alert-Report configuration file.
		"""
		data_report_configuration = []
		try:
			es_host = self.__dialog.createInputBoxToIPDialog("Enter the ElasticSearch IP address:", 8, 50, "localhost")
			data_report_configuration.append(es_host)
			es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, "9200")
			data_report_configuration.append(es_port)
			use_ssl_tls = self.__dialog.createYesOrNoDialog("\nDo you require Inv-Alert to communicate with ElasticSearch using the SSL/TLS protocol?", 8, 50, "SSL/TLS Connection")
			if use_ssl_tls == "ok":
				data_report_configuration.append(True)
				validate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require Telk-Alert-Report to validate the SSL certificate?", 8, 50, "Certificate Validation")
				if validate_certificate_ssl == "ok":
					data_report_configuration.append(True)
					path_certificate_file = self.__dialog.createFileDialog("/etc/Telk-Alert-Suite/Telk-Alert", 8, 50, "Select the CA certificate:", ".pem")
					data_report_configuration.append(path_certificate_file)
				else:
					data_report_configuration.append(False)
			else:
				data_report_configuration.append(False)
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			use_http_authentication = self.__dialog.createYesOrNoDialog("\nIs the use of HTTP authentication required to connect to ElasticSearch?", 8, 50, "HTTP Authentication")
			if use_http_authentication == "ok":
				data_report_configuration.append(True)
				user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
				data_report_configuration.append(user_http_authentication.decode("utf-8"))
				password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
				data_report_configuration.append(password_http_authentication.decode("utf-8"))
			else:
				data_report_configuration.append(False)
			path_alert_rules_folder = self.__dialog.createFolderDialog("/etc/Telk-Alert-Suite/Telk-Alert", 8, 50, "Select the path where the alert rules are located:")
			data_report_configuration.append(path_alert_rules_folder)
			list_all_alert_rules = self.__utils.getListOfAllYamlFilesInFolder(path_alert_rules_folder)
			if list_all_alert_rules:
				exclude_alert_rules = self.__dialog.createYesOrNoDialog("\nIDo you want to exclude one or more alert rules from report generation?", 8, 50, "Exclude Alert Rules")
				if exclude_alert_rules == "ok":
					list_alert_rules_to_exclude = self.__utils.convertListToDialogList(list_all_alert_rules, "Alert Rule")
					alert_rules_to_exclude = self.__dialog.createCheckListDialog("Select one or more options:", 16, 70, list_alert_rules_to_exclude, "Exclude Alert Rules")
					for alert_rule in alert_rules_to_exclude:
						list_all_alert_rules.remove(alert_rule)
			data_report_configuration.append(list_all_alert_rules)
			time_report_execution = self.__dialog.createTimeDialog("Select the time to get the report:", 2, 50, -1, -1)
			data_report_configuration.append(str(time_report_execution[0]) + ':' + str(time_report_execution[1]))
			telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			data_report_configuration.append(telegram_bot_token.decode("utf-8"))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			data_report_configuration.append(telegram_chat_id.decode("utf-8"))
			self.__createYamlFileReportConfiguration(data_report_configuration)
			if path.exists(self.__constants.PATH_FILE_REPORT_CONFIGURATION):
				self.__dialog.createMessageDialog("\nReport Configuration File Created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Report Configuration File Created", 1, "__createReportConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except (OSError, IOError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nError to create Telk-Alert-Report configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createReportConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()


	def modifyReportConfiguration(self):
		"""
		Method that allows to modify one or more values in the Telk-Alert-Report configuration file.
		"""
		options_fields_report_update = self.__dialog.createCheckListDialog("Select one or more options:", 10, 60, self.__constants.OPTIONS_FIELDS_REPORT_UPDATE, "Configuration Fields")
		try:
			data_report_configuration = self.__utils.readYamlFile(self.__constants.PATH_FILE_REPORT_CONFIGURATION)
			hash_file_configuration_original = self.__utils.getHashFunctionToFile(self.__constants.PATH_FILE_REPORT_CONFIGURATION)
			if "Execution Time" in options_fields_report_update:
				time_report_execution_actual = data_report_configuration["time_report_execution"].split(':')
				time_report_execution = self.__dialog.createTimeDialog("Select the time to get the report:", 2, 50, int(time_report_execution_actual[0]), int(time_report_execution_actual[1]))
				data_report_configuration["time_report_execution"] = str(time_report_execution[0]) + ':' + str(time_report_execution[1])
			if "Bot Token" in options_fields_report_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.__utils.decryptDataWithAES(data_report_configuration["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
				data_report_configuration["telegram_bot_token"] = telegram_bot_token.decode("utf-8")
			if "Chat ID" in options_fields_report_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.__utils.decryptDataWithAES(data_report_configuration["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
				data_report_configuration["telegram_chat_id"] = telegram_chat_id.decode("utf-8")
			self.__utils.createYamlFile(data_report_configuration, self.__constants.PATH_FILE_REPORT_CONFIGURATION)
			hash_file_configuration_new = self.__utils.getHashFunctionToFile(self.__constants.PATH_FILE_REPORT_CONFIGURATION)
			if hash_file_configuration_original == hash_file_configuration_new:
				self.__dialog.createMessageDialog("\nConfiguration file not modified.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nModified configuration file.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Modified configuration file", 2, "__modifyReportconfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__modifyReportconfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except (IOError, FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\nError to modify Telk-Alert-Report configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__modifyReportconfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG,user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()


	def __createYamlFileReportConfiguration(self, data_report_configuration):
		""" 	
		Method that creates the YAML file corresponding to the Telk-Alert-Report configuration.

		:arg data_report_configuration: Data to be stored in the configuration file.
		"""
		data_report_configuration_json = {"es_host" : data_report_configuration[0],
								   		  "es_port" : int(data_report_configuration[1]),
								   		  "use_ssl_tls" : data_report_configuration[2]}
		
		if data_report_configuration[2] == True:
			if data_report_configuration[3] == True:
				validate_certificate_ssl_json = {"validate_certificate_ssl" : data_report_configuration[3] , "path_certificate_file" : data_report_configuration[4]}
				last_index = 4
			else:
				validate_certificate_ssl_json = {"validate_certificate_ssl" : data_report_configuration[3]}
				last_index = 3
			data_report_configuration_json.update(validate_certificate_ssl_json)
		else:
			last_index = 2
		if data_report_configuration[last_index + 1] == True:
			http_authentication_json = {"use_http_authentication" : data_report_configuration[last_index + 1], "user_http_authentication" : data_report_configuration[last_index + 2], "password_http_authentication" : data_report_configuration[last_index + 3]}
			last_index += 3
		else:
			http_authentication_json = {"use_http_authentication" : data_report_configuration[last_index + 1]}
			last_index += 1
		data_report_configuration_json.update(http_authentication_json)
		aux_data_json = {"path_alert_rules_folder" : data_report_configuration[last_index + 1], "list_all_alert_rules" : data_report_configuration[last_index + 2], "time_report_execution" : data_report_configuration[last_index + 3], "telegram_bot_token" : data_report_configuration[last_index + 4], "telegram_chat_id" : data_report_configuration[last_index + 5]}
		data_report_configuration_json.update(aux_data_json)

		self.__utils.createYamlFile(data_report_configuration_json, self.__constants.PATH_FILE_REPORT_CONFIGURATION)
		self.__utils.changeOwnerToPath(self.__constants.PATH_FILE_REPORT_CONFIGURATION, self.__constants.USER, self.__constants.GROUP)