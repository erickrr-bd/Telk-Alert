"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Title that is shown in the background of the application.
	"""
	BACKTITLE = "TELK-ALERT-TOOL"

	"""
	Absolute path of Telk-Alert.
	"""
	PATH_BASE_TELK_ALERT = "/etc/Telk-Alert-Suite/Telk-Alert"

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
	Options that are shown when a value is going to be modified in the Telk-Alert configuration.
	"""
	OPTIONS_FIELDS_UPDATE = [("Host", "ElasticSearch Host", 0),
							 ("Port", "ElasticSearch Port", 0),
							 ("Folder", "Rules Folder", 0),
							 ("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							 ("HTTP Authentication", "Enable or disable Http authentication", 0)]

	"""
	Options displayed when the use of SSL/TLS is enabled.
	"""
	OPTIONS_SSL_TLS_TRUE = [("Disable", "Disable SSL/TLS communication", 0),
							("Certificate Validation", "Modify certificate validation", 0)]

	"""
	Options displayed when the use of SSL/TLS is disabled.
	"""
	OPTIONS_SSL_TLS_FALSE = [("Enable", "Enable SSL/TLS communication", 0)]

	"""
	Options displayed when SSL certificate validation is enabled.
	"""
	OPTIONS_VALIDATE_CERTIFICATE_TRUE = [("Disable", "Disable certificate validation", 0),
								   		 ("Certificate File", "Change certificate file", 0)]

	"""
	Options displayed when SSL certificate validation is disabled.
	"""
	OPTIONS_VALIDATE_CERTIFICATE_FALSE = [("Enable", "Enable certificate validation", 0)]

	"""
	Options that are displayed when HTTP authentication is enabled.
	"""
	OPTIONS_HTTP_AUTHENTICATION_TRUE = [("Disable", "Disable HTTP Authentication", 0),
								 		("Data", "Modify HTTP Authentication data", 0)]

	"""
	Options that are displayed when HTTP authentication is disabled.
	"""
	OPTIONS_HTTP_AUTHENTICATION_FALSE = [("Enable", "Enable HTTP Authentication", 0)]

	"""
	Options that are displayed when the HTTP authentication credentials are to be modified.
	"""
	OPTIONS_HTTP_AUTHENTICATION_DATA = [("Username", "Username for HTTP Authentication", 0),
								 		("Password", "User password", 0)]