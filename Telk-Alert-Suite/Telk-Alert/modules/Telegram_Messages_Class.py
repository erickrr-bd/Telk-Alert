from time import strftime
from libPyElk import libPyElk
from libPyLog import libPyLog
from .Constants_Class import Constants

"""
Class that manages messages sent via Telegram.
"""
class TelegramMessages:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.constants = Constants()
		self.elasticsearch = libPyElk()


	def generate_telegram_message(self, hit, alert_rule_data):
		"""
		Method that generates a text message based on an event found during a search in ElasticSearch.

		Return the text message.

		:arg hit (dict): Dictionary with the data of the event found during the search.
		:arg alert_rule_data (dict): Dictionary with the alert rule data.
		"""
		telegram_message = u'\u26A0\uFE0F' + ' ' + alert_rule_data["alert_rule_name"] +  ' ' + u'\u26A0\uFE0F' + "\n\n" + u'\U0001f6a6' +  " Alert level: " + alert_rule_data["alert_rule_level"] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
		telegram_message += "At least " + str(alert_rule_data["total_number_events"]) + " event(s) were found." + "\n\nFOUND EVENT:\n\n"
		telegram_message += self.elasticsearch.generateDataTelegramMessage(hit)
		return telegram_message


	def create_log_by_telegram_code(self, response_http_code, alert_rule_name):
		"""
		Method that generates a log based on an HTTP response code.

		:arg response_http_code (integer): HTTP code of the response. 
		:arg alert_rule_name (string): Name of the alert rule.
		"""
		if response_http_code == 200:
			self.logger.generateApplicationLog("Telegram message sent", 1, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		elif response_http_code == 400:
			self.logger.generateApplicationLog("Telegram message not sent. Bad request.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		elif response_http_code == 401:
			self.logger.generateApplicationLog("Telegram message not sent. Unauthorized.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		elif response_http_code == 404:
			self.logger.generateApplicationLog("Telegram message not sent. Not found.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)