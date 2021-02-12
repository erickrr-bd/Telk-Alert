import sys
import time
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions
from elasticsearch_dsl import Q, Search
sys.path.append('./modules')
from UtilsClass import Utils
from LoggerClass import Logger
from TelegramClass import Telegram

class Elastic:

	utils = Utils()
	logger = Logger()
	telegram = Telegram()

	def getConnectionElastic(self, telk_alert_conf):
		if (not telk_alert_conf['use_ssl']) and (not telk_alert_conf['use_http_auth']):
			try:
				conn_es = Elasticsearch([telk_alert_conf['es_host']], 
										port = telk_alert_conf['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
				print("Cluster name: " + conn_es.info()['cluster_name'])
				if conn_es.ping():
					print("\nConnection established to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']))
				return conn_es
			except exceptions.ConnectionError as exception:
				print("\nFailed connection to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']))
				self.logger.createLogTelkAlert(str(exception), 4)
				sys.exit(1)
		if (not telk_alert_conf['use_ssl']) and telk_alert_conf['use_http_auth']:
			try:
				conn_es = Elasticsearch([telk_alert_conf['es_host']], 
										port = telk_alert_conf['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(telk_alert_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(telk_alert_conf['http_auth_pass']).decode('utf-8')),
										use_ssl = False)
				print("Cluster name: " + conn_es.info()['cluster_name'])
				if conn_es.ping():
					print("\nConnection established to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']))
				return conn_es
			except exceptions.ConnectionError as exception:
				print("\nFailed connection to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']))
				self.logger.createLogTelkAlert(str(exception), 4)
				sys.exit(1)
			except exceptions.AuthenticationException as exception:
				print("\nHTTP authentication failed")
				self.logger.createLogTelkAlert(str(exception), 4)
				sys.exit(1)
		if telk_alert_conf['use_ssl'] and (not telk_alert_conf['use_http_auth']):
			if not telk_alert_conf['valid_certificates']:
				try:
					conn_es = Elasticsearch([telk_alert_conf['es_host']], 
											port = telk_alert_conf['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn=False)
					print("Cluster name: " + conn_es.info()['cluster_name'])
					if conn_es.ping():
						print("\nConnection established to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']))
					return conn_es
				except exceptions.ConnectionError as exception:
					print("\nFailed connection to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']))
					self.logger.createLogTelkAlert(str(exception), 4)
					sys.exit(1)
		if telk_alert_conf['use_ssl'] and telk_alert_conf['use_http_auth']:
			if not telk_alert_conf['valid_certificates']:
				try:
					conn_es = Elasticsearch([telk_alert_conf['es_host']], 
											port = telk_alert_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(telk_alert_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(telk_alert_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn=False)
					print("Cluster name: " + conn_es.info()['cluster_name'])
					if conn_es.ping():
						print("\nConnection established to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']))
					return conn_es
				except exceptions.ConnectionError as exception:
					print("\nFailed connection to: " + telk_alert_conf['es_host'] + ':' + str(telk_alert_conf['es_port']))
					self.logger.createLogTelkAlert(str(exception), 4)
					sys.exit(1)
				except exceptions.AuthenticationException as exception:
					print("\nHTTP authentication failed")
					self.logger.createLogTelkAlert(str(exception), 4)
					sys.exit(1)


	def searchRuleElastic(self, conn_es, rule_yaml):
		try:
			if conn_es.indices.exists(index = rule_yaml['index_name']):
				if rule_yaml['type_alert'] == 'Frequency':
					for unit_time in rule_yaml['time_search']:
						time_search = self.utils.convertTimeToMilliseconds(unit_time, rule_yaml['time_search'][unit_time])
					for unit_time in rule_yaml['time_back']:
						time_back = self.utils.convertTimeToMilliseconds(unit_time, rule_yaml['time_back'][unit_time])
					query_string_rule = rule_yaml['filter_search'][0]['query_string']['query']
					search_rule = Search(index = rule_yaml['index_name']).using(conn_es)
					search_rule = search_rule[0:int(10000)]
					query = Q("query_string", query = query_string_rule)
					while True:
						if not rule_yaml['restrict_by_host']:
							if rule_yaml['use_restriction_fields']:
								result_search = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : self.utils.convertDateToMilliseconds(datetime.now()) - time_back, 'lte' : self.utils.convertDateToMilliseconds(datetime.now()) } }).source(rule_yaml['fields'])
							else:
								result_search = search_rule.query(query).query('range', ** { '@timestamp' : { 'gte' : self.utils.convertDateToMilliseconds(datetime.now()) - time_back, 'lte' : self.utils.convertDateToMilliseconds(datetime.now()) } })
							message_telegram = self.telegram.getTelegramHeader(rule_yaml, time_back)
							for hit in result_search:
								message_telegram += self.telegram.getTelegramMessage(hit)
							print(message_telegram)
						time.sleep(time_search)
		except KeyError as exception:
			print("Key Error: " + str(exception))
			sys.exit(1)