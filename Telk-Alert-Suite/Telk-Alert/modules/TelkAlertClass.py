from os import path
from sys import exit
from glob import glob
from threading import Thread
from modules.UtilsClass import Utils
from modules.ElasticClass import Elastic

"""
Class that manages the start of the application.
"""
class TelkAlert:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Constructor for the TelkAlert class.

	Parameters:
	self -- An instantiated object of the TelkAlert class.
	"""
	def __init__(self):
		self.utils = Utils()

	"""
	Method that starts the Telk-Alert application.

	Parameters:
	self -- An instantiated object of the TelkAlert class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def startTelkAlert(self):
		path_configuration_file = self.utils.getPathTelkAlert("conf") + "/telk_alert_conf.yaml"
		if path.exists(path_configuration_file):
			telk_alert_configuration = self.utils.readYamlFile(path_configuration_file, 'r')
			try:
				if float(telk_alert_configuration['es_version']) >= 7.0 and float(telk_alert_configuration['es_version']) <= 7.16:
					self.utils.createTelkAlertLog("Telk-Alert v3.1", 1)
					self.utils.createTelkAlertLog("@2022 Tekium. All rights reserved.", 1)
					self.utils.createTelkAlertLog("Author: Erick Rodriguez", 1)
					self.utils.createTelkAlertLog("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com", 1)
					self.utils.createTelkAlertLog("License: GPLv3", 1)
					self.utils.createTelkAlertLog("Telk-Alert started...", 1)
					path_folder_rules = self.utils.getPathTelkAlert(telk_alert_configuration['name_folder_rules'])
					list_all_alert_rules = self.getAllAlertRules(path_folder_rules)
					if len(list_all_alert_rules) == 0:
						self.utils.createTelkAlertLog("No alert rules found in directory: " + path_folder_rules, 2)
					else:
						elastic = Elastic()
						conn_es = elastic.getConnectionElastic(telk_alert_configuration)
						self.utils.createTelkAlertLog(str(len(list_all_alert_rules)) + " alert rules found in directory: " + path_folder_rules, 1)
						for alert_rule in list_all_alert_rules:
							alert_rule_data = self.utils.readYamlFile(path_folder_rules + '/' + alert_rule, 'r')
							self.utils.createTelkAlertLog(alert_rule + " loaded.", 1)
							Thread(target = elastic.executionRule, args = (alert_rule_data, conn_es, )).start()
				else:
					self.utils.createTelkAlertLog("ElasticSearch version not supported by Telk-Alert.", 3)
					exit(1)
			except KeyError as exception:
				self.utils.createTelkAlertLog("Error starting Telk-Alert. For more information, see the logs.", 3)
				self.utils.createTelkAlertLog("Key Error: " + str(exception), 3)
				exit(1)
		else:
			self.utils.createTelkAlertLog("Configuration file not found.", 3)
			exit(1)

	"""
	Method that gets the names of all alert rules created in the directory.

	Parameters:
	self -- An instantiated object of the TelkAlert class.
	path_folder_rules -- Directory where all alert rules are stored.

	Return:
	list_alert_rules -- List with the names of the alert rules stored in the directory.
	"""
	def getAllAlertRules(self, path_rules_folder):
		list_all_alert_rules = [path.basename(x) for x in glob(path_rules_folder + '/*.yaml')]
		return list_all_alert_rules