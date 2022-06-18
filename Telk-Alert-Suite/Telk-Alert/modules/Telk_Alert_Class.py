from os import path
from threading import Thread
from libPyElk import libPyElk
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from .Constants_Class import Constants

class TelkAlert:

	__utils = None

	__logger = None

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
							Thread(name = alert_rule,target = self.__startAlertRule, args = (conn_es, data_alert_rule, )).start()
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
			print(time_search_in_seconds)
			for unit_time in data_alert_rule["time_range"]:
				date_math_time_range = self.__utils.convertTimeToDateMath(unit_time, data_alert_rule["time_range"][unit_time])
			print(date_math_time_range)
		except KeyError as exception:
			print("Error")