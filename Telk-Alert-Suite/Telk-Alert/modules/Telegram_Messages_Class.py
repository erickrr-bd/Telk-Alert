from time import strftime
from libPyElk import libPyElk
from libPyLog import libPyLog
from .Constants_Class import Constants

class TelegramMessages:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.elasticsearch = libPyElk()


	def multiple_alert_rule_message(self, result, alert_rule_data):
		"""
		"""
		telegram_message = u'\u26A0\uFE0F' + ' ' + alert_rule_data["alert_rule_name"] +  ' ' + u'\u26A0\uFE0F' + "\n\n" + u'\U0001f6a6' +  " Alert level: " + alert_rule_data["alert_rule_level"] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
		telegram_message += "At least " + str(alert_rule_data["total_number_events"]) + " event(s) were found." + "\n\nFOUND EVENT:\n\n"
		for hit in result:
			telegram_message += telegram_message + self.elasticsearch.generateDataTelegramMessage(hit)
		return telegram_message


	def only_alert_rule_message(self, result, alert_rule_data):
		telegram_message = u'\u26A0\uFE0F' + ' ' + alert_rule_data["alert_rule_name"] +  ' ' + u'\u26A0\uFE0F' + "\n\n" + u'\U0001f6a6' +  " Alert level: " + alert_rule_data["alert_rule_level"] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
		telegram_message += "At least " + str(alert_rule_data["total_number_events"]) + " event(s) were found." + "\n\nFOUND EVENT:\n\n"
		for hit in result:
			telegram_message += telegram_message + self.elasticsearch.generateDataTelegramMessage(hit)
			break
		telegram_message += "TOTAL EVENTS FOUND: " + str(len(result))
		return telegram_message


	def create_log_by_telegram_code(self, response_http_code, alert_rule_name):
		if response_http_code == 200:
			self.logger.generateApplicationLog("Telegram message sent", 1, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		elif response_http_code == 400:
			self.logger.generateApplicationLog()


	def __createLogByTelegramCode(self, response_status_code, alert_rule_name):
		if response_status_code == 200:
			self.__logger.generateApplicationLog("Telegram message sent.", 1, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_status_code == 400:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Bad request.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_status_code == 401:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Unauthorized.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_status_code == 404:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Not found.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)