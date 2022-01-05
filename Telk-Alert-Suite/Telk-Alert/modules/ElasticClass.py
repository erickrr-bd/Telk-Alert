from sys import exit
from time import sleep
from datetime import datetime
from modules.UtilsClass import Utils
from ssl import create_default_context
#from modules.TelegramClass import Telegram
from requests.exceptions import InvalidURL
from elasticsearch_dsl import Q, Search, A
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions

"""
Class that manages everything related to ElasticSearch.
"""
class Elastic:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Property that stores an object of type Telegram.
	"""
	#telegram = None

	"""
	Property that stores the data of the Telk-Alert configuration file.
	"""
	telk_alert_configuration = None

	"""
	Constructor for the Elastic class.

	Parameters:
	self -- An instantiated object of the Elastic class.
	"""
	def __init__(self, telk_alert_configuration):
		self.utils = Utils()
		self.telk_alert_configuration = telk_alert_configuration
		#self.telegram = Telegram()

	"""
	Method that creates a connection object with ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.

	Return:
	conn_es -- Object that contains the connection to ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	exceptions.ConnectionError -- Error raised when there was an exception while talking to ES. 
	exceptions.AuthenticationException -- Exception representing a 401 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	InvalidURL -- The URL provided was somehow invalid.
	"""
	def getConnectionElastic(self):
		conn_es = None
		try:
			if(not self.telk_alert_configuration['use_ssl_tls'] == True) and (not self.telk_alert_configuration['use_http_authentication'] == True):
				conn_es = Elasticsearch(self.telk_alert_configuration['es_host'],
										port = self.telk_alert_configuration['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
			if(not self.telk_alert_configuration['use_ssl_tls'] == True) and self.telk_alert_configuration['use_http_authentication'] == True:
				conn_es = Elasticsearch(self.telk_alert_configuration['es_host'],
										port = self.telk_alert_configuration['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(self.telk_alert_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(self.telk_alert_configuration['password_http_authentication']).decode('utf-8')),
										use_ssl = False)
			if self.telk_alert_configuration['use_ssl_tls'] == True and (not self.telk_alert_configuration['use_http_authentication'] == True):
				if not self.telk_alert_configuration['validate_certificate_ssl']:
					conn_es = Elasticsearch(self.telk_alert_configuration['es_host'],
											port = self.telk_alert_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = self.telk_alert_configuration['path_certificate_file'])
					conn_es = Elasticsearch(self.telk_alert_configuration['es_host'],
											port = self.telk_alert_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if self.telk_alert_configuration['use_ssl_tls'] == True and self.telk_alert_configuration['use_http_authentication'] == True:
				if not self.telk_alert_configuration['validate_certificate_ssl'] == True:
					conn_es = Elasticsearch(self.telk_alert_configuration['es_host'],
											port = self.telk_alert_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(self.telk_alert_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(self.telk_alert_configuration['password_http_authentication']).decode('utf-8')),
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = self.telk_alert_configuration['path_certificate_file'])
					conn_es = Elasticsearch(self.telk_alert_configuration['es_host'],
											port = self.telk_alert_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(self.telk_alert_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(self.telk_alert_configuration['password_http_authentication']).decode('utf-8')),
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if not conn_es == None:
				self.utils.createTelkAlertLog("Established connection with: " + self.telk_alert_configuration['es_host'] + ':' + str(self.telk_alert_configuration['es_port']), 1)
				self.utils.createTelkAlertLog("Cluster name: " + conn_es.info()['cluster_name'], 1)
				self.utils.createTelkAlertLog("Elasticsearch version: " + conn_es.info()['version']['number'], 1)
		except (KeyError, exceptions.ConnectionError, exceptions.AuthenticationException, exceptions.AuthorizationException, InvalidURL) as exception:
			self.utils.createTelkAlertLog("Failed to connect to ElasticSearch. For more information, see the logs.", 3)
			self.utils.createTelkAlertLog(exception, 3)
			exit(1)
		else:
			return conn_es
	
	"""
	"""
	def executionRule(self, alert_rule_data):
		conn_es = self.getConnectionElastic()
		try:
			for unit_time in alert_rule_data['time_search']:
				total_time_search_seconds = self.utils.convertTimeToSeconds(unit_time, alert_rule_data['time_search'][unit_time])
			for unit_time in alert_rule_data['time_range']:
				gte_search = self.utils.convertTimeToStringSearch(unit_time, alert_rule_data['time_range'][unit_time])
			query_string_alert_rule = alert_rule_data['query_type'][0]['query_string']['query']
			search_alert_rule_aux = Search(index = alert_rule_data['index_name']).using(conn_es)
			search_alert_rule_aux = search_alert_rule_aux[0:10000]
			query_string = Q("query_string", query = query_string_alert_rule)
			while True:
				if alert_rule_data['specific_fields_search'] == True:
					search_alert_rule = search_alert_rule_aux.query(query_string).query('range', ** { '@timestamp' : { 'gte' : gte_search, 'lte' : "now" } }).source(alert_rule_data['fields_name'])
				else:
					search_alert_rule = search_alert_rule_aux.query(query_string).query('range', ** { '@timestamp' : { 'gte' : gte_search, 'lte' : "now" } }).source(fields = None)
				result_search = search_alert_rule.execute()
				total_events = 0
				for hit in result_search['hits']['hits']:
					print(hit['_source']['message'])
					total_events += 1
				sleep(total_time_search_seconds)
		except KeyError as exception:
			self.utils.createTelkAlertLog("Error executing alert rule. For more information, see the logs.", 3)
			self.utils.createTelkAlertLog("Key Error: " + str(exception), 3)
			exit(1)


	"""
	Method that performs the search in ElasticSearch and in case of finding events, it sends the alert.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	rule_yaml -- List containing all the data of the alert rule.
	telk_alert_conf -- List containing all the information in the Telk-Alert configuration file.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	ValueError -- Is raised when a function receives an argument of the correct type but an inappropriate value. 
	TypeError -- The TypeError is thrown when an operation or function is applied to an object of an inappropriate type.
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
						time_search = self.utils.convertTimeToMilliseconds(unit_time, rule_yaml['time_search'][unit_time]) / 1000
					for unit_time in rule_yaml['time_back']:
						time_back = self.utils.convertTimeToMilliseconds(unit_time, rule_yaml['time_back'][unit_time])
					query_string_rule = rule_yaml['filter_search'][0]['query_string']['query']
					search_rule = Search(index = rule_yaml['index_name']).using(conn_es)
					search_rule = search_rule[0:int(telk_alert_conf['max_hits'])]
					query = Q("query_string", query = query_string_rule)
					while True:
						if rule_yaml['use_restriction_fields'] == True:
							search_aux = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : "now-2m", 'lte' : "now" } }).source(rule_yaml['fields'])
						else:
							search_aux = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : "now-2m", 'lte' : "now" } }).source(fields = None)
						if rule_yaml['restrict_by_host'] == True:
							a = A('terms', field = rule_yaml['field_hostname'])
							search_aux = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : "now-2m", 'lte' : "now" } }).source(fields = None)
							search_aux.aggs.bucket('events', a)
						result_search = search_aux.execute()
						total_events = 0
						for hit in result_search:
							total_events += 1
						if total_events >= rule_yaml['num_events']:
							self.logger.createLogTelkAlert(str(total_events) + " events found in the rule: " + rule_yaml['name_rule'], 2)
							self.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.createLogAction(str(total_events) + " events found in the rule: " + rule_yaml['name_rule']))
							print(str(total_events) + " events found in the rule: " + rule_yaml['name_rule'])
							if rule_yaml['restrict_by_host'] == True:
								for tag in result_search.aggregations.events.buckets:
									if int(tag.doc_count) >= rule_yaml['number_events_host']:
										self.logger.createLogTelkAlert(str(tag.doc_count) + " events found in the host " + tag.key + " in the rule: " + rule_yaml['name_rule'], 2)
										self.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.createLogAction(str(tag.doc_count) + " events found in the host " + tag.key +" in the rule: " + rule_yaml['name_rule']))
										print(str(tag.doc_count) + " events found in the host " + tag.key +  " in the rule: " + rule_yaml['name_rule'])
										if rule_yaml['type_alert_send'] == "multiple":
											self.sendMultipleAlerts(result_search, rule_yaml, flag_telegram, flag_email, time_back, conn_es, telk_alert_conf['writeback_index'])
										if rule_yaml['type_alert_send'] == "only":
											self.sendOnlyAlert(result_search, rule_yaml, flag_telegram, flag_email, time_back, tag.doc_count, conn_es, telk_alert_conf['writeback_index'])
							else:
								if rule_yaml['type_alert_send'] == "multiple":
									self.sendMultipleAlerts(result_search, rule_yaml, flag_telegram, flag_email, time_back, conn_es, telk_alert_conf['writeback_index'])
								if rule_yaml['type_alert_send'] == "only":
									self.sendOnlyAlert(result_search, rule_yaml, flag_telegram, flag_email, time_back, total_events, conn_es, telk_alert_conf['writeback_index'])
						time.sleep(time_search)
			else:
				self.logger.createLogTelkAlert("The index does not exist in ElasticSearch.", 4)
				print("\nThe index does not exist in ElasticSearch")
				sys.exit(1)
		except KeyError as exception:
			self.logger.createLogTelkAlert("Key Error: " + str(exception), 4)
			print("\nKey Error: " + str(exception))
			sys.exit(1)
		except ValueError as exception:
			self.logger.createLogTelkAlert("Value Error: " + str(exception), 4)
			print("\nValue Error: " + str(exception))
			sys.exit(1)
		except TypeError as exception:
			self.logger.createLogTelkAlert("Type Error: " + str(exception), 4)
			print("\nType Error:" + str(exception) + ". For more information see the application logs.")
			sys.exit(1)

	"""
	Method that performs the multiple sending of alerts.

	Parameters:
	self --  An instantiated object of the Elastic class.
	result_search -- An object that contains the results of the ElasticSearch search.
	rule_yaml -- List containing all the data of the alert rule.
	flag_telegram -- Flag that indicates if the alert should be sent to telegram.
	time_back -- Backward time in milliseconds.
	conn_es -- Object that contains the connection to ElasticSearch.
	index_name -- Name of the index where the search is performed in ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def sendMultipleAlerts(self, result_search, rule_yaml, flag_telegram, flag_email, time_back, conn_es, index_name):
		try:
			for hit in result_search:
				if flag_telegram == 1:
					message_telegram = self.telegram.getTelegramHeader(rule_yaml, time_back)
					message_telegram += self.telegram.getTelegramMessage(hit)
					telegram_code = self.telegram.sendTelegramAlert(self.utils.decryptAES(rule_yaml['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(rule_yaml['telegram_bot_token']).decode('utf-8'), message_telegram)
					self.generateLogES(index_name, conn_es, self.createLogAlertTelegram(rule_yaml['name_rule'], 1, telegram_code))
					self.telegram.getStatusByTelegramCode(telegram_code, rule_yaml['name_rule'])
				if flag_email == 1:
					message_email = self.email.getEmailHeader(rule_yaml, time_back)
					message_email += self.email.getEmailMessage(hit)
					response = self.email.sendEmailAlert(rule_yaml['email_from'], self.utils.decryptAES(rule_yaml['email_from_password']).decode('utf-8'), rule_yaml['email_to'], message_email, rule_yaml['name_rule'])
					self.email.getStatusEmailAlert(response, rule_yaml['email_to'])
					self.generateLogES(index_name, conn_es, self.createLogAlertEmail(rule_yaml['name_rule'], 1, response))
		except KeyError as exception:
			self.logger.createLogTelkAlert("Key error: " + str(exception), 4)
			print("\nKey Error: " + str(exception))
			sys.exit(1)


	"""
	Method that performs the unique sending of alerts.

	Parameters:
	self --  An instantiated object of the Elastic class.
	result_search -- An object that contains the results of the ElasticSearch search.
	rule_yaml -- List containing all the data of the alert rule.
	flag_telegram -- Flag that indicates if the alert should be sent to telegram.
	time_back -- Backward time in milliseconds.
	total_events -- Total events found in the search.
	conn_es -- Object that contains the connection to ElasticSearch.
	index_name -- Name of the index where the search is performed in ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def sendOnlyAlert(self, result_search, rule_yaml, flag_telegram, flag_email, time_back, total_events, conn_es, index_name):
		message_telegram = self.telegram.getTelegramHeader(rule_yaml, time_back)
		message_email = self.email.getEmailHeader(rule_yaml, time_back)
		for hit in result_search:
			message_telegram += self.telegram.getTelegramMessage(hit)
			message_email += self.email.getEmailMessage(hit)
			break
		try:
			if flag_telegram == 1:
				message_telegram += self.telegram.getTotalEventsFound(total_events)
				telegram_code = self.telegram.sendTelegramAlert(self.utils.decryptAES(rule_yaml['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(rule_yaml['telegram_bot_token']).decode('utf-8'), message_telegram)
				self.generateLogES(index_name, conn_es, self.createLogAlertTelegram(rule_yaml['name_rule'], total_events, telegram_code))
				self.telegram.getStatusByTelegramCode(telegram_code, rule_yaml['name_rule'])
			if flag_email == 1:
				message_email += self.email.getTotalEventsFound(total_events)
				response = self.email.sendEmailAlert(rule_yaml['email_from'], self.utils.decryptAES(rule_yaml['email_from_password']).decode('utf-8'), rule_yaml['email_to'], message_email, rule_yaml['name_rule'])
				self.email.getStatusEmailAlert(response, rule_yaml['email_to'])
				self.generateLogES(index_name, conn_es, self.createLogAlertEmail(rule_yaml['name_rule'], total_events, response))
		except KeyError as exception:
			self.logger.createLogTelkAlert("Key error: " + str(exception), 4)
			print("\nKey Error: " + str(exception))
			sys.exit(1)