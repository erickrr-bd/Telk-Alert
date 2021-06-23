import os
import io
import yaml
from datetime import datetime
from modules.UtilsClass import Utils

"""
Class that allows managing everything related to Telk-Alert-Agent.
"""
class Agent:
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Constructor for the Agent class.

	Parameters:
	self -- An instantiated object of the Agent class.
	"""
	def __init__(self):
		self.utils = Utils()
	
	"""
	Method that requests the data for the creation of the Telk-Alert-Agent configuration file.

	Parameters:
	self -- An instantiated object of the Agent class.
	form_dialog -- A FormDialogs class object.
	"""
	def createAgentConfiguration(self, form_dialog):
		now = datetime.now()
		data_agent_conf = []
		time_agent_one = form_dialog.getDataTime("Select the first time of service validation:", now.hour, now.minute)
		time_agent_two = form_dialog.getDataTime("Select the second time of service validation:", now.hour, now.minute)
		telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), form_dialog)
		telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"), form_dialog)
		data_agent_conf.append(time_agent_one)
		data_agent_conf.append(time_agent_two)
		data_agent_conf.append(telegram_bot_token)
		data_agent_conf.append(telegram_chat_id)
		self.createFileConfiguration(data_agent_conf, form_dialog)
		if not os.path.exists(self.utils.getPathTagent('conf') + '/agent_conf.yaml'):
			self.utils.createLogTool("Configuration file not created", 4)
			form_dialog.d.msgbox("\nConfiguration file not created", 7, 50, title = "Error message")
		else:
			self.utils.createLogTool("Configuration file created", 2)
			form_dialog.d.msgbox("\nConfiguration file created", 7, 50, title = "Notification message")
		form_dialog.mainMenu()

	"""
	Method that modifies one or more fields of the Telk-Alert-Agent configuration file.

	Parameters:
	self -- An instantiated object of the Agent class.
	form_dialog -- A FormDialogs class object.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	"""
	def modifyAgentConfiguration(self, form_dialog):
		options_agent_modify = [("First Time", "First time the service is validated", 0),
							   ("Second Time", "Second time the service is validated", 0),
							   ("Bot Token", "Telegram bot token", 0),
							   ("Chat ID", "Telegram chat id", 0)]

		flag_first_time = 0
		flag_second_time = 0
		flag_bot_token = 0
		flag_chat_id = 0
		opt_agent_modify = form_dialog.getDataCheckList("Select one or more options:", options_agent_modify, "Telk-Alert-Agent Configuration")
		for opt_agent in opt_agent_modify:
			if opt_agent == "First Time":
				flag_first_time = 1
			if opt_agent == "Second Time":
				flag_second_time = 1
			if opt_agent == "Bot Token":
				flag_bot_token = 1
			if opt_agent == "Chat ID":
				flag_chat_id = 1
		try:
			hash_origen = self.utils.getSha256File(self.utils.getPathTagent('conf') + '/agent_conf.yaml', form_dialog)
			with open(self.utils.getPathTagent('conf') + '/agent_conf.yaml') as file_agent_conf:
				data_agent_conf = yaml.safe_load(file_agent_conf)
			if flag_first_time == 1:
				time_actual_one = data_agent_conf['time_agent_one'].split(':')
				time_agent_one = form_dialog.getDataTime("Select the first time of service validation:", int(time_actual_one[0]), int(time_actual_one[1]))
				data_agent_conf['time_agent_one'] = str(time_agent_one[0]) + ':' + str(time_agent_one[1])
			if flag_second_time == 1:
				time_actual_two = data_agent_conf['time_agent_two'].split(':')
				time_agent_two = form_dialog.getDataTime("Select the second time of service validation:", int(time_actual_two[0]), int(time_actual_two[1]))
				data_agent_conf['time_agent_two'] = str(time_agent_two[0]) + ':' + str(time_agent_two[1])
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
		except OSError as exception:
			self.utils.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nError opening or modifying the configuration file. For more details, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()
		
	"""
	Method that starts the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the Agent class.
	form_dialog -- A FormDialogs class object.
	"""
	def startService(self, form_dialog):
		result = os.system("systemctl start telk-alert-agent.service")
		if int(result) == 0:
			self.utils.createLogTool("Telk-Alert-Agent service started", 2)
			form_dialog.d.msgbox("\nTelk-Alert-Agent service started", 7, 50, title = "Notification message")
		if int(result) == 1280:
			self.utils.createLogTool("Failed to start telk-alert-agent.service. Service not found.", 4)
			form_dialog.d.msgbox("\nFailed to start telk-alert-agent.service. Service not found.", 7, 50, title = "Error message")

	"""
	Method that restarts the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the Agent class.
	form_dialog -- A FormDialogs class object.
	"""
	def restartService(self, form_dialog):
		result = os.system("systemctl restart telk-alert-agent.service")
		if int(result) == 0:
			self.utils.createLogTool("Telk-Alert-Agent service restarted", 2)
			form_dialog.d.msgbox("\nTelk-Alert-Agent service restarted", 7, 50, title = "Notification message")	
		if int(result) == 1280:
			self.utils.createLogTool("Failed to restart telk-alert-agent.service. Service not found.", 4)
			form_dialog.d.msgbox("\nFailed to restart telk-alert-agent.service. Service not found.", 7, 50, title = "Error message")

	"""
	Method that stops the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the Agent class.
	form_dialog -- A FormDialogs class object.
	"""
	def stopService(self, form_dialog):
		result = os.system("systemctl stop telk-alert-agent.service")
		if int(result) == 0:
			self.utils.createLogTool("Telk-Alert-Agent service stopped", 2)
			form_dialog.d.msgbox("\nTelk-Alert-Agent service stopped", 7, 50, title = "Notification message")
		if int(result) == 1280:
			self.utils.createLogTool("Failed to stop telk-alert-agent.service. Service not found.", 4)
			form_dialog.d.msgbox("\nFailed to stop telk-alert-agent.service. Service not found.", 7, 50, title = "Error message")

	"""
	Method that obtains the status of the Telk-Alert-Agent service.

	Parameters:
	self -- An instantiated object of the Agent class.
	form_dialog -- A FormDialogs class object.
	"""
	def getStatusService(self, form_dialog):
		if os.path.exists('/tmp/telk_alert_agent.status'):
			os.remove('/tmp/telk_alert_agent.status')
		os.system('(systemctl is-active --quiet telk-alert-agent.service && echo "Telk-Alert Agent service is running!" || echo "Telk-Alert Agent service is not running!") >> /tmp/telk_alert_agent.status')
		os.system('echo "Detailed service status:" >> /tmp/telk_alert_agent.status')
		os.system('systemctl -l status telk-alert-agent.service >> /tmp/telk_alert_agent.status')
		with io.open('/tmp/telk_alert_agent.status', 'r', encoding = 'utf-8') as file_status:
			form_dialog.getScrollBox(file_status.read(), title = "Status Service")

	"""
	Method that creates the YAML file of the Telk-Alert-Agent configuration.

	Parameters:
	self -- An instantiated object of the Agent class.
	data_agent_conf -- List containing all the data entered to create the configuration file.
	form_dialog -- A FormDialogs class object.

	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	"""
	def createFileConfiguration(self, data_agent_conf, form_dialog):

		data_conf = {'time_agent_one': str(data_agent_conf[0][0]) + ':' + str(data_agent_conf[0][1]),
		'time_agent_two' : str(data_agent_conf[1][0]) + ':' + str(data_agent_conf[1][1]),
		'telegram_bot_token' : data_agent_conf[2].decode('utf-8'),
		'telegram_chat_id' : data_agent_conf[3].decode('utf-8')
		}

		try:
			with open(self.utils.getPathTagent('conf') + '/agent_conf.yaml', 'w') as agent_conf_file:
				yaml.dump(data_conf, agent_conf_file, default_flow_style = False)
			self.utils.changeUidGid(self.utils.getPathTagent('conf') + '/agent_conf.yaml')
		except OSError as exception:
			self.utils.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nError creating configuration file. For more details, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()