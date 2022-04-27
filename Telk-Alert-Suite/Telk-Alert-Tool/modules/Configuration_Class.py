from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

class Configuration:
	__utils = None
	
	__dialog = None

	__constants = None

	__action_to_cancel = None


	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel: Method to be called when the user chooses the cancel option.
		"""
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def createConfiguration(self):
		"""
		Method that collects the information for the creation of the Telk-Alert configuration file.
		"""
		data_configuration = []
		try:
			es_host = self.__dialog.createInputBoxToIPDialog("Enter the ElasticSearch IP address:", 8, 50, "localhost")
			data_configuration.append(es_host)
			es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, "9200")
			data_configuration.append(es_port)
			name_folder_rules = self.__dialog.createFolderOrFileNameDialog("Enter the name of the directory where the alert rules will be saved:", 10, 50, "folder_alert_rules")
			data_configuration.append(name_folder_rules)
			use_ssl_tls = self.__dialog.createYesOrNoDialog("\nDo you require Inv-Alert to communicate with ElasticSearch using the SSL/TLS protocol?", 8, 50, "SSL/TLS Connection")
			if use_ssl_tls == "ok":
				data_configuration.append(True)
				validate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require Inv-Alert to validate the SSL certificate?", 8, 50, "Certificate Validation")
				if validate_certificate_ssl == "ok":
					data_configuration.append(True)
					path_certificate_file = self.__dialog.createFileDialog("/etc", 8, 50, "Select the CA certificate:", ".pem")
					data_configuration.append(path_certificate_file)
				else:
					data_configuration.append(False)
			else:
				data_configuration.append(False)
			use_http_authentication = self.__dialog.createYesOrNoDialog("\nIs the use of HTTP authentication required to connect to ElasticSearch?", 8, 50, "HTTP Authentication")
			if use_http_authentication == "ok":
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				data_configuration.append(True)
				user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
				data_configuration.append(user_http_authentication.decode('utf-8'))
				password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
				data_configuration.append(password_http_authentication.decode('utf-8'))
			else:
				data_configuration.append(False)
			print(data_configuration)
			self.__action_to_cancel()
		except (FileNotFoundError, IOError, OSError) as exception:
			print(exception)
			self.__dialog.createMessageDialog("\nError creating, opening or reading the file. For more information, see the logs.", 8, 50, "Error Message")
			self.__action_to_cancel()
		#self.__createFileYamlConfiguration(data_configuration)
		#if path.exists(self.__constants.PATH_FILE_CONFIGURATION):
		#	self.__logger.createApplicationLog("Configuration file created", 1)
		#	self.__dialog.createMessageDialog("\nConfiguration file created.", 7, 50, "Notification Message")
		#else:
		#	self.__dialog.createMessageDialog("\nError creating configuration file. For more information, see the logs.", 8, 50, "Error Message")
		#self.__action_to_cancel()	
