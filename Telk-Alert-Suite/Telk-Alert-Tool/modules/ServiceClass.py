from io import open as open_io
from os import system, path, remove
from modules.UtilsClass import Utils

"""
Class that allows you to manage everything related to the Telk-Alert service.
"""
class Service:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Property that stores an object of the FormDialog class.
	"""
	form_dialog = None

	"""
	Constructor for the Service class.

	Parameters:
	self -- An instantiated object of the Service class.
	form_dialog -- FormDialog class object.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)

	"""
	Method that starts the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def startService(self):
		result = system("systemctl start telk-alert.service")
		if int(result) == 0:
			self.utils.createTelkAlertToolLog("Telk-Alert service started", 1)
			self.form_dialog.d.msgbox(text = "\nTelk-Alert service started.", height = 7, width = 50, title = "Notification Message")
		if int(result) == 1280:
			self.utils.createTelkAlertToolLog("Failed to start telk-alert.service. Service not found.", 3)
			self.form_dialog.d.msgbox(text = "\nFailed to start telk-alert.service. Service not found.", height = 7, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that restarts the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def restartService(self):
		result = system("systemctl restart telk-alert.service")
		if int(result) == 0:
			self.utils.createTelkAlertToolLog("Telk-Alert service restarted", 1)
			self.form_dialog.d.msgbox(text = "\nTelk-Alert service restarted.", height = 7, width = 50, title = "Notification Message")
		if int(result) == 1280:
			self.utils.createTelkAlertToolLog("Failed to restart telk-alert.service. Service not found.", 3)
			self.form_dialog.d.msgbox(text = "\nFailed to restart telk-alert.service. Service not found.", height = 7, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that stops the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def stopService(self):
		result = system("systemctl stop telk-alert.service")
		if int(result) == 0:
			self.utils.createTelkAlertToolLog("Telk-Alert service stopped", 1)
			self.form_dialog.d.msgbox(text = "\nTelk-Alert service stopped.", height = 7, width = 50, title = "Notification Message")	
		if int(result) == 1280:
			self.utils.createTelkAlertToolLog("Failed to stop telk-alert.service: Service not found", 3)
			self.form_dialog.d.msgbox(text = "\nFailed to stop telk-alert.service. Service not found.", height = 7, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that obtains the status of the Telk-Alert service.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def getStatusService(self):
		if path.exists('/tmp/telk_alert.status'):
			remove('/tmp/telk_alert.status')
		system('(systemctl is-active --quiet telk-alert.service && echo "Telk-Alert service is running!" || echo "Telk-Alert service is not running!") >> /tmp/telk_alert.status')
		system('echo "Detailed service status:" >> /tmp/telk_alert.status')
		system('systemctl -l status telk-alert.service >> /tmp/telk_alert.status')
		with open_io('/tmp/telk_alert.status', 'r', encoding = 'utf-8') as file_status:
			self.form_dialog.getScrollBox(file_status.read(), title = "Status Service")
		self.form_dialog.mainMenu()