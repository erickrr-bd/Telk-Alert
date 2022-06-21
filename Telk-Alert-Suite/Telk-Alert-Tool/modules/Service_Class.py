from libPyLog import libPyLog
from io import open as open_io
from os import system, path, remove
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related with the Telk-Alert service.
"""
class Service:
	"""
	Attribute that stores an object of the libPyDialog class.
	"""
	__dialog = None

	"""
	Attribute that stores an object of the libPyLog class.
	"""
	__logger = None

	"""
	Attribute that stores an object of the Constants class.
	"""
	__constants = None

	"""
	Attribute that stores the method to be called when the user chooses the cancel option.
	"""
	__action_to_cancel = None


	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel: Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__constants = Constants()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def startTelkAlertService(self):
		"""
		Method that starts the Telk-Alert service.
		"""
		result = system("systemctl start telk-alert.service")
		if int(result) == 0:
			self.__dialog.createMessageDialog("\nTelk-Alert service started.", 7, 50, "Notification Message")
			self.__logger.generateApplicationLog("Telk-Alert service started", 1, "__TelkAlertService", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif int(result) == 1280:
			self.__dialog.createMessageDialog("\nFailed to start telk-alert.service. Service not found.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog("Failed to start telk-alert.service. Service not found.", 3, "__TelkAlertService", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		self.__action_to_cancel()


	def restartTelkAlertService(self):
		"""
		Method that restarts the Telk-Alert service.
		"""
		result = system("systemctl restart telk-alert.service")
		if int(result) == 0:
			self.__dialog.createMessageDialog("\nTelk-Alert service restarted.", 7, 50, "Notification Message")
			self.__logger.generateApplicationLog("Telk-Alert service restarted", 1, "__TelkAlertService", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif int(result) == 1280:
			self.__dialog.createMessageDialog("\nFailed to restart telk-alert.service. Service not found.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog("Failed to restart telk-alert.service. Service not found.", 3, "__TelkAlertService", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		self.__action_to_cancel()


	def stopTelkAlertService(self):
		"""
		Method that stops the Telk-Alert service.
		"""
		result = system("systemctl stop telk-alert.service")
		if int(result) == 0:
			self.__dialog.createMessageDialog("\nTelk-Alert service stopped.", 7, 50, "Notification Message")
			self.__logger.generateApplicationLog("Telk-Alert service stopped", 1, "__TelkAlertService", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif int(result) == 1280:
			self.__dialog.createMessageDialog("\nFailed to stop telk-alert.service. Service not found.", 8, 50, "Notification Message")
			self.__logger.generateApplicationLog("Failed to stop telk-alert.service. Service not found.", 3, "__TelkAlertService", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		self.__action_to_cancel()


	def getStatusTelkAlertService(self):
		"""
		Method that obtains the status of the Telk-Alert service.
		"""
		if path.exists('/tmp/telk_alert.status'):
			remove('/tmp/telk_alert.status')
		system('(systemctl is-active --quiet telk-alert.service && echo "Telk-Alert service is running!" || echo "Telk-Alert service is not running!") >> /tmp/telk_alert.status')
		system('echo "Detailed service status:" >> /tmp/telk_alert.status')
		system('systemctl -l status telk-alert.service >> /tmp/telk_alert.status')
		with open_io('/tmp/telk_alert.status', 'r', encoding = 'utf-8') as file_status:
			self.__dialog.createScrollBoxDialog(file_status.read(), 18, 70, "Telk-Alert Service")
		self.__action_to_cancel()