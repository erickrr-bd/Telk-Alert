from io import open as open_io
from os import path, system, remove
from modules.UtilsClass import Utils

"""
Class that allows managing everything related to Telk-Alert-Agent.
"""
class Agent:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Property that stores an object of the FormDialog class.
	"""
	form_dialog = None

	"""
	Property that stores the path of the Telk-Alert-Agent configuration file.
	"""
	path_configuration_file = None

	"""
	Constructor for the Agent class.

	Parameters:
	self -- An instantiated object of the Agent class.
	form_dialog -- FormDialog class object.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		self.path_configuration_file = self.utils.getPathTelkAlertAgent('conf') + "/telk_alert_agent_conf.yaml"
	
	"""
	Method that requests the data for the creation of the Telk-Alert-Agent configuration file.

	Parameters:
	self -- An instantiated object of the Agent class.
	"""
	def createAgentConfiguration(self):
		data_agent_configuration = []
		time_execution_one = self.form_dialog.getDataTime("Select the first time of service validation:", -1, -1)
		data_agent_configuration.append(time_execution_one)
		time_execution_two = self.form_dialog.getDataTime("Select the second time of service validation:", -1, -1)
		data_agent_configuration.append(time_execution_two)
		telegram_bot_token = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
		data_agent_configuration.append(telegram_bot_token.decode('utf-8'))
		telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
		data_agent_configuration.append(telegram_chat_id.decode('utf-8'))
		self.createFileConfiguration(data_agent_configuration)
		if not path.exists(self.path_configuration_file):
			self.form_dialog.d.msgbox(text = "\nConfiguration file not created.", height = 7, width = 50, title = "Error Message")
		else:
			self.utils.createTelkAlertToolLog("Configuration file created", 1)
			self.form_dialog.d.msgbox(text = "\nConfiguration file created.", height = 7, width = 50, title = "Notification Message")
		self.form_dialog.mainMenu()

	"""
	Method that modifies one or more fields of the Telk-Alert-Agent configuration file.

	Parameters:
	self -- An instantiated object of the Agent class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def updateAgentConfiguration(self):
		list_fields_update_agent = [("First Time", "First time the service is validated", 0),
							    	("Second Time", "Second time the service is validated", 0),
							    	("Bot Token", "Telegram bot token", 0),
							    	("Chat ID", "Telegram chat id", 0)]

		flag_time_execution_one = 0
		flag_time_execution_two = 0
		flag_telegram_bot_token = 0
		flag_telegram_chat_id = 0
		options_fields_update_agent = self.form_dialog.getDataCheckList("Select one or more options:", list_fields_update_agent, "Configuration Fields")
		for option in options_fields_update_agent:
			if option == "First Time":
				flag_time_execution_one = 1
			elif option == "Second Time":
				flag_time_execution_two = 1
			elif option == "Bot Token":
				flag_telegram_bot_token = 1
			elif option == "Chat ID":
				flag_telegram_chat_id = 1
		try:
			hash_configuration_file_original = self.utils.getHashToFile(self.path_configuration_file)
			data_agent_configuration = self.utils.readYamlFile(self.path_configuration_file, 'rU')
			if flag_time_execution_one == 1:
				time_execution_one_actual = data_agent_configuration['time_execution_one'].split(':')
				time_execution_one = self.form_dialog.getDataTime("Select the first time of service validation:", int(time_execution_one_actual[0]), int(time_execution_one_actual[1]))
				data_agent_configuration['time_execution_one'] = str(time_execution_one[0]) + ':' + str(time_execution_one[1])
			if flag_time_execution_two == 1:
				time_actual_two = data_agent_conf['time_execution_two'].split(':')
				time_agent_two = form_dialog.getDataTime("Select the second time of service validation:", int(time_actual_two[0]), int(time_actual_two[1]))
				data_agent_conf['time_execution_two'] = str(time_agent_two[0]) + ':' + str(time_agent_two[1])
			if flag_bot_token == 1:
				telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", self.utils.decryptAES(data_agent_conf['telegram_bot_token'], form_dialog).decode('utf-8')), form_dialog)
				data_agent_conf['telegram_bot_token'] = telegram_bot_token.decode('utf-8')
			if flag_chat_id == 1:
				telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", self.utils.decryptAES(data_agent_conf['telegram_chat_id'], form_dialog).decode('utf-8')), form_dialog)
				data_agent_conf['telegram_chat_id'] = telegram_chat_id.decode('utf-8')
			with open(self.utils.getPathTagent('conf') + '/agent_conf.yaml', 'w') as file_agent_conf:
				yaml.safe_dump(data_agent_conf, file_agent_conf, default_flow_style = False)
			hash_modify = self.utils.getSha256File(self.utils.getPathTagent('conf') + '/agent_conf.yaml', form_dialog)
			if hash_origen == hash_modify:
				form_dialog.d.msgbox("\nConfiguration file not modified", 7, 50, title = "Notification message")
			else:
				self.utils.createLogTool("Modified configuration file", 2)
				form_dialog.d.msgbox("\nModified configuration file", 7, 50, title = "Notification message")
			form_dialog.mainMenu()
		except KeyError as exception:
			self.utils.createLogTool("Key not found in configuration file: " + str(exception), 4)
			form_dialog.d.msgbox("\nKey not found in configuration file: " + str(exception), 7, 50, title = "Error message")
			form_dialog.mainMenu()
		
	"""
	Method that starts the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the Agent class.
	"""
	def startService(self):
		result = system("systemctl start telk-alert-agent.service")
		if int(result) == 0:
			self.utils.createTelkAlertToolLog("Telk-Alert-Agent service started", 1)
			self.form_dialog.d.msgbox(text = "\nTelk-Alert-Agent service started.", height = 7, width = 50, title = "Notification Message")
		if int(result) == 1280:
			self.utils.createTelkAlertToolLog("Failed to start telk-alert-agent.service. Service not found.", 3)
			self.form_dialog.d.msgbox(text = "\nFailed to start telk-alert-agent.service. Service not found.", height = 7, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that restarts the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the Agent class.
	"""
	def restartService(self):
		result = system("systemctl restart telk-alert-agent.service")
		if int(result) == 0:
			self.utils.createTelkAlertToolLog("Telk-Alert-Agent service restarted", 1)
			self.form_dialog.d.msgbox(text = "\nTelk-Alert-Agent service restarted.", height = 7, width = 50, title = "Notification Message")	
		if int(result) == 1280:
			self.utils.createTelkAlertToolLog("Failed to restart telk-alert-agent.service. Service not found.", 3)
			self.form_dialog.d.msgbox(text = "\nFailed to restart telk-alert-agent.service. Service not found.", height = 7, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()
		
	"""
	Method that stops the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the Agent class.
	"""
	def stopService(self):
		result = system("systemctl stop telk-alert-agent.service")
		if int(result) == 0:
			self.utils.createTelkAlertToolLog("Telk-Alert-Agent service stopped", 1)
			self.form_dialog.d.msgbox(text = "\nTelk-Alert-Agent service stopped.", height = 7, width = 50, title = "Notification Message")
		if int(result) == 1280:
			self.utils.createTelkAlertToolLog("Failed to stop telk-alert-agent.service. Service not found.", 3)
			self.form_dialog.d.msgbox(text = "\nFailed to stop telk-alert-agent.service. Service not found.", height = 7, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that obtains the status of the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the Agent class.
	"""
	def getStatusService(self, form_dialog):
		if path.exists('/tmp/telk_alert_agent.status'):
			remove('/tmp/telk_alert_agent.status')
		system('(systemctl is-active --quiet telk-alert-agent.service && echo "Telk-Alert Agent service is running!" || echo "Telk-Alert Agent service is not running!") >> /tmp/telk_alert_agent.status')
		system('echo "Detailed service status:" >> /tmp/telk_alert_agent.status')
		system('systemctl -l status telk-alert-agent.service >> /tmp/telk_alert_agent.status')
		with open_io('/tmp/telk_alert_agent.status', 'r', encoding = 'utf-8') as file_status:
			self.form_dialog.getScrollBox(file_status.read(), title = "Status Service")
		self.form_dialog.mainMenu()
		
	"""
	Method that creates the YAML file of the Telk-Alert-Agent configuration.

	Parameters:
	self -- An instantiated object of the Agent class.
	data_agent_configuration -- Object that stores the data that will be saved in the Telk-Alert-Agent configuration file.
	"""
	def createFileConfiguration(self, data_agent_configuration):

		data_json_agent = {'time_execution_one': str(data_agent_configuration[0][0]) + ':' + str(data_agent_configuration[0][1]),
					 	   'time_execution_two' : str(data_agent_configuration[1][0]) + ':' + str(data_agent_configuration[1][1]),
						   'telegram_bot_token' : data_agent_configuration[2],
		  			 	   'telegram_chat_id' : data_agent_configuration[3]}

		self.utils.createYamlFile(data_json_agent, self.path_configuration_file, 'w')