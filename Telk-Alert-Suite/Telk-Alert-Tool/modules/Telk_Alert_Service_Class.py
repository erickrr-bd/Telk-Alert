from io import open
from os import system
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages the Telk-Alert service.
"""
class TelkAlertService:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def start_service(self):
		"""
		Method that starts the Telk-Alert service.
		"""
		try:
			command_result = system("systemctl start telk-alert.service")
			if int(command_result) == 0:
				self.dialog.createMessageDialog("\nTelk-Alert service started.", 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Telk-Alert service started", 1, "__serviceTelkAlert", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.createMessageDialog("\nError starting Telk-Alert service. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__serviceTelkAlert", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error")


	def restart_service(self):
		"""
		Method that restarts the Telk-Alert service.
		"""
		try:
			command_result = system("systemctl restart telk-alert.service")
			if int(command_result) == 0:
				self.dialog.createMessageDialog("\nTelk-Alert service restarted.", 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Telk-Alert service restarted", 1, "__serviceTelkAlert", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.createMessageDialog("\nError restarting Telk-Alert service. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__serviceTelkAlert", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error")


	def stop_service(self):
		"""
		Method that stops the Telk-Alert service.
		"""
		try:
			command_result = system("systemctl stop telk-alert.service")
			if int(command_result) == 0:
				self.dialog.createMessageDialog("\nTelk-Alert service stopped.", 7, 50, "Notification Message")
				self.logger.generateApplicationLog("Telk-Alert service stopped", 2, "__serviceTelkAlert", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.createMessageDialog("\nError stopping Telk-Alert service. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__serviceTelkAlert", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error")


	def get_service_status(self):
		"""
		Method that obtains and displays the current status of the Telk-Alert service.
		"""
		try:
			self.utils.deleteFile("/tmp/telk_alert.status")
			system('(systemctl is-active --quiet telk-alert.service && echo "Telk-Alert service is running!" || echo "Telk-Alert service is not running!") >> /tmp/telk_alert.status')
			system('echo "Detailed service status:" >> /tmp/telk_alert.status')
			system("systemctl -l status telk-alert.service >> /tmp/telk_alert.status")
			with open("/tmp/telk_alert.status", 'r', encoding = "utf-8") as service_status_file:
				self.dialog.createScrollBoxDialog(service_status_file.read(), 18, 70, "Telk-Alert Service")
		except Exception as exception:
			self.dialog.createMessageDialog("\nError obtaining Telk-Alert service status. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.generateApplicationLog(exception, 3, "__serviceTelkAlert", use_file_handler = True, log_file_name = self.constants.LOG_FILE_NAME, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error")