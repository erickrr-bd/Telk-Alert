"""
Class that manages the constant values of Telk-Alert-Agent.
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
	Absolute path of the Telk-Alert-Agent configuration file.
	"""
	TELK_ALERT_AGENT_CONFIGURATION_FILE_PATH = "/etc/Telk-Alert-Suite/Telk-Alert-Agent/configuration/telk_alert_agent_conf.yaml"

	"""
	Absolute path of the file where the encryption key is stored.
	"""
	KEY_FILE_PATH = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/key"

	"""
	Absolute path of the Telk-Alert-Agent log file.
	"""
	LOG_FILE_NAME = "/var/log/Telk-Alert/telk-alert-agent-log-"

	"""
	Owner user of the application files.
	"""
	USER = "telk_alert"

	"""
	Owner group of the application files.
	"""
	GROUP = "telk_alert"