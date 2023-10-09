"""
Class that manages the constant values of Telk-Alert.
"""
class Constants:
	"""
	Telk-Alert absolute path.
	"""
	TELK_ALERT_PATH = "/etc/Telk-Alert-Suite/Telk-Alert"

	"""
	Absolute path of the Telk-Alert configuration file.
	"""
	TELK_ALERT_CONFIGURATION_FILE_PATH = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert_conf.yaml"

	"""
	Absolute path of the file where the encryption key is stored.
	"""
	KEY_FILE_PATH = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/key"

	"""
	Absolute path of the SSL certificate.
	"""
	CERTIFICATE_FILE_PATH = "/etc/Telk-Alert-Suite/Telk-Alert/certificates"

	"""
	Absolute path of the Telk-Alert-Tool log file.
	"""
	LOG_FILE_NAME = "/var/log/Telk-Alert/telk-alert-log-"

	"""
	Owner user of the application files.
	"""
	USER = "telk_alert"

	"""
	Owner group of the application files.
	"""
	GROUP = "telk_alert"