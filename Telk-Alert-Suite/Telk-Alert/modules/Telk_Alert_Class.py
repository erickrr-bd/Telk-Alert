from os import path
from threading import Thread
from libPyElk import libPyElk
from libPyLog import libPyLog
from time import sleep, strftime
from libPyUtils import libPyUtils
from libPyTelegram import libPyTelegram
from .Constants_Class import Constants

class TelkAlert:

	__utils = None

	__logger = None

	__telegram = None

	__constants = None

	__elasticsearch = None


	def __init__(self):
		"""
		Method that corresponds to the constructor of the class.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__elasticsearch = libPyElk()
		self.__telegram = libPyTelegram()


	def startTelkAlert(self):
		"""
		Method that starts the Telk-Alert application
		"""
		try:
			if path.exists(self.__constants.PATH_FILE_CONFIGURATION):
				data_configuration = self.__utils.readYamlFile(self.__constants.PATH_FILE_CONFIGURATION)
				if data_configuration["use_http_authentication"] == True:
					conn_es = self.__elasticsearch.createConnectionToElasticSearch(data_configuration, path_key_file = self.__constants.PATH_KEY_FILE)
				else:
					conn_es = self.__elasticsearch.createConnectionToElasticSearch(data_configuration)
				if not conn_es == None:
					self.__logger.generateApplicationLog("Telk-Alert v3.2", 1, "__start", use_stream_handler = True)
					self.__logger.generateApplicationLog("@2022 Tekium. All rights reserved.", 1, "__start", use_stream_handler = True)
					self.__logger.generateApplicationLog("Author: Erick Rodriguez", 1, "__start", use_stream_handler = True)
					self.__logger.generateApplicationLog("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com", 1, "__start", use_stream_handler = True)
					self.__logger.generateApplicationLog("License: GPLv3", 1, "__start", use_stream_handler = True)
					self.__logger.generateApplicationLog("Telk-Alert started", 1, "__start", use_stream_handler = True)
					self.__logger.generateApplicationLog("Established connection with: " + data_configuration['es_host'] + ':' + str(data_configuration['es_port']), 1, "__start" , use_stream_handler = True)
					self.__logger.generateApplicationLog("Elasticsearch Cluster Name: " + conn_es.info()["cluster_name"], 1, "__start", use_stream_handler = True)
					self.__logger.generateApplicationLog("Elasticsearch Version: " + conn_es.info()["version"]["number"], 1, "__start", use_stream_handler = True)
					path_alert_rules_folder = self.__constants.PATH_BASE_TELK_ALERT + '/' + data_configuration["name_folder_rules"]
					list_all_alert_rules = self.__utils.getListOfAllYamlFilesInFolder(path_alert_rules_folder)
					if list_all_alert_rules:
						self.__logger.generateApplicationLog(str(len(list_all_alert_rules)) + " alert rules in: " + path_alert_rules_folder, 1, "__start", use_stream_handler = True)
						for alert_rule in list_all_alert_rules:
							self.__logger.generateApplicationLog(alert_rule[:-5] + " loaded", 1, "__start", use_stream_handler = True)
							data_alert_rule = self.__utils.readYamlFile(path_alert_rules_folder + '/' + alert_rule)
							Thread(name = alert_rule[:-5],target = self.__startAlertRule, args = (conn_es, data_alert_rule, )).start()
					else:
						self.__logger.generateApplicationLog("No alert rules found in: " + path_alert_rules_folder, 1, "__start", use_stream_handler = True)
			else:
				self.__logger.generateApplicationLog("Configuration file not found", 3, "Configuration", use_stream_handler = True)
		except KeyError  as exception:
			print("Error 2")
		except (OSError, IOError, FileNotFoundError) as exception:
			print("Error")
		except (self.__elasticsearch.exceptions.AuthenticationException, self.__elasticsearch.exceptions.ConnectionError, self.__elasticsearch.exceptions.AuthorizationException, self.__elasticsearch.exceptions.RequestError) as exception:
			self.__logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			self.__logger.generateApplicationLog("Error connecting with ElasticSearch. For more information, see the logs.", 3, "__connection", use_stream_handler = True)


	def __startAlertRule(self, conn_es, data_alert_rule):
		"""
		"""
		try:
			for unit_time in data_alert_rule["time_search"]:
				time_search_in_seconds = self.__utils.convertTimeToSeconds(unit_time, data_alert_rule["time_search"][unit_time])
			for unit_time in data_alert_rule["time_range"]:
				date_math_time_range = self.__utils.convertTimeToDateMath(unit_time, data_alert_rule["time_range"][unit_time])
			search_in_elastic = self.__elasticsearch.createSearchQueryStringElasticSearch(conn_es, data_alert_rule["index_pattern_name"], data_alert_rule["query_type"][0]["query_string"]["query"])
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			telegram_bot_token = self.__utils.decryptDataWithAES(data_alert_rule["telegram_bot_token"], passphrase).decode("utf-8")
			telegram_chat_id = self.__utils.decryptDataWithAES(data_alert_rule["telegram_chat_id"], passphrase).decode("utf-8")
			while True:
				if not data_alert_rule["use_custom_rule_option"] == True:
					result_search = self.__elasticsearch.executeSearchQueryStringElasticSearch(search_in_elastic, date_math_time_range, "now/m", data_alert_rule["use_fields_option"], fields = data_alert_rule["fields_name"])
					if result_search:
						if len(result_search) >= data_alert_rule["number_events_found_by_alert"]:
							self.__logger.generateApplicationLog("Events found: " + str(len(result_search)), 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True)
							if data_alert_rule["send_type_alert_rule"] == "multiple":
								self.__sendMultipleAlertRule(result_search, data_alert_rule, telegram_bot_token, telegram_chat_id)
							if data_alert_rule["send_type_alert_rule"] == "only":
								self.__sendOnlyAlertRule(result_search, data_alert_rule, telegram_bot_token, telegram_chat_id, len(result_search))
					else:
						self.__logger.generateApplicationLog("No events found", 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True)
				sleep(time_search_in_seconds)
		except KeyError as exception:
			print("Error")

	def __sendMultipleAlertRule(self, result_search, data_alert_rule, telegram_bot_token, telegram_chat_id):
		try:
			for hit in result_search:
				message_header = u'\u26A0\uFE0F' + " " + data_alert_rule["alert_rule_name"] +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\U0001f6a6' +  " Alert level: " + data_alert_rule["alert_rule_level"] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
				message_header += "At least " + str(data_alert_rule["number_events_found_by_alert"]) + " event(s) were found." + "\n\n"
				message_to_send = message_header + self.__elasticsearch.generateTelegramMessagewithElasticData(hit)
				response_status_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_to_send)
				self.__createLogByTelegramCode(response_status_code, data_alert_rule["alert_rule_name"])
		except KeyError as exception:
			print("KeyError")

	def __sendOnlyAlertRule(self, result_search, data_alert_rule, telegram_bot_token, telegram_chat_id, total_events):
		try:
			message_header = u'\u26A0\uFE0F' + " " + data_alert_rule["alert_rule_name"] +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\U0001f6a6' +  " Alert level: " + data_alert_rule["alert_rule_level"] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
			message_header += "At least " + str(data_alert_rule["number_events_found_by_alert"]) + " event(s) were found." + "\n\n"
			for hit in result_search:
				message_to_send = message_header + self.__elasticsearch.generateTelegramMessagewithElasticData(hit)
				break
			message_to_send += "TOTAL EVENTS FOUND: " + str(total_events)
			response_status_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_to_send)
			self.__createLogByTelegramCode(response_status_code, data_alert_rule["alert_rule_name"])
		except KeyError as exception:
			print("Error")


	def __createLogByTelegramCode(self, response_status_code, alert_rule_name):
		"""
		Method that creates a log based on the HTTP code received as a response.

		:arg response_http_code: HTTP code received in the response when sending the alert to Telegram.
		"""
		if response_status_code == 200:
			self.__logger.generateApplicationLog("Telegram message sent.", 1, "__" + alert_rule_name, use_stream_handler = True)
		elif response_status_code == 400:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Bad request.", 3, "__" + alert_rule_name, use_stream_handler = True)
		elif response_status_code == 401:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Unauthorized.", 3, "__" + alert_rule_name, use_stream_handler = True)
		elif response_status_code == 404:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Not found.", 3, "__" + alert_rule_name, use_stream_handler = True)