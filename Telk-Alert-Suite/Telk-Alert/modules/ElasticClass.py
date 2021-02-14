import sys
import time
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions
from elasticsearch_dsl import Q, Search, A
sys.path.append('./modules')
from UtilsClass import Utils
from LoggerClass import Logger
from TelegramClass import Telegram

"""
Class that allows you to manage everything related to ElasticSearch.
"""
class Elastic:

	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Telegram type object.
	"""
	telegram = Telegram()

	"""
	Method that establishes the connection of Telk-Alert with ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	telk_alert_conf -- List containing all the information in the Telk-Alert configuration file.

	Return:
	conn_es -- Object that contains the connection to ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES. 
	exceptions.AuthenticationException -- Exception representing a 401 status code.
	"""
	def getConnectionElastic(self, telk_alert_conf):
		try:
			if (not telk_alert_conf['use_ssl']) and (not telk_alert_conf['use_http_auth']):
				conn_es = Elasticsearch([telk_alert_conf['es_host']], 
										port = telk_alert_conf['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
			if (not telk_alert_conf['use_ssl']) and telk_alert_conf['use_http_auth']:
				conn_es = Elasticsearch([telk_alert_conf['es_host']], 
										port = telk_alert_conf['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(telk_alert_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(telk_alert_conf['http_auth_pass']).decode('utf-8')),
										use_ssl = False)
			if telk_alert_conf['use_ssl'] and (not telk_alert_conf['use_http_auth']):
				if not telk_alert_conf['valid_certificates']:
					conn_es = Elasticsearch([telk_alert_conf['es_host']], 
											port = telk_alert_conf['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn=False)
			if telk_alert_conf['use_ssl'] and telk_alert_conf['use_http_auth']:
				if not telk_alert_conf['valid_certificates']:
					conn_es = Elasticsearch([telk_alert_conf['es_host']], 
											port = telk_alert_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(telk_alert_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(telk_alert_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn=False)
			print("\nCONNECTION DATA\n")
			print("Cluster name: " + conn_es.info()['cluster_name'])
			print("ElasticSearch Version: " + conn_es.info()['version']['number'])
			if conn_es.ping():
				print("Connection established to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']) + '\n')
				return conn_es
		except KeyError as exception:
			print("\nKey error: " + str(exception) + '. For more information see the application logs.')
			self.logger.createLogTelkAlert("Key error: " + str(exception), 4)
			sys.exit(1)
		except exceptions.ConnectionError as exception:
			print("Failed connection to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']) + '. For more information see the application logs.')
			self.logger.createLogTelkAlert(str(exception), 4)
			sys.exit(1)
		except exceptions.AuthenticationException as exception:
			print("HTTP authentication failed. For more information see the application logs.")
			self.logger.createLogTelkAlert(str(exception), 4)
			sys.exit(1)
	
	"""
	"""
	def searchRuleElastic(self, conn_es, rule_yaml, telk_alert_conf):
		try:
			if conn_es.indices.exists(index = rule_yaml['index_name']):
				if rule_yaml['type_alert'] == 'Frequency':
					flag_email = 0
					flag_telegram = 0
					for i in range(len(rule_yaml['alert'])):
						if rule_yaml['alert'][i] == "email":
							flag_email = 1
						if rule_yaml['alert'][i] == "telegram":
							flag_telegram = 1
					for unit_time in rule_yaml['time_search']:
						time_search = self.utils.convertTimeToMilliseconds(unit_time, rule_yaml['time_search'][unit_time])
					for unit_time in rule_yaml['time_back']:
						time_back = self.utils.convertTimeToMilliseconds(unit_time, rule_yaml['time_back'][unit_time])
					query_string_rule = rule_yaml['filter_search'][0]['query_string']['query']
					search_rule = Search(index = rule_yaml['index_name']).using(conn_es)
					search_rule = search_rule[0:int(telk_alert_conf['max_hits'])]
					query = Q("query_string", query = query_string_rule)
					while True:
						if not rule_yaml['restrict_by_host']:
							total_events = 0
							if rule_yaml['use_restriction_fields']:
								result_search = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : self.utils.convertDateToMilliseconds(datetime.now()) - time_back, 'lte' : self.utils.convertDateToMilliseconds(datetime.now()) } }).source(rule_yaml['fields'])
							else:
								search_aux = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : self.utils.convertDateToMilliseconds(datetime.now()) - time_back, 'lte' : self.utils.convertDateToMilliseconds(datetime.now()) } }).source(fields = None)
								result_search = search_aux.execute()
							for hit in result_search:
								total_events += 1
							if total_events >= rule_yaml["num_events"]:
								if rule_yaml['type_alert_send'] == "multiple":
									for hit in result_search:
										if flag_telegram == 1:
											message_telegram = self.telegram.getTelegramHeader(rule_yaml, time_back)
											message_telegram += self.telegram.getTelegramMessage(hit)
											#telegram_code = self.telegram.sendTelegramAlert(self.utils.decryptAES(rule_yaml['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(rule_yaml['telegram_bot_token']).decode('utf-8'), message_telegram)
											#self.telegram.getStatusByTelegramCode(telegram_code)
								if rule_yaml['type_alert_send'] == "only":
									message_telegram = self.telegram.getTelegramHeader(rule_yaml, time_back)
									for hit in result_search:
										message_telegram += self.telegram.getTelegramMessage(hit)
										break
									if flag_telegram == 1:
										message_telegram += self.telegram.getTotalEventsFound(total_events)
										print(message_telegram)
										#telegram_code = self.telegram.sendTelegramAlert(self.utils.decryptAES(rule_yaml['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(rule_yaml['telegram_bot_token']).decode('utf-8'), message_telegram)
										#self.telegram.getStatusByTelegramCode(telegram_code)
						else:
							a = A('terms', field = rule_yaml['field_hostname'])
							search_aux = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : self.utils.convertDateToMilliseconds(datetime.now()) - time_back, 'lte' : self.utils.convertDateToMilliseconds(datetime.now()) } }).source(fields = None)
							search_aux.aggs.bucket('events', a)
							result_search = search_aux.execute()
							for tag in result_search.aggregations.events.buckets:
								print(tag.key, tag.doc_count)
								if int(tag.doc_count) >= rule_yaml['number_events_host']:
									for hit in result_search:
										if flag_telegram == 1:
											message_telegram = self.telegram.getTelegramHeader(rule_yaml, time_back)
											message_telegram += self.telegram.getTelegramMessage(hit)
											telegram_code = self.telegram.sendTelegramAlert(self.utils.decryptAES(rule_yaml['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(rule_yaml['telegram_bot_token']).decode('utf-8'), message_telegram)
											self.telegram.getStatusByTelegramCode(telegram_code)
						time.sleep(time_search)
		except KeyError as exception:
			print("Key Error: " + str(exception))
			sys.exit(1)