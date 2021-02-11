import os
import sys
import glob
import threading
sys.path.append('./modules')
from UtilsClass import Utils
from LoggerClass import Logger
from ElasticClass import Elastic

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

	def readAllAlertRules(self):
		print("Telk-Alert started ...\n")
		print("Author: Erick Rodriguez erickrr.tbd93@gmail.com\n")
		print("License: GPLv3\n")
		try:
			telk_alert_conf = self.utils.readFileYaml(self.utils.getPathTalert('conf') + '/es_conf.yaml')
			path_rules_folder = self.utils.getPathTalert(telk_alert_conf['rules_folder'])
			list_alert_rules = self.getAllAlertRules(path_rules_folder)
			print(str(len(list_alert_rules)) + " alert rule(s) found in " + path_rules_folder + '\n')
			if len(list_alert_rules) != 0:
				for alert_rule in list_alert_rules:
					rule_yaml = self.utils.readFileYaml(path_rules_folder + '/' + alert_rule)
					print("Rule " + alert_rule + ' loaded and executed\n')
					thread_rule = threading.Thread(target = self.createRule, args = (rule_yaml, telk_alert_conf, )).start()
			else:
				print("No alert rule found in directory.")
				self.logger.createLogTelkAlert("No alert rule found in directory.", 3)
				sys.exit(1)
		except (TypeError, KeyError) as exception:
			self.logger.createLogTelkAlert("Error: " + str(exception), 4)
			sys.exit(1)


	def createRule(self, rule_yaml, telk_alert_conf):
		self.elastic.getConnectionElastic(telk_alert_conf)

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