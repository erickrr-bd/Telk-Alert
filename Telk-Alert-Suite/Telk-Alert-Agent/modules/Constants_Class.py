"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Absolute path of the Telk-Alert-Agent configuration file.
	"""
	PATH_FILE_AGENT_CONFIGURATION = "/etc/Telk-Alert-Suite/Telk-Alert-Agent/configuration/telk_alert_agent_conf.yaml"

	"""
	Absolute path of the file where the key for the encryption/decryption process is stored.
	"""
	PATH_KEY_FILE = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/key"

	"""
	Absolute path of the application logs.
	"""
	NAME_FILE_LOG = "/var/log/Telk-Alert/telk-alert-agent-log-"

	"""
	Name of the user created for the operation of the application.
	"""
	USER = "telk_alert"

	"""
	Name of the group created for the operation of the application.
	"""
	GROUP = "telk_alert"