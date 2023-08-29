from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages the Telk-Alert-Agent configuration file.
"""
class TelkAlertAgentConfiguration:

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
		Method that creates the Telk-Alert-Agent configuration file.
		"""
		try:
			telk_alert_agent_data = []
			passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
			option_unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
			telk_alert_agent_data.append(option_unit_time)
			unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + option_unit_time + " of how often the service status will be validated:", 9, 50, "1")
			telk_alert_agent_data.append(unit_time_total)
			telegram_bot_token = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			telk_alert_agent_data.append(telegram_bot_token)
			telegram_chat_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			telk_alert_agent_data.append(telegram_chat_id)
			self.create_yaml_file(telk_alert_agent_data)
			if path.exists(self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH):
				self.dialog.createMessageDialog("\nTelk-Alert-Agent configuration file created.", 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Telk-Alert-Agent configuration file created", 1, "__createConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except (OSError, FileNotFoundError) as exception:
			self.dialog.createMessageDialog("\nError creating Telk-Alert-Agent configuration file. For more information, see the logs.")
			self.logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def update_configuration(self):
		"""
		Method that updates one or more values of the Telk-Alert-Agent configuration file.
		"""
		try:
			options_telk_alert_agent_configuration_update = self.dialog.createCheckListDialog("Select one or more options:", 10, 55, self.constants.OPTIONS_TELK_ALERT_AGENT_CONFIGURATION_UPDATE, "Telk-Alert-Agent Configuration Fields")
			telk_alert_agent_data = self.utils.readYamlFile(self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH)
			file_hash_original = self.utils.getHashFunctionOfFile(self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH)
			if "Time" in options_telk_alert_agent_configuration_update:
				self.update_time(telk_alert_agent_data)
			if "Bot Token" in options_telk_alert_agent_configuration_update:
				self.update_telegram_bot_token(telk_alert_agent_data)
			if "Chat ID" in options_telk_alert_agent_configuration_update:
				self.update_telegram_chat_id(telk_alert_agent_data)
			self.utils.createYamlFile(telk_alert_agent_data, self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH)
			files_hash_new = self.utils.getHashFunctionOfFile(self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH)
			if file_hash_original == files_hash_new:
				self.dialog.createMessageDialog("\nTelk-Alert-Agent configuration file not updated.", 7, 50, "Notification Message")
			else:
				self.dialog.createMessageDialog("\nTelk-Alert-Agent configuration file updated.", 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Telk-Alert-Agent configuration file updated", 2, "__updateConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except (KeyError, OSError) as exception:
			self.dialog.createMessageDialog("\nError updating Telk-Alert-Agent configuration file. For more information, see the logs.")
			self.logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def display_configuration(self):
		"""
		Method that shows the current configuration of Telk-Alert-Agent.
		"""
		try:
			yaml_file_data = self.utils.convertYamlFileToString(self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH)
			message_to_display = "\nTelk-Alert-Agent Configuration:\n\n" + yaml_file_data
			self.dialog.createScrollBoxDialog(message_to_display, 18, 70, "Telk-Alert-Agent Configuration")
		except (OSError, FileNotFoundError) as exception:
			self.dialog.createMessageDialog("\nError displaying Telk-Alert-Agent configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__displayConfiguration", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def create_yaml_file(self, telk_alert_agent_data):
		"""
		Method that creates the YAML file corresponding to the Telk-Alert-Agent configuration file.

		:arg telk_alert_agent_data (list): List with the data that will be stored in the YAML file.
		"""
		telk_alert_agent_data_json = {
			"service_validation_time" : {telk_alert_agent_data[0] : int(telk_alert_agent_data[1])},
			"telegram_bot_token" : telk_alert_agent_data[2],
			"telegram_chat_id" : telk_alert_agent_data[3]
		}

		self.utils.createYamlFile(telk_alert_agent_data_json, self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH)
		self.utils.changeFileFolderOwner(self.constants.TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH, self.constants.USER, self.constants.GROUP, "640")


	def update_time(self, telk_alert_agent_data):
		"""
		Method that updates the time when the Telk-Alert service will be validated.

		Returns the dictionary with the updated configuration file data.

		:arg telk_alert_agent_data (dict): Dictionary with the data stored in the configuration file.
		"""
		current_unit_time = list(telk_alert_agent_data["service_validation_time"].keys())[0]
		for item in self.constants.OPTIONS_UNIT_TIME:
			if item[0] == current_unit_time:
				item[2] = 1
			else:
				item[2] = 0
		option_unit_time = self.dialog.createRadioListDialog("Select a option:", 10, 50, self.constants.OPTIONS_UNIT_TIME, "Unit Time")
		unit_time_total = self.dialog.createInputBoxToNumberDialog("Enter the total in " + option_unit_time + " of how often the service status will be validated:", 9, 50, str(telk_alert_agent_data["service_validation_time"][current_unit_time]))
		telk_alert_agent_data["service_validation_time"] = {option_unit_time : int(unit_time_total)}
		return telk_alert_agent_data


	def update_telegram_bot_token(self, telk_alert_agent_data):
		"""
		Method that updates the Telegram Bot Token.

		Returns the dictionary with the updated configuration file data.

		:arg telk_alert_agent_data (dict): Dictionary with the data stored in the configuration file.
		"""
		passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
		telegram_bot_token = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.utils.decryptDataWithAES(telk_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
		telk_alert_agent_data["telegram_bot_token"] = telegram_bot_token
		return telk_alert_agent_data


	def update_telegram_chat_id(self, telk_alert_agent_data):
		"""
		Method that updates the Telegram chat ID.

		Returns the dictionary with the updated configuration file data.

		:arg telk_alert_agent_data (dict): Dictionary with the data stored in the configuration file.
		"""
		passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
		telegram_chat_id = self.utils.encryptDataWithAES(self.dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.utils.decryptDataWithAES(telk_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
		telk_alert_agent_data["telegram_chat_id"] = telegram_chat_id
		return telk_alert_agent_data