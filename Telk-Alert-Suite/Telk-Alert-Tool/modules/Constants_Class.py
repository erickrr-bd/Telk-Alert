"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Title that is shown in the background of the application.
	"""
	BACKTITLE = "TELK-ALERT-TOOL"

	"""
	Absolute path of the Telk-Alert configuration file.
	"""
	PATH_FILE_CONFIGURATION = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert_conf.yaml"

	"""
	Absolute path of the file where the key for the encryption/decryption process is stored.
	"""
	PATH_KEY_FILE = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/key"

	"""
	Absolute path of the application logs.
	"""
	NAME_FILE_LOG = "/var/log/Telk-Alert/telk-alert-tool-log-"

	"""
	Name of the application logs.
	"""
	NAME_LOG = "TELK_ALERT_TOOL_LOG"

	"""
	Name of the user created for the operation of the application.
	"""
	USER = "telk_alert"

	"""
	Name of the group created for the operation of the application.
	"""
	GROUP = "telk_alert"

	"""
	Options displayed in the main menu.
	"""
	OPTIONS_MAIN_MENU = [("1", "Telk-Alert Configuration"),
					     ("2", "Alert Rules"),
					     ("3", "Telk-Alert Service"),
					     ("4", "Telk-Alert Agent"),
					     ("5", "About"),
					     ("6", "Exit")]

	"""
	Options that are shown when the configuration file does not exist.
	"""
	OPTIONS_CONFIGURATION_FALSE = [("Create", "Create the configuration file", 0)]

	"""
	Options that are shown when the configuration file exists.
	"""
	OPTIONS_CONFIGURATION_TRUE = [("Modify", "Modify the configuration file", 0)]

	"""
	Options that are shown when a value is going to be modified in the VulTek-Alert configuration.
	"""
	OPTIONS_FIELDS_UPDATE = [("Time", "Time execution", 0),
							 ("Level", "Vulnerability level", 0),
							 ("Bot Token", "Telegram Bot Token", 0),
							 ("Chat ID", "Telegram channel identifier", 0)]

	"""
	Options displayed in the service menu.
	"""
	OPTIONS_SERVICE_MENU = [("1", "Start Service"),
				            ("2", "Restart Service"),
				            ("3", "Stop Service"),
				            ("4", "Service Status")]

	"""
	Options that show the level of criticality of the vulnerabilities.
	"""
	OPTIONS_LEVEL_VULNERABILITIES = [["low", "Low level vulnerability", 0],
								     ["moderate", "Medium level vulnerability", 0],
								     ["important", "Important level vulnerability", 0],
								     ["critical", "Critical level vulnerability", 0]]