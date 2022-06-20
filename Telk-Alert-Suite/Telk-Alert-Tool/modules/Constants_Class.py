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

	OPTIONS_ALERT_RULES_MENU = [("1", "Create new alert rule"),
					 			("2", "Update alert rule"),
					 			("3", "Delete alert rule(s)"),
					 			("4", "Show all alert rules")]

	OPTIONS_ALERT_RULE_LEVEL = [["Low", "Low level alert", 1],
							 	["Medium", "Medium level alert", 0],
							 	["High", "High level alert", 0]]

	OPTIONS_ALERT_RULE_TYPE = [("Frequency", "Perform searches periodically", 1)]

	OPTIONS_UNIT_TIME = [["minutes", "Time expressed in minutes", 1],
					  	 ["hours", "Time expressed in hours", 0],
					  	 ["days", "Time expressed in days", 0]]

	OPTIONS_QUERY_TYPE = [("query_string", "Perform the search using a Query String", 1)]

	OPTIONS_CUSTOM_RULE = [("Hostname", "Restrict by hostname", 0),
					 	   ("Username", "Restrict by username", 0)]

	OPTIONS_SEND_TYPE_ALERT = [["only", "A single alert with the total of events found", 1],
						       ["multiple", "An alert for each event found", 0]]

	"""
	Options that are displayed to modify "Alert Rule".
	"""
	OPTIONS_FIELDS_UPDATE_ALERT_RULE = [("Name", "Alert rule name", 0),
							  			("Level", "Alert rule level", 0),
							  			("Index", "Index name or index pattern in ElastcSearch", 0),
							  			("Number Events", "Number of events to which the alert is sent", 0),
							  			("Time Search", "Time in which the search will be repeated", 0),
							  			("Time Range", "Time range in which events will be searched", 0),
							  			("Query String", "Query string for event search", 0),
							  			("Fields Option", "Enables or disables the use of fields option", 0),
							  			("Custom Rule", "Enable or disable the use of custom rule", 0),
							  			("Shipping Type", "How the alert will be sent", 0),
							  			("Bot Token", "Telegram Bot Token", 0),
							  			("Chat ID", "Telegram channel identifier", 0)]
	
	"""
	Options that are displayed when "use fields" option is false.
	"""
	OPTIONS_USE_FIELDS_OPTION_FALSE = [("Enable", "Enables the use fields option", 0)]

	"""
	Options that are displayed when "use fields" option is true.
	"""
	OPTIONS_USE_FIELDS_OPTION_TRUE = [("Disable", "Disable the use fields option", 0),
								      ("Data", "Modify configured data", 0)]

	"""
	Options that are displayed when "use fields" option is modify.
	"""
	OPTIONS_USE_FIELDS_OPTION_UPDATE = [("1", "Add New Field(s)"),
									   	("2", "Modify Field(s)"),
									   	("3", "Remove Field(s)")]