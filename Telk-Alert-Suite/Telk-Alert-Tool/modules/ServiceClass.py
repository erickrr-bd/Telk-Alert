import os
import io
from modules.LoggerClass import Logger

"""
Class that allows you to manage everything related to the Telk-Alert service.
"""
class Service:
	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Method that starts the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the Service class.
	form_dialog -- A FormDialogs class object.
	"""
	def startService(self, form_dialog):
		result = os.system("systemctl start telk-alert.service")
		if int(result) == 0:
			self.logger.createLogTool("Telk-Alert service started", 2)
			form_dialog.d.msgbox("\nTelk-Alert service started", 7, 50, title = "Notification message")
		if int(result) == 1280:
			self.logger.createLogTool("Failed to start telk-alert.service. Service not found.", 4)
			form_dialog.d.msgbox("\nFailed to start telk-alert.service. Service not found.", 7, 50, title = "Error message")
			
	"""
	Method that restarts the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the Service class.
	form_dialog -- A FormDialogs class object.
	"""
	def restartService(self, form_dialog):
		result = os.system("systemctl restart telk-alert.service")
		if int(result) == 0:
			self.logger.createLogTool("Telk-Alert service restarted", 2)
			form_dialog.d.msgbox("\nTelk-Alert service restarted", 7, 50, title = "Notification message")
		if int(result) == 1280:
			self.logger.createLogTool("Failed to restart telk-alert.service. Service not found.", 4)
			form_dialog.d.msgbox("\nFailed to restart telk-alert.service. Service not found", 7, 50, title = "Error message")

	"""
	Method that stops the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the Service class.
	form_dialog -- A FormDialogs class object.
	"""
	def stopService(self, form_dialog):
		result = os.system("systemctl stop telk-alert.service")
		if int(result) == 0:
			self.logger.createLogTool("Telk-Alert service stopped", 2)
			form_dialog.d.msgbox("\nTelk-Alert service stopped", 7, 50, title = "Notification message")	
		if int(result) == 1280:
			self.logger.createLogTool("Failed to stop telk-alert.service: Service not found", 4)
			form_dialog.d.msgbox("\nFailed to stop telk-alert.service. Service not found.", 7, 50, title = "Error message")

	"""
	Method that obtains the status of the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the Service class.
	form_dialog -- A FormDialogs class object.
	"""
	def getStatusService(self, form_dialog):
		if os.path.exists('/tmp/telk_alert.status'):
			os.remove('/tmp/telk_alert.status')
		os.system('(systemctl is-active --quiet telk-alert.service && echo "Telk-Alert service is running!" || echo "Telk-Alert service is not running!") >> /tmp/telk_alert.status')
		os.system('echo "Detailed service status:" >> /tmp/telk_alert.status')
		os.system('systemctl -l status telk-alert.service >> /tmp/telk_alert.status')
		with io.open('/tmp/telk_alert.status', 'r', encoding = 'utf-8') as file_status:
			form_dialog.getScrollBox(file_status.read(), title = "Status Service")
