from sys import exit
from time import sleep
from datetime import datetime
from modules.UtilsClass import Utils
from ssl import create_default_context
from modules.TelegramClass import Telegram
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
	Property that stores an object of the Telegram class.
	"""
	telegram = None

	"""
	Constructor for the Elastic class.

	Parameters:
	self -- An instantiated object of the Elastic class.
	"""
	def __init__(self):
		self.utils = Utils()
		self.telegram = Telegram()

	"""
	Method that creates a connection object with ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	telk_alert_configuration -- Object that contains the data of the Telk-Alert configuration file.

	Return:
	conn_es -- Object that contains the connection to ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	exceptions.ConnectionError -- Error raised when there was an exception while talking to ES. 
	exceptions.AuthenticationException -- Exception representing a 401 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	InvalidURL -- The URL provided was somehow invalid.
	"""
	def getConnectionElastic(self, telk_alert_configuration):
		conn_es = None
		try:
			if(not telk_alert_configuration['use_ssl_tls'] == True) and (not telk_alert_configuration['use_http_authentication'] == True):
				conn_es = Elasticsearch(telk_alert_configuration['es_host'],
										port = telk_alert_configuration['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
			if(not telk_alert_configuration['use_ssl_tls'] == True) and telk_alert_configuration['use_http_authentication'] == True:
				conn_es = Elasticsearch(telk_alert_configuration['es_host'],
										port = telk_alert_configuration['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(telk_alert_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(telk_alert_configuration['password_http_authentication']).decode('utf-8')),
										use_ssl = False)
			if telk_alert_configuration['use_ssl_tls'] == True and (not telk_alert_configuration['use_http_authentication'] == True):
				if not telk_alert_configuration['validate_certificate_ssl']:
					conn_es = Elasticsearch(telk_alert_configuration['es_host'],
											port = telk_alert_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = telk_alert_configuration['path_certificate_file'])
					conn_es = Elasticsearch(telk_alert_configuration['es_host'],
											port = telk_alert_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if telk_alert_configuration['use_ssl_tls'] == True and telk_alert_configuration['use_http_authentication'] == True:
				if not telk_alert_configuration['validate_certificate_ssl'] == True:
					conn_es = Elasticsearch(telk_alert_configuration['es_host'],
											port = telk_alert_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(telk_alert_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(telk_alert_configuration['password_http_authentication']).decode('utf-8')),
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = telk_alert_configuration['path_certificate_file'])
					conn_es = Elasticsearch(telk_alert_configuration['es_host'],
											port = telk_alert_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(telk_alert_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(telk_alert_configuration['password_http_authentication']).decode('utf-8')),
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if not conn_es == None:
				self.utils.createTelkAlertLog("Established connection with: " + telk_alert_configuration['es_host'] + ':' + str(telk_alert_configuration['es_port']), 1)
				self.utils.createTelkAlertLog("Cluster name: " + conn_es.info()['cluster_name'], 1)
				self.utils.createTelkAlertLog("Elasticsearch version: " + conn_es.info()['version']['number'], 1)
		except (KeyError, exceptions.ConnectionError, exceptions.AuthenticationException, exceptions.AuthorizationException, InvalidURL) as exception:
			self.utils.createTelkAlertLog("Failed to connect to ElasticSearch. For more information, see the logs.", 3)
			self.utils.createTelkAlertLog(exception, 3)
			exit(1)
		else:
			return conn_es
	
	"""
	Method that is in charge of carrying out the searches defined in the alert rules and sending the alerts.

	Parameters:
	self -- An instantiated object of the Elastic class.
	alert_rule_data -- Object with the data corresponding to the alert rule.
	conn_es -- Object that contains the connection to ElasticSearch.
	
	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict).
	"""
	def executionRule(self, alert_rule_data, conn_es):
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
				if not alert_rule_data['custom_rule'] == True:
					self.executeNotCustomRule(alert_rule_data, query_string, search_alert_rule_aux, gte_search)
				else:
					search_alert_custom_rule = search_alert_rule_aux.query(query_string).query('range', ** { '@timestamp' : { 'gte' : gte_search, 'lte' : "now" } }).source(fields = None)
					if alert_rule_data['restriction_hostname'] == True:
						a = A('terms', field = alert_rule_data['field_hostname'])
						search_alert_custom_rule.aggs.bucket('events', a)
					result_search_custom_rule = search_alert_custom_rule.execute()
					for tag_hostname in result_search_custom_rule.aggregations.events.buckets:
						if tag_hostname.doc_count >= alert_rule_data['number_events_hostname']:
							if alert_rule_data['restriction_username'] == True:
								query_string_hostname = Q("query_string", query = query_string_alert_rule + " AND " + alert_rule_data['field_hostname'] + ':' + tag_hostname.key)
								search_alert_rule_hostname = search_alert_rule_aux.query(query_string_hostname).query('range', ** { '@timestamp' : { 'gte' : gte_search, 'lte' : "now" } }).source(fields = None)
								a = A('terms', field = alert_rule_data['field_username'])
								search_alert_rule_hostname.aggs.bucket('events', a)
								result_search_hostname = search_alert_rule_hostname.execute()
								for tag_username in result_search_hostname.aggregations.events.buckets:
									if tag_username.doc_count >= alert_rule_data['number_events_username']:
										query_string_final = Q("query_string", query = query_string_alert_rule + " AND " + alert_rule_data['field_hostname'] + ':' + tag_hostname.key + " AND " + alert_rule_data['field_username'] + ':' + tag_username.key)
										self.executeNotCustomRule(alert_rule_data, query_string_final, search_alert_rule_aux, gte_search)
				sleep(total_time_search_seconds)
		except KeyError as exception:
			self.utils.createTelkAlertLog("Error executing alert rule. For more information, see the logs.", 3)
			self.utils.createTelkAlertLog("Key Error: " + str(exception), 3)
			exit(1)

	"""
	Method that performs the search defined in the alert rule and sends the alerts of a normal alert rule.

	Parameters:
	self -- An instantiated object of the Elastic class.
	alert_rule_data -- Object with the data corresponding to the alert rule.
	query_string -- Query String with which to search for events in ELasticSearch.
	gte_search -- Time range in which the search for events will be carried out.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict).
	"""
	def executeNotCustomRule(self, alert_rule_data, query_string, search_alert_rule_aux, gte_search):
		try:
			if alert_rule_data['specific_fields_search'] == True:
				search_alert_rule = search_alert_rule_aux.query(query_string).query('range', ** { '@timestamp' : { 'gte' : gte_search, 'lte' : "now" } }).source(alert_rule_data['fields_name'])
			else:
				search_alert_rule = search_alert_rule_aux.query(query_string).query('range', ** { '@timestamp' : { 'gte' : gte_search, 'lte' : "now" } }).source(fields = None)
			result_search = search_alert_rule.execute()
			if len(result_search) >= alert_rule_data['num_events']:
				self.utils.createTelkAlertLog(str(len(result_search)) + " rule events found: " + alert_rule_data['name_rule'], 1)
				if alert_rule_data['type_alert_send'] == "multiple":
					self.sendMultipleAlerts(result_search, alert_rule_data)
				elif alert_rule_data['type_alert_send'] == "only":
					self.sendOnlyAlert(result_search, alert_rule_data, len(result_search))
		except KeyError as exception:
			self.utils.createTelkAlertLog("Error executing alert rule. For more information, see the logs.", 3)
			self.utils.createTelkAlertLog("Key Error: " + str(exception), 3)
			exit(1)

	"""
	Method that performs the multiple sending of alerts.

	Parameters:
	self --  An instantiated object of the Elastic class.
	result_search -- An object that contains the results of the ElasticSearch search.
	alert_rule_data -- Object with the data corresponding to the alert rule.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def sendMultipleAlerts(self, result_search, alert_rule_data):
		try:
			for hit in result_search:
				message_telegram = self.telegram.getTelegramHeader(alert_rule_data)
				message_telegram += self.telegram.getTelegramMessage(hit)
				self.telegram.sendTelegramAlert(self.utils.decryptAES(alert_rule_data['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(alert_rule_data['telegram_bot_token']).decode('utf-8'), message_telegram)
		except KeyError as exception:
			self.utils.createTelkAlertLog("Failed to send the alert. For more information, see the logs.", 3)
			self.utils.createTelkAlertLog("Key Error: " + str(exception), 3)
			exit(1)

	"""
	Method that performs the unique sending of alerts.

	Parameters:
	self --  An instantiated object of the Elastic class.
	result_search -- An object that contains the results of the ElasticSearch search.
	alert_rule_data -- Object with the data corresponding to the alert rule.
	total_events -- Total events found during the search.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def sendOnlyAlert(self, result_search, alert_rule_data, total_events):
		try:
			message_telegram = self.telegram.getTelegramHeader(alert_rule_data)
			for hit in result_search:
				message_telegram += self.telegram.getTelegramMessage(hit)
				break
			message_telegram += self.telegram.getTotalEventsFound(total_events)
			self.telegram.sendTelegramAlert(self.utils.decryptAES(alert_rule_data['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(alert_rule_data['telegram_bot_token']).decode('utf-8'), message_telegram)
		except KeyError as exception:
			self.utils.createTelkAlertLog("Failed to send the alert. For more information, see the logs.", 3)
			self.utils.createTelkAlertLog("Key Error: " + str(exception), 3)
			exit(1)