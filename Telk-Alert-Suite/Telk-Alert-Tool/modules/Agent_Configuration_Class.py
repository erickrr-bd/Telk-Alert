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
			data_agent_configuration.append(telegram_bot_token.decode('utf-8'))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			data_agent_configuration.append(telegram_chat_id.decode('utf-8'))
			self.__createFileYamlAgentConfiguration(data_agent_configuration)
			if path.exists(self.__constants.PATH_FILE_AGENT_CONFIGURATION):
				self.__dialog.createMessageDialog("\nAgent Configuration File Created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Agent Configuration File Created", 1, "__createAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()
		except (OSError, IOError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nError to create Telk-Alert-Agent configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__action_to_cancel()


	def __createFileYamlAgentConfiguration(self, data_agent_configuration):
		""" 	
		Method that creates the YAML file corresponding to the Telk-Alert-Agent configuration.

		:arg data_agent_configuration: Data to be stored in the configuration file.
		"""
		data_agent_configuration_json = {'time_agent_first_execution': data_agent_configuration[0],
								   		 'time_agent_second_execution': data_agent_configuration[1],
								   		 'telegram_bot_token': data_agent_configuration[2],
								   		 'telegram_chat_id': data_agent_configuration[3]}

		self.__utils.createYamlFile(data_agent_configuration_json, self.__constants.PATH_FILE_AGENT_CONFIGURATION)
		self.__utils.changeOwnerToPath(self.__constants.PATH_FILE_AGENT_CONFIGURATION, self.__constants.USER, self.__constants.GROUP)