from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related to the configuration of Telk-Alert-Agent.
"""
class AgentConfiguration:
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


	def createAgentConfiguration(self):
		"""
		Method that collects the information for the creation of the Telk-Alert-Agent configuration file.
		"""
		data_agent_configuration = []
		try:
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			time_agent_first_execution = self.__dialog.createTimeDialog("Select the first time of service validation:", 2, 50, -1, -1)
			data_agent_configuration.append(str(time_agent_first_execution[0]) + ':' + str(time_agent_first_execution[1]))
			time_agent_second_execution = self.__dialog.createTimeDialog("Select the second time of service validation:", 2, 50, -1, -1)
			data_agent_configuration.append(str(time_agent_second_execution[0]) + ':' + str(time_agent_second_execution[1]))
			telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			data_agent_configuration.append(telegram_bot_token.decode("utf-8"))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			data_agent_configuration.append(telegram_chat_id.decode("utf-8"))
			self.__createFileYamlAgentConfiguration(data_agent_configuration)
			if path.exists(self.__constants.PATH_FILE_AGENT_CONFIGURATION):
				self.__dialog.createMessageDialog("\nAgent Configuration File Created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Agent Configuration File Created", 1, "__createAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except (OSError, IOError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nError to create Telk-Alert-Agent configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()


	def modifyAgentConfiguration(self):
		"""
		Method that allows to modify one or more values in the Telk-Alert-Agent configuration file.
		"""
		options_fields_agent_update = self.__dialog.createCheckListDialog("Select one or more options:", 12, 60, self.__constants.OPTIONS_FIELDS_AGENT_UPDATE, "Configuration Fields")
		try:
			data_agent_configuration = self.__utils.readYamlFile(self.__constants.PATH_FILE_AGENT_CONFIGURATION)
			hash_file_configuration_original = self.__utils.getHashFunctionToFile(self.__constants.PATH_FILE_AGENT_CONFIGURATION)
			if "First Time" in options_fields_agent_update:
				time_agent_first_execution_actual = data_agent_configuration["time_agent_first_execution"].split(':')
				time_agent_first_execution = self.__dialog.createTimeDialog("Select the first time of service validation:", 2, 50, int(time_agent_first_execution_actual[0]), int(time_agent_first_execution_actual[1]))
				data_agent_configuration["time_agent_first_execution"] = str(time_agent_first_execution[0]) + ':' + str(time_agent_first_execution[1])
			if "Second Time" in options_fields_agent_update:
				time_agent_second_execution_actual = data_agent_configuration["time_agent_second_execution"].split(':')
				time_agent_second_execution = self.__dialog.createTimeDialog("Select the second time of service validation:", 2, 50, int(time_agent_second_execution_actual[0]), int(time_agent_second_execution_actual[1]))
				data_agent_configuration["time_agent_second_execution"] = str(time_agent_second_execution[0]) + ':' + str(time_agent_second_execution[1])
			if "Bot Token" in options_fields_agent_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.__utils.decryptDataWithAES(data_agent_configuration["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
				data_agent_configuration["telegram_bot_token"] = telegram_bot_token.decode("utf-8")
			if "Chat ID" in options_fields_agent_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.__utils.decryptDataWithAES(data_agent_configuration["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
				data_agent_configuration["telegram_chat_id"] = telegram_chat_id.decode("utf-8")
			self.__utils.createYamlFile(data_agent_configuration, self.__constants.PATH_FILE_AGENT_CONFIGURATION)
			hash_file_configuration_new = self.__utils.getHashFunctionToFile(self.__constants.PATH_FILE_AGENT_CONFIGURATION)
			if hash_file_configuration_original == hash_file_configuration_new:
				self.__dialog.createMessageDialog("\nConfiguration file not modified.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nModified configuration file.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Modified configuration file", 2, "__modifyAgentconfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__modifyAgentconfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except (IOError, FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\nError to modify Telk-Alert-Agent configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__modifyAgentconfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG,user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()


	def __createFileYamlAgentConfiguration(self, data_agent_configuration):
		""" 	
		Method that creates the YAML file corresponding to the Telk-Alert-Agent configuration.

		:arg data_agent_configuration: Data to be stored in the configuration file.
		"""
		data_agent_configuration_json = {"time_agent_first_execution": data_agent_configuration[0],
								   		 "time_agent_second_execution": data_agent_configuration[1],
								   		 "telegram_bot_token": data_agent_configuration[2],
								   		 "telegram_chat_id": data_agent_configuration[3]}

		self.__utils.createYamlFile(data_agent_configuration_json, self.__constants.PATH_FILE_AGENT_CONFIGURATION)
		self.__utils.changeOwnerToPath(self.__constants.PATH_FILE_AGENT_CONFIGURATION, self.__constants.USER, self.__constants.GROUP)