"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Absolute path of Telk-Alert.
	"""
	PATH_BASE_TELK_ALERT = "/etc/Telk-Alert-Suite/Telk-Alert"

	"""
	Absolute path of the Telk-Alert configuration file.
	"""
	PATH_FILE_CONFIGURATION = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert_conf.yaml"

	"""
	Absolute path of the Telk-Alert-Report configuration file.
	"""
	PATH_FILE_REPORT_CONFIGURATION = "/etc/Telk-Alert-Suite/Telk-Alert-Report/configuration/telk_alert_report_conf.yaml"

	"""
	Absolute path of the file where the key for the encryption/decryption process is stored.
	"""
	PATH_KEY_FILE = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/key"

	"""
	Absolute path of the application logs.
	"""
	NAME_FILE_LOG = "/var/log/Telk-Alert/telk-alert-log-"

	"""
	Name of the user created for the operation of the application.
	"""
	USER = "telk_alert"

	"""
	Name of the group created for the operation of the application.
	"""
	GROUP = "telk_alert"