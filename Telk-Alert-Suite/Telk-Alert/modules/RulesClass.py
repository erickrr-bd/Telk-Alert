import os
import sys
import glob
import threading
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger
from modules.ElasticClass import Elastic

"""
Class that allows managing alert rules.
"""
class Rules:
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores an object of type Logger.
	"""
	logger = None

	"""
	Property that stores an object of type Elastic.
	"""
	elastic = None

	"""
	Constructor for the Rules class.

	Parameters:
	self -- An instantiated object of the Rules class.
	"""
	def __init__(self):
		self.logger = Logger()
		self.utils = Utils()
		self.elastic = Elastic()

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
				self.logger.createLogTelkAlert(str(len(list_alert_rules)) + " alert rule(s) found in " + path_rules_folder, 2)
				self.elastic.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.elastic.createLogAction(str(len(list_alert_rules)) + " alert rule(s) found in " + path_rules_folder))
				print(str(len(list_alert_rules)) + " alert rule(s) found in " + path_rules_folder + '\n')	
				if len(list_alert_rules) != 0:
					for alert_rule in list_alert_rules:
						rule_yaml = self.utils.readFileYaml(path_rules_folder + '/' + alert_rule)
						self.logger.createLogTelkAlert("Rule " + alert_rule + ' loaded and executed', 2)
						self.elastic.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.elastic.createLogRules(alert_rule, 'loaded and executed'))
						print("Rule " + alert_rule + ' loaded and executed\n')
						thread_rule = threading.Thread(target = self.elastic.searchRuleElastic, args = (conn_es, rule_yaml, telk_alert_conf,)).start()
				else:
					self.logger.createLogTelkAlert("No alert rule(s) found in " + telk_alert_conf['rules_folder'], 3)
					self.elastic.generateLogES(telk_alert_conf['writeback_index'], conn_es, self.elastic.createLogAction("No alert rule(s) found in " + telk_alert_conf['rules_folder']))
					print("No alert rule(s) found in " + telk_alert_conf['rules_folder'])	
					sys.exit(1)
			except KeyError as exception:
				self.logger.createLogTelkAlert("Key Error: " + str(exception), 4)
				print("\nKey Error: " + str(exception))
				sys.exit(1)
			except TypeError as exception:
				self.logger.createLogTelkAlert(str(exception), 4)
				print("\nType Error: " + str(exception))
				sys.exit(1)
		else:
			self.logger.createLogTelkAlert("ElasticSearch version not supported by Telk-Alert", 4)
			print("\nElasticSearch version not supported by Telk-Alert.")
			sys.exit(1)

	"""
	Method that gets the names of all alert rules created in the directory.

	Parameters:
	self -- An instantiated object of the Rules class.
	path_folder_rules -- Directory where all alert rules are stored.

	Return:
	list_alert_rules -- List with the names of the alert rules stored in the directory.
	"""
	def getAllAlertRules(self, path_rules_folder):
		list_alert_rules = [os.path.basename(x) for x in glob.glob(path_rules_folder + '/*.yaml')]
		return list_alert_rules