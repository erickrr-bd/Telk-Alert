import yaml
import json
import os
import sys
sys.path.append('./modules')
from UtilsClass import Utils
from LoggerClass import Logger

class Configuration:

	utils = Utils()

	def createFileConfiguration(self, data_conf):
		d = {'es_version': str(data_conf[0]),
			'es_host': str(data_conf[1]),
			'es_port': int(data_conf[2]),
			'rules_folder': str(data_conf[3]),
			'use_ssl': json.loads(str(data_conf[4]).lower()),
			'use_http_auth': json.loads(str(data_conf[5]).lower())}
		if data_conf[5] == True:
			http_auth_data = {'http_auth_user' : data_conf[6].decode("utf-8"), 'http_auth_pass' : data_conf[7].decode("utf-8")}
			data_aux = {'writeback_index' : str(data_conf[8]), 'max_hits' : int(data_conf[9])}
			d.update(http_auth_data)
		else:
			data_aux = {'writeback_index' : str(data_conf[6]), 'max_hits' : int(data_conf[7])}
		d.update(data_aux)
		try:
			if(not os.path.isdir(self.utils.getPathTalert(str(data_conf[3])))):
			 os.mkdir(self.utils.getPathTalert(str(data_conf[3])))
			with open(self.utils.getPathTalert('conf') + '/es_conf.yaml', 'w') as yaml_file:
				yaml.dump(d, yaml_file, default_flow_style = False)
			#Utils.changeUidGid(Utils.getPathTalert('conf') + '/es_conf.yaml')
			#Utils.changeUidGid(Utils.getPathTalert(str(data_conf[3])))
		except OSError as exception:
			Logger.createLogTool("Error" + str(exception), 4)