import json
from threading import Thread
from tabulate import tabulate
from libPyLog import libPyLog
from libPyElk import libPyElk
from libPyUtils import libPyUtils
from .Constants_Class import Constants

class TelkAlertReport:

	__utils = None

	__logger = None

	__constants = None

	__elasticsearch = None


	def __init__(self):
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__elasticsearch = libPyElk()


	def startTelkAlertReport(self):
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
				self.__logger.generateApplicationLog("Established connection with: " + data_report_configuration["es_host"] + ':' + str(data_report_configuration["es_port"]), 1, "__start" , use_stream_handler = True)
				self.__logger.generateApplicationLog("Elasticsearch Cluster Name: " + conn_es.info()["cluster_name"], 1, "__start", use_stream_handler = True)
				self.__logger.generateApplicationLog("Elasticsearch Version: " + conn_es.info()["version"]["number"], 1, "__start", use_stream_handler = True)
				for alert_rule in data_report_configuration["list_all_alert_rules"]:
					self.__logger.generateApplicationLog(alert_rule[:-5] + " loaded", 1, "__start", use_stream_handler = True)
					data_alert_rule = self.__utils.readYamlFile(data_report_configuration["path_alert_rules_folder"] + '/' + alert_rule)
					Thread(name = alert_rule[:-5], target = self.__getAlertRuleReport, args = (conn_es, data_alert_rule, )).start()
		except KeyError as exception:
			print("Error")
		except (OSError, FileNotFoundError) as exception:
			print("Error 2")


	def __getAlertRuleReport(self, conn_es, data_alert_rule):
		try:
			search_in_elastic = self.__elasticsearch.createSearchObject(conn_es, data_alert_rule["index_pattern_name"])
			query_string_alert_rule = data_alert_rule["query_type"][0]["query_string"]["query"]
			if "fields_name" in data_alert_rule:
				if "message" in data_alert_rule["fields_name"]:
					data_alert_rule["fields_name"].remove("message")
			if data_alert_rule["use_fields_option"] == True:
				result_search = self.__elasticsearch.executeSearchQueryString(search_in_elastic, "now-1d/d", "now/d", query_string_alert_rule, data_alert_rule["use_fields_option"], fields = data_alert_rule["fields_name"])
			else:
				result_search = self.__elasticsearch.executeSearchQueryString(search_in_elastic, "now-1d/d", "now/d", query_string_alert_rule, data_alert_rule["use_fields_option"])
			if result_search:
				for hit in result_search:
					headers = self.__elasticsearch.getFieldsofElasticData(hit)
					data = self.__elasticsearch.generateArraywithElasticData(hit)
					with open('/home/erodriguez/Documentos/table_' + data_alert_rule["alert_rule_name"] + ".txt", 'w') as f:
						f.write(tabulate(data, headers, tablefmt = "grid"))
				#d = json.loads(result_search)
				#print(tabulate(d))
			else:
				self.__logger.generateApplicationLog("No events found", 1, "__" + data_alert_rule["alert_rule_name"], use_stream_handler = True)
		except KeyError as exception:
			print("Error")
		except (self.__elasticsearch.exceptions.ConnectionTimeout) as exception:
			print("Error 2")