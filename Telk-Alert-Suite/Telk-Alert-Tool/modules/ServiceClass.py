import os
import io
from LoggerClass import Logger

"""
Class that allows you to manage everything related to the Telk-Alert service.
"""
class Service:

	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Method that allows starting the Telk-Alert service.

	Parameters:
	self -- Instance object.
	form_dialog -- A FormDialogs object.
	"""
	def startService(self, form_dialog):
		result = os.system("systemctl start telk_alert.service")
		if int(result) == 0:
			form_dialog.d.msgbox("\nService started", 7, 50, title = "Error message")
			self.logger.createLogTool("Service started", 2)
		if int(result) == 1280:
			form_dialog.d.msgbox("\nFailed to start telk_alert.service: Not found", 7, 50, title = "Error message")
			self.logger.createLogTool("Service Error: Failed to start telk_alert.service: Not found", 4)

	"""
	Method that allows restarting the Telk-Alert service.

	Parameters:
	self -- Instance object.
	form_dialog -- A FormDialogs object.
	"""
	def restartService(self, form_dialog):
		result = os.system("systemctl restart telk_alert.service")
		if int(result) == 0:
			form_dialog.d.msgbox("\nService restarted", 7, 50, title = "Error message")
			self.logger.createLogTool("Service restarted", 2)
		if int(result) == 1280:
			form_dialog.d.msgbox("\nFailed to restart telk_alert.service: Not found", 7, 50, title = "Error message")
			self.logger.createLogTool("Service Error: Failed to restart telk_alert.service: Not found", 4)

	"""
	Method to stop the Telk-Alert service.

	Parameters:
	self -- Instance object.
	form_dialog -- A FormDialogs object.
	"""
	def stopService(self, form_dialog):
		result = os.system("systemctl stop telk_alert.service")
		if int(result) == 0:
			form_dialog.d.msgbox("\nService stopped", 7, 50, title = "Error message")
			self.logger.createLogTool("Service stopped", 2)
		if int(result) == 1280:
			form_dialog.d.msgbox("\nFailed to stop telk_alert.service: Not found", 7, 50, title = "Error message")
			self.logger.createLogTool("Service Error: Failed to stop telk_alert.service: Not found", 4)

	"""
	Method that allows obtaining the status of the Telk-Alert service.

	Parameters:
	self -- Instance object.
	form_dialog -- A FormDialogs object.
	"""
	def getStatusService(self, form_dialog):
		if os.path.exists('/tmp/telk_alert.status'):
			os.remove('/tmp/telk_alert.status')
		os.system('(systemctl is-active --quiet telk_alert.service && echo "Telk-Alert service is running!" || echo "Telk-Alert service is not running!") >> /tmp/telk_alert.status')
		os.system('echo "Detailed service status:" >> /tmp/telk_alert.status')
		os.system('systemctl -l status telk_alert.service >> /tmp/telk_alert.status')
		with io.open('/tmp/telk_alert.status', 'r', encoding = 'utf-8') as file_status:
			form_dialog.getScrollBox(file_status.read(), title = "Status Service")
