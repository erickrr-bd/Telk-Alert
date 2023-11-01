from time import strftime
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


	def generate_telegram_message(self, telk_alert_service_status):
		"""
		Method that generates a text message based on the status of the Telk-Alert service

		Return the text message.

		:arg telk_alert_service_status (string): Telk-Alert service status.
		"""
		telegram_message = "" + u'\u26A0\uFE0F' + " Telk-Alert Service " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + "Service Status Validation Time: " + strftime("%c") + "\n\n\n"
		telegram_message += "Telk-Alert Service Status: " + u'\U0001f534' + "\n\n"
		telegram_message += "" + u'\U0001f4cb' + " Note: The red circle indicates that Telk-Alert service isn't working. Report to an administrator.\n\n"
		return telegram_message


	def generate_telegram_message_threads(self, threads_number, total_alert_rules):
		"""
		Method that generates a text message based on the total number of alert rules working.

		Return the text message.

		:arg threads_number (integer): Number of threads working on Telk-Alert.
		:arg total_alert_rules (integer): Number of Telk-Alert alert rules.
		"""
		telegram_message = "" + u'\u26A0\uFE0F' + " Telk-Alert Service " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + "Service Status Validation Time: " + strftime("%c") + "\n\n\n"
		telegram_message += "" + u'\U0001f4cb' + " The Telk-Alert service has restarted because there are " + str(threads_number) + '/' + str(total_alert_rules) + " alert rules running.\n\n"
		return telegram_message


	def create_log_by_telegram_code(self, response_http_code):
		"""
		Method that generates a log based on an HTTP response code.

		:arg response_http_code (integer): HTTP code of the response. 
		"""
		if response_http_code == 200:
			self.logger.generateApplicationLog("Telegram message sent", 1, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		elif response_http_code == 400:
			self.logger.generateApplicationLog("Telegram message not sent. Bad request.", 3, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		elif response_http_code == 401:
			self.logger.generateApplicationLog("Telegram message not sent. Unauthorized.", 3, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		elif response_http_code == 404:
			self.logger.generateApplicationLog("Telegram message not sent. Not found.", 3, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)