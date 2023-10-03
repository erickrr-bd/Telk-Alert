from os import path
from time import sleep
from threading import Thread
from libPyElk import libPyElk
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from .Telegram_Messages_Class import TelegramMessages

"""
Class that manages Telk-Alert actions.
"""
class TelkAlert:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.elasticsearch = libPyElk()
		self.telegram = libPyTelegram()
		self.telegram_messages = TelegramMessages()


	def start_telk_alert(self):
		"""
		Method that starts Telk-Alert.
		"""
		try:
			self.logger.generateApplicationLog("Copyright@2023 Tekium. All rights reserved.", 1, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog("Author: Erick Roberto Rodríguez Rodríguez", 1, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 1, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog("Github: https://github.com/erickrr-bd/Telk-Alert", 1, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog("Telk-Alert v3.3 - October 2023", 1, "__start", use_stream_handler = True)
			if path.exists(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH):
				self.logger.generateApplicationLog("Reading configuration file in: " + self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH, 1, "__readConfigurationFile", use_stream_handler = True)
				telk_alert_data = self.utils.readYamlFile(self.constants.TELK_ALERT_CONFIGURATION_FILE_PATH)
				if telk_alert_data["use_authentication_method"]:
					if telk_alert_data["authentication_method"] == "HTTP Authentication":
						conn_es = self.elasticsearch.createConnectionHTTPAuthentication(telk_alert_data, self.constants.KEY_FILE_PATH)
					elif telk_alert_data["authentication_method"] == "API Key":
						conn_es = self.elasticsearch.createConnectionAPIKey(telk_alert_data, self.constants.KEY_FILE_PATH)
				else:
					conn_es = self.elasticsearch.createConnectionWithoutAuthentication(telk_alert_data)
				self.logger.generateApplicationLog("Connection established with: " + ','.join(telk_alert_data["es_host"]) + " Port: " + str(telk_alert_data["es_port"]), 1, "__clusterConnection", use_stream_handler = True)
				self.logger.generateApplicationLog("ElasticSearch Cluster Name: " + conn_es.info()["cluster_name"], 1, "__clusterConnection", use_stream_handler = True)
				self.logger.generateApplicationLog("ElasticSearch Version: " + conn_es.info()["version"]["number"], 1, "__clusterConnection", use_stream_handler = True)
				self.logger.generateApplicationLog("Connection established using SSL/TLS", 1, "__clusterConnection", use_stream_handler = True) if telk_alert_data["use_ssl_tls"] else self.logger.generateApplicationLog("Connection established without SSL/TLS", 2, "__clusterConnection", use_stream_handler = True)
				self.logger.generateApplicationLog("SSL certificate verification enabled", 1, "__clusterConnection", use_stream_handler = True) if telk_alert_data["verificate_certificate_ssl"] else self.logger.generateApplicationLog("SSL certificate verification disabled", 2, "__clusterConnection", use_stream_handler = True)
				self.logger.generateApplicationLog("Certificate file path: " + telk_alert_data["certificate_file_path"], 1, "__clusterConnection", use_stream_handler = True) if telk_alert_data["verificate_certificate_ssl"] else self.logger.generateApplicationLog("Certificate file path: None", 2, "__clusterConnection", use_stream_handler = True)
				self.logger.generateApplicationLog("Authentication method enabled", 1, "__clusterConnection", use_stream_handler = True) if telk_alert_data["use_authentication_method"] else self.logger.generateApplicationLog("Authentication method disabled", 2, "__clusterConnection", use_stream_handler = True)
				if telk_alert_data["use_authentication_method"]:
					self.logger.generateApplicationLog("Authentication method: " + telk_alert_data["authentication_method"], 1, "__clusterConnection", use_stream_handler = True) if telk_alert_data["authentication_method"] == "HTTP Authentication" else self.logger.generateApplicationLog("Authentication method: " + telk_alert_data["authentication_method"], 1, "__clusterConnection", use_stream_handler = True)
				alert_rules_folder_path = self.constants.TELK_ALERT_PATH + '/' + telk_alert_data["alert_rules_folder"]
				alert_rules_list = self.utils.getListYamlFilesInFolder(alert_rules_folder_path)
				if alert_rules_list:
					self.logger.generateApplicationLog(str(len(alert_rules_list)) + " alert rule(s) found in: " + alert_rules_folder_path, 1, "__readAlertRules", use_stream_handler = True)
					for alert_rule in alert_rules_list:
						alert_rule_data = self.utils.readYamlFile(alert_rules_folder_path + '/' + alert_rule)
						Thread(name = alert_rule[:-5], target = self.start_alert_rule, args = (conn_es, alert_rule_data)).start()
				else:
					self.logger.generateApplicationLog("No alert rules found in: " + alert_rules_folder_path, 1, "__readAlertRules", use_stream_handler = True) 
			else:
				self.logger.generateApplicationLog("Configuration file not found", 3, "__readConfigurationFile", use_stream_handler = True)
		except Exception as exception:
			self.logger.generateApplicationLog("Error starting Telk-Alert. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)


	def start_alert_rule(self, conn_es, alert_rule_data):
		"""

		"""
		try:
			self.logger.generateApplicationLog(alert_rule_data["alert_rule_name"] + " loaded", 1, "__readAlertRules", use_stream_handler = True)
			search_unit_time = list(alert_rule_data["search_time"].keys())[0]
			search_time_seconds = self.utils.convertTimeToSeconds(search_unit_time, alert_rule_data["search_time"][search_unit_time])
			range_unit_time = list(alert_rule_data["range_time"].keys())[0]
			gte_date_math = self.utils.getGteDateMath(range_unit_time, alert_rule_data["range_time"][range_unit_time])
			lte_date_math = self.utils.getLteDateMath(range_unit_time)
			passphrase = self.utils.getPassphraseKeyFromFile(self.constants.KEY_FILE_PATH)
			telegram_bot_token = self.utils.decryptDataWithAES(alert_rule_data["telegram_bot_token"], passphrase).decode("utf-8")
			telegram_chat_id = self.utils.decryptDataWithAES(alert_rule_data["telegram_chat_id"], passphrase).decode("utf-8")
			query_string = alert_rule_data["query_type"][0]["query_string"]["query"]
			search = self.elasticsearch.createSearch(conn_es, alert_rule_data["index_pattern"])
			list_timestamp = []
			while True:
				if alert_rule_data["use_custom_search"]:
					print("Custom")
				else:
					if alert_rule_data["use_fields_selection"]:
						result = self.elasticsearch.searchByQueryString(search, query_string, gte_date_math, lte_date_math, alert_rule_data["use_fields_selection"], fields_name = alert_rule_data["fields_name"])
					else:
						result = self.elasticsearch.searchByQueryString(search, query_string, gte_date_math, lte_date_math, alert_rule_data["use_fields_selection"])
					if result:
						if len(result) >= alert_rule_data["total_number_events"]:
							print(list_timestamp)
							self.logger.generateApplicationLog("Events found: " + str(len(result)), 1, "__" + alert_rule_data["alert_rule_name"], use_stream_handler = True, use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
							if alert_rule_data["alert_delivery_type"] == "multiple":
								for hit in result:
									if hit["@timestamp"] in list_timestamp:
										list_timestamp.remove(hit["@timestamp"])
									else:
										telegram_message = self.telegram_messages.generate_telegram_message(hit, alert_rule_data)
										response_http_code = self.telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, telegram_message)
										self.telegram_messages.create_log_by_telegram_code(response_http_code, alert_rule_data["alert_rule_name"])
										list_timestamp.append(hit["@timestamp"])
							elif alert_rule_data["alert_delivery_type"] == "only":
								for hit in result:
									telegram_message = self.telegram_messages.generate_telegram_message(hit, alert_rule_data)
									break
								telegram_message += "TOTAL EVENTS FOUND: " + str(len(result))
								response_http_code = self.telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, telegram_message)
								self.telegram_messages.create_log_by_telegram_code(response_http_code, alert_rule_data["alert_rule_name"])
					else:
						self.logger.generateApplicationLog("No events found", 1, "__" + alert_rule_data["alert_rule_name"], use_stream_handler = True)
				sleep(search_time_seconds)
		except Exception as exception:
			self.logger.generateApplicationLog("Error executing alert rule. For more information, see the logs.", 3, "__" + alert_rule_data["alert_rule_name"], use_stream_handler = True)
			self.logger.generateApplicationLog(exception, 3, "__" + alert_rule_data["alert_rule_name"], use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)

"""
def __startAlertRule(self, conn_es, data_alert_rule):
		try:
			while True:
				if not data_alert_rule["use_custom_rule_option"] == True:
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
"""