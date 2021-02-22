import os
import sys
import glob
import threading
#sys.path.append('./modules')
from modules.LoggerClass import Logger
from modules.UtilsClass import Utils
from modules.ElasticClass import Elastic

"""
Class that allows managing alert rules.
"""
class Rules:

	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Elastic type object.
	"""
	elastic = Elastic()

	"""
	A method that reads all the alert rules created and creates the threads to perform ElasticSearch searches.

	Parameters:
	self -- An instantiated object of the Rules class.

	Exceptions:
	TypeError -- The TypeError is thrown when an operation or function is applied to an object of an inappropriate type.
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def readAllAlertRules(self):
		telk_alert_conf = self.utils.readFileYaml(self.utils.getPathTalert('conf') + '/es_conf.yaml')
		if float(telk_alert_conf['es_version']) >= 7.0:
			print("Telk-Alert v3.0\n")
			print("@2021 Tekium. All rights reserved.\n")
			print("Author: Erick Rodriguez erickrr.tbd93@gmail.com\n")
			print("License: GPLv3\n")
			print("\nTelk-Alert started...")
			try:
				conn_es = self.elastic.getConnectionElastic(telk_alert_conf)
				path_rules_folder = self.utils.getPathTalert(telk_alert_conf['rules_folder'])
				list_alert_rules = self.getAllAlertRules(path_rules_folder)
				print("ALERT RULES DATA\n")
				print(str(len(list_alert_rules)) + " alert rule(s) found in " + path_rules_folder + '\n')
				self.elastic.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.elastic.createLogAction(str(len(list_alert_rules)) + " alert rule(s) found in " + path_rules_folder))
				self.logger.createLogTelkAlert(str(len(list_alert_rules)) + " alert rule(s) found in " + path_rules_folder, 2)
				if len(list_alert_rules) != 0:
					for alert_rule in list_alert_rules:
						rule_yaml = self.utils.readFileYaml(path_rules_folder + '/' + alert_rule)
						print("Rule " + alert_rule + ' loaded and executed\n')
						self.elastic.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.elastic.createLogRules(alert_rule, 'loaded and executed'))
						self.logger.createLogTelkAlert("Rule " + alert_rule + ' loaded and executed', 2)
						thread_rule = threading.Thread(target = self.elastic.searchRuleElastic, args = (conn_es, rule_yaml, telk_alert_conf,)).start()
				else:
					print("No alert rule found in directory.")
					self.elastic.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.elastic.createLogAction("No alert rule found in directory"))
					self.logger.createLogTelkAlert("No alert rule found in directory.", 3)
					sys.exit(1)
			except KeyError as exception:
				print("\nKey Error: " + str(exception))
				self.logger.createLogTelkAlert("Key Error: " + str(exception), 4)
				sys.exit(1)
			except TypeError as exception:
				print("\nType Error: " + str(exception))
				self.logger.createLogTelkAlert("Type Error: " + str(exception), 4)
				sys.exit(1)
		else:
			print("ElasticSearch version not supported.")
			self.logger.createLogTelkAlert("ElasticSearch version not supported.", 4)
			sys.exit(1)

	"""
	Method that allows to obtain all the alert rules saved in a directory.

	Parameters:
	self -- An instantiated object of the Rules class.
	path_folder_rules -- Directory where all alert rules are stored.

	Return:
	list_alert_rules -- List with the names of the alert rules stored in the directory.
	"""
	def getAllAlertRules(self, path_rules_folder):
		list_alert_rules = [os.path.basename(x) for x in glob.glob(path_rules_folder + '/*.yaml')]
		return list_alert_rules