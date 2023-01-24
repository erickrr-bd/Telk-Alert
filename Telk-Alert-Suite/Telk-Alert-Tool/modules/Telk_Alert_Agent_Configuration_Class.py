from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related to the configuration of Telk-Alert-Agent.
"""
class TelkAlertAgentConfiguration:

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
		Method that collects the information for the creation of the Telk-Alert-Agent configuration file.
		"""
		telk_alert_agent_data = []
		try:
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			first_execution = self.__dialog.createTimeDialog("Select the first time of service validation:", 2, 50, -1, -1)
			telk_alert_agent_data.append(str(first_execution[0]) + ':' + str(first_execution[1]))
			second_execution = self.__dialog.createTimeDialog("Select the second time of service validation:", 2, 50, -1, -1)
			telk_alert_agent_data.append(str(second_execution[0]) + ':' + str(second_execution[1]))
			telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			telk_alert_agent_data.append(telegram_bot_token.decode("utf-8"))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			telk_alert_agent_data.append(telegram_chat_id.decode("utf-8"))
			self.__createYamlFileConfiguration(telk_alert_agent_data)
			if path.exists(self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE):
				self.__dialog.createMessageDialog("\nTelk-Alert-Agent Configuration File Created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Telk-Alert-Agent Configuration File Created", 1, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nValue Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def modifyConfiguration(self):
		"""
		Method that allows to modify one or more values in the Telk-Alert-Agent configuration file.
		"""
		options_configuration_telk_alert_agent_update = self.__dialog.createCheckListDialog("Select one or more options:", 11, 65, self.__constants.OPTIONS_CONFIGURATION_TELK_ALERT_AGENT_UPDATE, "Telk-Alert-Agent Configuration Fields")
		try:
			telk_alert_agent_data = self.__utils.readYamlFile(self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE)
			hash_file_configuration_original = self.__utils.getHashFunctionToFile(self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE)
			if "First Execution" in options_configuration_telk_alert_agent_update:
				first_execution_actual = telk_alert_agent_data["first_execution"].split(':')
				first_execution = self.__dialog.createTimeDialog("Select the first time of service validation:", 2, 50, int(first_execution_actual[0]), int(first_execution_actual[1]))
				telk_alert_agent_data["first_execution"] = str(first_execution[0]) + ':' + str(first_execution[1])
			if "Second Execution" in options_configuration_telk_alert_agent_update:
				second_execution_actual = telk_alert_agent_data["second_execution"].split(':')
				second_execution = self.__dialog.createTimeDialog("Select the second time of service validation:", 2, 50, int(second_execution_actual[0]), int(second_execution_actual[1]))
				telk_alert_agent_data["second_execution"] = str(second_execution[0]) + ':' + str(second_execution[1])
			if "Bot Token" in options_configuration_telk_alert_agent_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.__utils.decryptDataWithAES(telk_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
				telk_alert_agent_data["telegram_bot_token"] = telegram_bot_token.decode("utf-8")
			if "Chat ID" in options_configuration_telk_alert_agent_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.__utils.decryptDataWithAES(telk_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
				telk_alert_agent_data["telegram_chat_id"] = telegram_chat_id.decode("utf-8")
			self.__utils.createYamlFile(telk_alert_agent_data, self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE)
			hash_file_configuration_new = self.__utils.getHashFunctionToFile(self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE)
			if hash_file_configuration_original == hash_file_configuration_new:
				self.__dialog.createMessageDialog("\nTelk-ALert-Agent configuration file not modified.", 8, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nTelk-ALert-Agent configuration file modified.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Telk-ALert-Agent configuration file modified", 2, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nValue Error. For more information, see the logs.", 7, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG,user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def showConfigurationData(self):
		"""
		Method that displays the data stored in the Telk-Alert-Agent configuration file.
		"""
		try:
			telk_alert_agent_data = self.__utils.convertDataYamlFileToString(self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE)
			message_to_display = "\nTelk-Alert-Agent Configuration:\n\n" + telk_alert_agent_data
			self.__dialog.createScrollBoxDialog(message_to_display, 12, 70, "Telk-Alert-Agent Configuration")
		except (FileNotFoundError, OSError) as exception:
			self.__dialog.createMessageDialog("\nFile Not Found or OS Error. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__showConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def __createYamlFileConfiguration(self, telk_alert_agent_data):
		""" 	
		Method that creates the YAML file corresponding to the Telk-Alert-Agent configuration.

		:arg telk_alert_agent_data: Data to be stored in the configuration file.
		"""
		telk_alert_agent_data_json = {
			"first_execution": telk_alert_agent_data[0],
			"second_execution": telk_alert_agent_data[1],
			"telegram_bot_token": telk_alert_agent_data[2],
			"telegram_chat_id": telk_alert_agent_data[3]
		}

		self.__utils.createYamlFile(telk_alert_agent_data_json, self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE)
		self.__utils.changeOwnerToPath(self.__constants.PATH_TELK_ALERT_AGENT_CONFIGURATION_FILE, self.__constants.USER, self.__constants.GROUP)