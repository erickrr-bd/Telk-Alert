import sys
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch_dsl import Q, Search
sys.path.append('./modules')
from UtilsClass import Utils

class Elastic:

	utils = Utils()

	def getConnectionElastic(self, telk_alert_conf):
		if telk_alert_conf['use_ssl'] and telk_alert_conf['use_http_auth']:
			if not telk_alert_conf['valid_certificates']:
				conn_es = Elasticsearch([telk_alert_conf['es_host']], 
										port = telk_alert_conf['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(telk_alert_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(telk_alert_conf['http_auth_pass']).decode('utf-8')),
										use_ssl = True,
										verify_certs = False)
				print(conn_es.info()) 
