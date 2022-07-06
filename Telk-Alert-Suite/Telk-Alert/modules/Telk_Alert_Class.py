from sys import exit
from threading import Thread
from libPyElk import libPyElk
from libPyLog import libPyLog
from time import sleep, strftime
from libPyUtils import libPyUtils
from libPyTelegram import libPyTelegram
from .Constants_Class import Constants

"""
Class that manages the operation of Telk-Alert.
"""
class TelkAlert:
	"""
	Attribute that stores an object of the libPyUtils class.
	"""
	__utils = None

	"""
	Attribute that stores an object of the libPyLog class.
	"""
	__logger = None

	"""
	Attribute that stores an object of the libPyTelegram class.
	"""
	__telegram = None

	"""
	Attribute that stores an object of the Constants class.
	"""
	__constants = None

	"""
	Attribute that stores an object of the libPyElk class.
	"""
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
		Method that starts the Telk-Alert application.
		"""
		try:
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
				self.__logger.generateApplicationLog("Established connection with: " + data_configuration['es_host'] + ':' + str(data_configuration['es_port']), 1, "__connection" , use_stream_handler = True)
				self.__logger.generateApplicationLog("Elasticsearch Cluster Name: " + conn_es.info()["cluster_name"], 1, "__connection", use_stream_handler = True)
				self.__logger.generateApplicationLog("Elasticsearch Version: " + conn_es.info()["version"]["number"], 1, "__connection", use_stream_handler = True)
				path_alert_rules_folder = self.__constants.PATH_BASE_TELK_ALERT + '/' + data_configuration["name_folder_rules"]
				list_all_alert_rules = self.__utils.getListOfAllYamlFilesInFolder(path_alert_rules_folder)
				if list_all_alert_rules:
					self.__logger.generateApplicationLog(str(len(list_all_alert_rules)) + " alert rules in: " + path_alert_rules_folder, 1, "__readAlertRules", use_stream_handler = True)
					for alert_rule in list_all_alert_rules:
						self.__logger.generateApplicationLog(alert_rule[:-5] + " loaded", 1, "__alertRule", use_stream_handler = True)
						data_alert_rule = self.__utils.readYamlFile(path_alert_rules_folder + '/' + alert_rule)
						Thread(name = alert_rule[:-5], target = self.__startAlertRule, args = (conn_es, data_alert_rule, )).start()
				else:
					self.__logger.generateApplicationLog("No alert rules found in: " + path_alert_rules_folder, 1, "__readAlertRules", use_stream_handler = True)
		except KeyError  as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__start", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)
		except (OSError, IOError, FileNotFoundError) as exception:
			self.__logger.generateApplicationLog("Error to found, open or read a file or directory. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)
		except (self.__elasticsearch.exceptions.AuthenticationException, self.__elasticsearch.exceptions.ConnectionError, self.__elasticsearch.exceptions.AuthorizationException, self.__elasticsearch.exceptions.RequestError, self.__elasticsearch.exceptions.ConnectionTimeout) as exception:
			self.__logger.generateApplicationLog("Error connecting with ElasticSearch. For more information, see the logs.", 3, "__connection", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__connection", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)


	def __startAlertRule(self, conn_es, data_alert_rule):
		"""
		Method that starts the alert rule's search

		:arg conn_es: Object that contains a connection to ElasticSearch.
		:arg data_alert_rule: bject that contains the data of the alert rule.
		"""
		try:
			for unit_time in data_alert_rule["time_search"]:
				time_search_in_seconds = self.__utils.convertTimeToSeconds(unit_time, data_alert_rule["time_search"][unit_time])
			for unit_time in data_alert_rule["time_range"]:
				gte_date_math_string = self.__utils.getGteDateMathElasticSearch(unit_time, data_alert_rule["time_range"][unit_time])
				lte_date_math_string = self.__utils.getLteDateMathElasticSearch(unit_time)
			search_in_elastic = self.__elasticsearch.createSearchObject(conn_es, data_alert_rule["index_pattern_name"])
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			telegram_bot_token = self.__utils.decryptDataWithAES(data_alert_rule["telegram_bot_token"], passphrase).decode("utf-8")
			telegram_chat_id = self.__utils.decryptDataWithAES(data_alert_rule["telegram_chat_id"], passphrase).decode("utf-8")
			query_string_alert_rule = data_alert_rule["query_type"][0]["query_string"]["query"]
			while True:
				if not data_alert_rule["use_custom_rule_option"] == True:
					if data_alert_rule["use_fields_option"] == True:
						result_search = self.__elasticsearch.executeSearchQueryString(search_in_elastic, gte_date_math_string, lte_date_math_string, query_string_alert_rule, data_alert_rule["use_fields_option"], fields = data_alert_rule["fields_name"])
					else:
						result_search = self.__elasticsearch.executeSearchQueryString(search_in_elastic, gte_date_math_string, lte_date_math_string, query_string_alert_rule, data_alert_rule["use_fields_option"])
					if result_search:
						if len(result_search) >= data_alert_rule["number_events_found_by_alert"]:
							self.__logger.generateApplicationLog("Events found: " + str(len(result_search)), 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
							if data_alert_rule["send_type_alert_rule"] == "multiple":
								self.__sendMultipleAlertRule(result_search, data_alert_rule, telegram_bot_token, telegram_chat_id)
							elif data_alert_rule["send_type_alert_rule"] == "only":
								self.__sendOnlyAlertRule(result_search, data_alert_rule, telegram_bot_token, telegram_chat_id, len(result_search))
					else:
						self.__logger.generateApplicationLog("No events found", 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True)
				else:
					result_search_custom_rule = self.__elasticsearch.executeSearchQueryStringWithAggregation(search_in_elastic, data_alert_rule["field_name_hostname"], gte_date_math_string, lte_date_math_string, query_string_alert_rule, False)
					if result_search_custom_rule:
						for tag_hostname in result_search_custom_rule.aggregations.events.buckets:
							if tag_hostname.doc_count >= data_alert_rule["number_total_events_by_hostname"]:
								if data_alert_rule["restriction_by_username"] == True:
									query_string_alert_rule += " AND " + data_alert_rule['field_name_hostname'] + ':' + tag_hostname.key
									result_search_hostname = self.__elasticsearch.executeSearchQueryStringWithAggregation(search_in_elastic, data_alert_rule["field_name_username"], gte_date_math_string, lte_date_math_string, query_string_alert_rule, False)
									for tag_username in result_search_hostname.aggregations.events.buckets:
										if tag_username.doc_count >= data_alert_rule["number_total_events_by_username"]:
											query_string_alert_rule += " AND " + data_alert_rule['field_name_username'] + ':' + tag_username.key
											if data_alert_rule["use_fields_option"] == True:
												result_search = self.__elasticsearch.executeSearchQueryString(search_in_elastic, gte_date_math_string, lte_date_math_string, query_string_alert_rule, data_alert_rule["use_fields_option"], fields = data_alert_rule["fields_name"])
											else:
												result_search = self.__elasticsearch.executeSearchQueryString(search_in_elastic, gte_date_math_string, lte_date_math_string, query_string_alert_rule, data_alert_rule["use_fields_option"])
											self.__logger.generateApplicationLog("Events found: " + str(len(result_search)), 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
											if data_alert_rule["send_type_alert_rule"] == "multiple":
												self.__sendMultipleAlertRule(result_search, data_alert_rule, telegram_bot_token, telegram_chat_id)
											elif data_alert_rule["send_type_alert_rule"] == "only":
												self.__sendOnlyAlertRule(result_search, data_alert_rule, telegram_bot_token, telegram_chat_id, len(result_search))
					else:
						self.__logger.generateApplicationLog("No events found", 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True)
				sleep(time_search_in_seconds)
		except KeyError as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)
		except (self.__elasticsearch.exceptions.AuthenticationException, self.__elasticsearch.exceptions.ConnectionError, self.__elasticsearch.exceptions.AuthorizationException, self.__elasticsearch.exceptions.RequestError, self.__elasticsearch.exceptions.ConnectionTimeout) as exception:
			self.__logger.generateApplicationLog("Error performing an action in ElasticSearch. For more information, see the logs.", 3, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__" + data_alert_rule["alert_rule_name"], use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)	


	def __sendMultipleAlertRule(self, result_search, data_alert_rule, telegram_bot_token, telegram_chat_id):
		"""
		Method that sends an alert for each event found.

		:arg result_search: Object that contains the result data of the ElasticSearch search.
		:arg data_alert_rule: Object that contains the data of the alert rule.
		:arg telegram_bot_token: Telegram Bot Token.
		:arg telegram_chat_id: Telegram channel identifier where the alert will be send.
		"""
		try:
			message_header = u'\u26A0\uFE0F' + " " + data_alert_rule["alert_rule_name"] +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\U0001f6a6' +  " Alert level: " + data_alert_rule["alert_rule_level"] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
			message_header += "At least " + str(data_alert_rule["number_events_found_by_alert"]) + " event(s) were found." + "\n\nFOUND EVENT:\n\n"
			for hit in result_search:
				message_to_send = message_header + self.__elasticsearch.generateTelegramMessagewithElasticData(hit)
				response_status_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_to_send)
				self.__createLogByTelegramCode(response_status_code, data_alert_rule["alert_rule_name"])
		except KeyError as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)


	def __sendOnlyAlertRule(self, result_search, data_alert_rule, telegram_bot_token, telegram_chat_id, total_events):
		"""
		Method that sends only an alert for all events found.

		:arg result_search: Object that contains the result data of the ElasticSearch search.
		:arg data_alert_rule: Object that contains the data of the alert rule.
		:arg telegram_bot_token: Telegram Bot Token.
		:arg telegram_chat_id: Telegram channel identifier where the alert will be send.
		:arg total_events: Total of events found in the search.
		"""
		try:
			message_header = u'\u26A0\uFE0F' + " " + data_alert_rule["alert_rule_name"] +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\U0001f6a6' +  " Alert level: " + data_alert_rule["alert_rule_level"] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
			message_header += "At least " + str(data_alert_rule["number_events_found_by_alert"]) + " event(s) were found." + "\n\nFOUND EVENT:\n\n"
			for hit in result_search:
				message_to_send = message_header + self.__elasticsearch.generateTelegramMessagewithElasticData(hit)
				break
			message_to_send += "TOTAL EVENTS FOUND: " + str(total_events)
			response_status_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_to_send)
			self.__createLogByTelegramCode(response_status_code, data_alert_rule["alert_rule_name"])
		except KeyError as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)


	def __createLogByTelegramCode(self, response_status_code, alert_rule_name):
		"""
		Method that creates a log based on the HTTP code received as a response.

		:arg response_status_code: HTTP code received in the response when sending the alert to Telegram.
		:arg alert_rule_name: Name of the alert rule from which the alert was sent.
		"""
		if response_status_code == 200:
			self.__logger.generateApplicationLog("Telegram message sent.", 1, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_status_code == 400:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Bad request.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_status_code == 401:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Unauthorized.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_status_code == 404:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Not found.", 3, "__" + alert_rule_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)