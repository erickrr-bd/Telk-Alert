from sys import exit
from threading import Thread
from libPyLog import libPyLog
from libPyElk import libPyElk
from time import sleep, strftime
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram

"""
Class that manages the operation of Telk-Alert-Report.
"""
class TelkAlertReport:

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
		self.__telegram = libPyTelegram()
		self.__elasticsearch = libPyElk()


	def startTelkAlertReport(self):
		"""
		Method that starts the Telk-Alert-Report application.
		"""
		try:
			data_report_configuration = self.__utils.readYamlFile(self.__constants.PATH_FILE_REPORT_CONFIGURATION)
			if data_report_configuration["use_http_authentication"] == True:
				conn_es = self.__elasticsearch.createConnectionToElasticSearch(data_report_configuration, path_key_file = self.__constants.PATH_KEY_FILE)
			else:
				conn_es = self.__elasticsearch.createConnectionToElasticSearch(data_report_configuration)
			if not conn_es == None:
				self.__logger.generateApplicationLog("Telk-Alert-Report v3.2", 1, "__start", use_stream_handler = True)
				self.__logger.generateApplicationLog("@2022 Tekium. All rights reserved.", 1, "__start", use_stream_handler = True)
				self.__logger.generateApplicationLog("Author: Erick Rodriguez", 1, "__start", use_stream_handler = True)
				self.__logger.generateApplicationLog("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com", 1, "__start", use_stream_handler = True)
				self.__logger.generateApplicationLog("License: GPLv3", 1, "__start", use_stream_handler = True)
				self.__logger.generateApplicationLog("Telk-Alert-Report started", 1, "__start", use_stream_handler = True)
				self.__logger.generateApplicationLog("Established connection with: " + data_report_configuration["es_host"] + ':' + str(data_report_configuration["es_port"]), 1, "__connection" , use_stream_handler = True)
				self.__logger.generateApplicationLog("Elasticsearch Cluster Name: " + conn_es.info()["cluster_name"], 1, "__connection", use_stream_handler = True)
				self.__logger.generateApplicationLog("Elasticsearch Version: " + conn_es.info()["version"]["number"], 1, "__connection", use_stream_handler = True)
				for alert_rule in data_report_configuration["list_all_alert_rules"]:
					self.__logger.generateApplicationLog(alert_rule[:-5] + " loaded", 1, "__alertRule", use_stream_handler = True)
					data_alert_rule = self.__utils.readYamlFile(data_report_configuration["path_alert_rules_folder"] + '/' + alert_rule)
					Thread(name = alert_rule[:-5], target = self.__getAlertRuleReport, args = (conn_es, data_alert_rule, )).start()
		except KeyError as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__start", use_stream_handler = True, use_file_handler = True, name_file_log  = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)
		except (OSError, FileNotFoundError) as exception:
			self.__logger.generateApplicationLog("Error to open or read a file. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, name_file_log  = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)
		except (self.__elasticsearch.exceptions.AuthenticationException, self.__elasticsearch.exceptions.ConnectionError, self.__elasticsearch.exceptions.AuthorizationException, self.__elasticsearch.exceptions.RequestError, self.__elasticsearch.exceptions.ConnectionTimeout) as exception:
			self.__logger.generateApplicationLog("Error connecting with ElasticSearch. For more information, see the logs.", 3, "__connection", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__connection", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)


	def __getAlertRuleReport(self, conn_es, data_alert_rule):
		"""
		"""
		try:
			search_in_elastic = self.__elasticsearch.createSearchObject(conn_es, data_alert_rule["index_pattern_name"])
			query_string_alert_rule = data_alert_rule["query_type"][0]["query_string"]["query"]
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			telegram_bot_token = self.__utils.decryptDataWithAES(data_alert_rule["telegram_bot_token"], passphrase).decode("utf-8")
			telegram_chat_id = self.__utils.decryptDataWithAES(data_alert_rule["telegram_chat_id"], passphrase).decode("utf-8")
			path_table_file = self.__constants.PATH_TABLE_FILES + '/' + data_alert_rule["alert_rule_name"] + ".txt"
			#This block is optional
			if "fields_name" in data_alert_rule:
				if "message" in data_alert_rule["fields_name"]:
					data_alert_rule["fields_name"].remove("message")
			#End block
			if data_alert_rule["use_fields_option"] == True:
				result_search = self.__elasticsearch.executeSearchQueryString(search_in_elastic, "now-1d/d", "now/d", query_string_alert_rule, data_alert_rule["use_fields_option"], fields = data_alert_rule["fields_name"])
			else:
				result_search = self.__elasticsearch.executeSearchQueryString(search_in_elastic, "now-1d/d", "now/d", query_string_alert_rule, data_alert_rule["use_fields_option"])
			if result_search:
				self.__logger.generateApplicationLog("Events found: " + str(len(result_search)), 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True)
				for hit in result_search:
					headers_table = self.__elasticsearch.getFieldsofElasticData(hit)
					data_table = self.__elasticsearch.generateArraywithElasticData(hit)
				self.__utils.createFileWithTable(path_table_file, data_table, headers_table)
				self.__utils.changeOwnerToPath(path_table_file, self.__constants.USER, self.__constants.GROUP)
				message_to_send = u'\u26A0\uFE0F' + " " + data_alert_rule["alert_rule_name"] +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\U0001f6a6' +  " Alert level: " + data_alert_rule["alert_rule_level"] + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
				message_to_send += "TOTAL EVENTS FOUND: " + str(len(result_search))
				response_status_code = self.__telegram.sendFileMessageTelegram(telegram_bot_token, telegram_chat_id, message_to_send.encode("utf-8"), path_table_file)
				self.__createLogByTelegramCode(response_status_code, data_alert_rule["alert_rule_name"])
			else:
				self.__logger.generateApplicationLog("No events found", 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True)
		except KeyError as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__start", use_stream_handler = True, use_file_handler = True, name_file_log  = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)
		except (OSError, FileNotFoundError) as exception:
			self.__logger.generateApplicationLog("Error to open or read a file. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, name_file_log  = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			exit(1)
		except (self.__elasticsearch.exceptions.AuthenticationException, self.__elasticsearch.exceptions.ConnectionError, self.__elasticsearch.exceptions.AuthorizationException, self.__elasticsearch.exceptions.RequestError, self.__elasticsearch.exceptions.ConnectionTimeout) as exception:
			self.__logger.generateApplicationLog("Error connecting with ElasticSearch. For more information, see the logs.", 3, "__connection", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__connection", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
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