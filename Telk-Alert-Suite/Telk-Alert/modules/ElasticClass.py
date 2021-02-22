import sys
import time
import socket
import requests
import platform
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions
from elasticsearch_dsl import Q, Search, A
from modules.LoggerClass import Logger
from modules.UtilsClass import Utils
from modules.TelegramClass import Telegram
from modules.EmailClass import Email

"""
Class that allows you to manage everything related to ElasticSearch.
"""
class Elastic:

	"""
	Property that stores the IP where Telk-Alert is working.
	"""
	host_ip = ""

	"""
	Property that stores the name of the host where Telk-Alert is working.
	"""
	host_name = ""

	"""
	Property where the operating system of the host where Telk-Alert is working is stored.
	"""
	host_os_name = ""

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
	Telegram type object.
	"""
	email = Email()

	"""
	Constructor for the Elastic class.

	Parameters:
	self -- An instantiated object of the Elastic class.
	"""
	def __init__(self):
		self.host_name = socket.gethostname()
		self.host_ip = socket.gethostbyname(self.host_name)
		self.host_os_name = platform.linux_distribution()

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
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	requests.exceptions.InvalidURL -- The URL provided was somehow invalid
	"""
	def getConnectionElastic(self, telk_alert_conf):
		try:
			if (not telk_alert_conf['use_ssl'] == True) and (not telk_alert_conf['use_http_auth'] == True):
				conn_es = Elasticsearch([telk_alert_conf['es_host']], 
										port = telk_alert_conf['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
			if (not telk_alert_conf['use_ssl'] == True) and telk_alert_conf['use_http_auth'] == True:
				conn_es = Elasticsearch([telk_alert_conf['es_host']], 
										port = telk_alert_conf['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(telk_alert_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(telk_alert_conf['http_auth_pass']).decode('utf-8')),
										use_ssl = False)
			if telk_alert_conf['use_ssl'] == True and (not telk_alert_conf['use_http_auth'] == True):
				if not telk_alert_conf['valid_certificates'] == True:
					conn_es = Elasticsearch([telk_alert_conf['es_host']], 
											port = telk_alert_conf['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn=False)
			if telk_alert_conf['use_ssl'] == True and telk_alert_conf['use_http_auth'] == True:
				if not telk_alert_conf['valid_certificates'] == True:
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
				self.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.createLogAction("Connection established to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port'])))
				print("Connection established to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']) + '\n')
				self.logger.createLogTelkAlert("Connection established to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']), 2)
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
		except exceptions.AuthorizationException as exception:
			print("Unauthorized access. For more information see the application logs.")
			self.logger.createLogTelkAlert(str(exception), 4)
			sys.exit(1)
		except requests.exceptions.InvalidURL as exception:
			print(str(exception))
			self.logger.createLogTelkAlert(str(exception), 4)
			sys.exit(1)
	
	"""

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
						time_search = self.utils.convertTimeToMilliseconds(unit_time, rule_yaml['time_search'][unit_time])
					for unit_time in rule_yaml['time_back']:
						time_back = self.utils.convertTimeToMilliseconds(unit_time, rule_yaml['time_back'][unit_time])
					query_string_rule = rule_yaml['filter_search'][0]['query_string']['query']
					search_rule = Search(index = rule_yaml['index_name']).using(conn_es)
					search_rule = search_rule[0:int(telk_alert_conf['max_hits'])]
					query = Q("query_string", query = query_string_rule)
					while True:
						if rule_yaml['use_restriction_fields'] == True:
							search_aux = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : self.utils.convertDateToMilliseconds(datetime.now()) - time_back, 'lte' : self.utils.convertDateToMilliseconds(datetime.now()) } }).source(rule_yaml['fields'])
						else:
							search_aux = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : self.utils.convertDateToMilliseconds(datetime.now()) - time_back, 'lte' : self.utils.convertDateToMilliseconds(datetime.now()) } }).source(fields = None)
						if rule_yaml['restrict_by_host'] == True:
							a = A('terms', field = rule_yaml['field_hostname'])
							search_aux = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : self.utils.convertDateToMilliseconds(datetime.now()) - time_back, 'lte' : self.utils.convertDateToMilliseconds(datetime.now()) } }).source(fields = None)
							search_aux.aggs.bucket('events', a)
						result_search = search_aux.execute()
						total_events = 0
						for hit in result_search:
								total_events += 1
						if total_events >= rule_yaml['num_events']:
							print(str(total_events) + " events found in the rule: " + rule_yaml['name_rule'])
							self.logger.createLogTelkAlert(str(total_events) + " events found in the rule: " + rule_yaml['name_rule'], 2)
							self.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.createLogAction(str(total_events) + " events found in the rule: " + rule_yaml['name_rule']))
							if rule_yaml['restrict_by_host'] == True:
								for tag in result_search.aggregations.events.buckets:
									if int(tag.doc_count) >= rule_yaml['number_events_host']:
										print(str(tag.doc_count) + " events found in the host " + tag.key +  " in the rule: " + rule_yaml['name_rule'])
										self.logger.createLogTelkAlert(str(tag.doc_count) + " events found in the host " + tag.key + " in the rule: " + rule_yaml['name_rule'], 2)
										self.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.createLogAction(str(tag.doc_count) + " events found in the host " + tag.key +" in the rule: " + rule_yaml['name_rule']))
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
		except KeyError as exception:
			print("\nKey Error: " + str(exception) + '. For more information see the application logs.')
			self.logger.createLogTelkAlert("Key Error: " + str(exception), 4)
			sys.exit(1)
		except ValueError as exception:
			print("\nValue Error: " + str(exception))
			self.logger.createLogTelkAlert("Value Error: " + str(exception), 4)
			sys.exit(1)
		except TypeError as exception:
			print("\nType Error:" + str(exception) + ". For more information see the application logs.")
			self.logger.createLogTelkAlert("Type Error: " + str(exception), 4)
			sys.exit(1)

	"""
	Method that performs the multiple sending of alerts.

	Parameters:
	self --  An instantiated object of the Elastic class.
	result_search -- An object that contains the results of the ElasticSearch search.
	rule_yaml -- List containing all the data of the alert rule.
	flag_telegram -- Flag that indicates if the alert should be sent to telegram.
	time_back -- Backward time in milliseconds.

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
			print("Key Error: " + str(exception) + '. For more information see the application logs.')
			self.logger.createLogTelkAlert("Key error: " + str(exception), 4)
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
			print("Key Error: " + str(exception) + '. For more information see the application logs.')
			self.logger.createLogTelkAlert("Key error: " + str(exception), 4)
			sys.exit(1)

	"""
	Method that generates the JSON of the actions carried out in Telk-Alert that will be saved in ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	action -- Action performed.

	Return:
	log_json -- JSON object that contains the data that will be stored in ElasticSearch.
	"""
	def createLogAction(self, action):
		log_json = {
			'@timestamp' : datetime.utcnow(),
			'TELK.host.name' : self.host_name,
			'TELK.host.ip' : self.host_ip,
			'TELK.host.os.name' : self.host_os_name,
			'TELK.action' : action
		}
		return log_json

	"""
	Method that generates the JSON of the alert rules created so far.

	Parameters:
	self -- An instantiated object of the Elastic class.
	name_rule -- Name of the alert rule.
	status_rule -- State in which the rule is.

	Return:
	log_json -- JSON object that contains the data that will be stored in ElasticSearch.
	"""
	def createLogRules(self, name_rule, status_rule):
		log_json = {
			'@timestamp' : datetime.utcnow(),
			'TELK.host.name' : self.host_name,
			'TELK.host.ip' : self.host_ip,
			'TELK.host.os.name' : self.host_os_name,
			'RULE.name' : name_rule,
			'RULE.status' : status_rule
		}
		return log_json

	"""
	Method that generates the JSON of the alerts sent to Telegram.

	Parameters:
	self -- An instantiated object of the Elastic class.
	name_rule -- Name of the alert rule.
	total_events -- Total events found in the search.
	telegram_code -- HTTP code in response to the request made to Telegram.

	Return:
	log_json -- JSON object that contains the data that will be stored in ElasticSearch.
	"""
	def createLogAlertTelegram(self, name_rule, total_events, telegram_code):
		telegram_res = ""
		if telegram_code == 200:
			telegram_res = "Success"
		else:
			telegram_res = "Failed"
		log_json = {
			'@timestamp' : datetime.utcnow(),
			'TELK.host.name' : self.host_name,
			'TELK.host.ip' : self.host_ip,
			'TELK.host.os.name' : self.host_os_name,
			'RULE.name' : name_rule,
			'ALERT.events.total' : total_events,
			'ALERT.telegram.code': telegram_code,
			'ALERT.telegram.res' : telegram_res 
		}
		return log_json


	def createLogAlertEmail(self, name_rule, total_events, response):
		if len(response) == 0:
			response = "Success"
		log_json = {
			'@timestamp' : datetime.utcnow(),
			'TELK.host.name' : self.host_name,
			'TELK.host.ip' : self.host_ip,
			'TELK.host.os.name' : self.host_os_name,
			'RULE.name' : name_rule,
			'ALERT.events.total' : total_events,
			'ALERT.email.res': str(response)
		}
		return log_json

	"""
	Parameters:
	self -- An instantiated object of the Elastic class.
	index_name -- Name of the index that will be created in ElasticSearch and where the Telk-Alert logs will be stored.
	conn_es -- Object that contains the connection to ElasticSearch.
	log_json -- JSON object that contains the data that will be stored in ElasticSearch.
	"""
	def generateLogES(self, index_name, conn_es, log_json):
		index_name += "-" + datetime.now().strftime("%Y-%m-%d")
		conn_es.index(index = index_name, body = log_json)