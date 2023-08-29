"""
Class that manages the constant values of Telk-Alert-Tool.
"""
class Constants:
	"""
	Message that appears in the background of the application.
	"""
	BACKTITLE = "TELK-ALERT-TOOL v3.3 by Erick Rodriguez"

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
	Absolute path of the SSL certificate.
	"""
	CERTIFICATE_FILE_PATH = "/etc/Telk-Alert-Suite/Telk-Alert/certificates"

	"""
	Absolute path of the Telk-Alert-Tool log file.
	"""
	LOG_FILE_NAME = "/var/log/Telk-Alert/telk-alert-tool-log-"

	"""
	Owner user of the application files.
	"""
	USER = "telk_alert"

	"""
	Owner group of the application files.
	"""
	GROUP = "telk_alert"

	"""
	Options that are displayed in the "Main" menu.
	"""
	OPTIONS_MAIN_MENU = [("1", "Configuration"),
					     ("2", "Alert Rules"),
					     ("3", "Service"),
					     ("4", "About"),
					     ("5", "Exit")]

	"""
	Options that are displayed in the "Configuration" menu.
	"""
	OPTIONS_CONFIGURATION_MENU = [("1", "Telk-Alert"),
					     		  ("2", "Telk-Alert-Agent")]

	"""
	Options displayed when there is no Telk-Alert configuration file.
	"""
	OPTIONS_CONFIGURATION_FALSE = [("Create", "Create the configuration file", 0)]

	"""
	Options that are displayed when the Telk-Alert configuration file exists.
	"""
	OPTIONS_CONFIGURATION_TRUE = [("Update", "Update the configuration file", 0),
								  ("Display", "Display the configuration file", 0)]

	"""
	Options displayed to select an authentication method.
	"""
	OPTIONS_AUTHENTICATION_METHOD = [("HTTP Authentication", "Use HTTP Authentication", 0),
								     ("API Key", "Use API Key", 0)]

	"""
	Options that are displayed when the option to update the Telk-Alert configuration file is chosen.
	"""
	OPTIONS_TELK_ALERT_CONFIGURATION_UPDATE = [("Host", "ElasticSearch Host", 0),
							 	 			   ("Port", "ElasticSearch Port", 0),
							 	 			   ("Folder", "Alert Rules Folder", 0),
							 	 			   ("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							 	 			   ("Authentication", "Enable or disable authentication method", 0)]

	"""
	Options that are displayed in the "ElasticSearch Hosts" menu.
	"""
	OPTIONS_ES_HOST = [("1", "Add New Hosts"),
					   ("2", "Modify Hosts"),
					   ("3", "Remove Hosts")]

	"""
	Options displayed when the use of SSL/TLS is enabled.
	"""
	OPTIONS_SSL_TLS_TRUE = [("Disable", "Disable SSL/TLS communication", 0),
							("Certificate Verification", "Modify certificate verification", 0)]

	"""
	Options displayed when the use of SSL/TLS is disabled.
	"""
	OPTIONS_SSL_TLS_FALSE = [("Enable", "Enable SSL/TLS communication", 0)]

	"""
	Options displayed when certificate verification is enabled.
	"""
	OPTIONS_VERIFICATE_CERTIFICATE_TRUE = [("Disable", "Disable certificate verification", 0),
								   		   ("Certificate File", "Change certificate file", 0)]

	"""
	Options displayed when certificate verification is disabled.
	"""
	OPTIONS_VERIFICATE_CERTIFICATE_FALSE = [("Enable", "Enable certificate verification", 0)]

	"""
	Options that are displayed when an authentication method is enabled.
	"""
	OPTIONS_AUTHENTICATION_TRUE = [("Disable", "Disable authentication method", 0),
								   ("Method", "Modify authentication method", 0)]

	"""
	Options that are displayed when an authentication method is going to be updated.
	"""
	OPTIONS_AUTHENTICATION_METHOD_UPDATE = [("Disable", "Disable authentication method", 0),
									        ("Data", "Modify authentication method data", 0)]

	"""
	Options that are displayed when an authentication method isn't enabled.
	"""
	OPTIONS_AUTHENTICATION_FALSE = [("Enable", "Enable authentication", 0)]

	"""
	Options that are displayed when the authentication method is HTTP Authentication.
	"""
	OPTIONS_HTTP_AUTHENTICATION_DATA = [("Username", "Username for HTTP Authentication", 0),
								 		("Password", "User password", 0)]

	"""
	Options that are displayed when the authentication method is API Key.
	"""
	OPTIONS_API_KEY_DATA = [("ID", "API Key ID", 0),
							("API Key", "API Key", 0)]

	"""
	Options that display units of time.
	"""
	OPTIONS_UNIT_TIME = [["minutes", "Time expressed in minutes", 1],
					  	 ["hours", "Time expressed in hours", 0],
					  	 ["days", "Time expressed in days", 0]]

	"""
	Options that are displayed when the option to update the Telk-Alert-Agent configuration file is chosen.
	"""
	OPTIONS_TELK_ALERT_AGENT_CONFIGURATION_UPDATE = [("Time", "Service validation time", 0),
							       					 ("Bot Token", "Telegram bot token", 0),
							       					 ("Chat ID", "Telegram chat id", 0)]