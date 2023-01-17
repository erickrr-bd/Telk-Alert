"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Title displayed in the background of the application.
	"""
	BACKTITLE = "TELK-ALERT-TOOL v3.3 by Erick Rodriguez"

	"""
	Absolute path of Telk-Alert.
	"""
	PATH_BASE_TELK_ALERT = "/etc/Telk-Alert-Suite/Telk-Alert"

	"""
	Absolute path of the Telk-Alert configuration file.
	"""
	PATH_TELK_ALERT_CONFIGURATION_FILE = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert_conf.yaml"

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
	NAME_FILE_LOG = "/var/log/Telk-Alert/telk-alert-tool-log-"

	"""
	Name of the user created for the operation of the application.
	"""
	USER = "telk_alert"

	"""
	Name of the group created for the operation of the application.
	"""
	GROUP = "telk_alert"

	"""
	Options displayed in the "Main" menu.
	"""
	OPTIONS_MAIN_MENU = [("1", "Telk-Alert Configuration"),
					     ("2", "Alert Rules"),
					     ("3", "Telk-Alert Service"),
					     ("4", "Telk-Alert Agent"),
					     ("5", "Telk-Alert Report"),
					     ("6", "About"),
					     ("7", "Exit")]

	"""
	Options displayed when the configuration file doesn't exist.
	"""
	OPTIONS_CONFIGURATION_FALSE = [("Create", "Create the configuration file", 0)]

	"""
	Options displayed when the configuration file exists.
	"""
	OPTIONS_CONFIGURATION_TRUE = [("Modify", "Modify the configuration file", 0),
								  ("Show", "Show configuration data", 0)]

	"""
	Options displayed to select an authentication method.
	"""
	OPTIONS_AUTHENTICATION_METHOD = [("HTTP Authentication", "Use HTTP Authentication", 0),
								     ("API Key", "Use API Key", 0)]

	"""
	Options displayed when a value is gonna be modified in the Telk-Alert configuration.
	"""
	OPTIONS_CONFIGURATION_TELK_ALERT_UPDATE = [("Host", "ElasticSearch Host", 0),
							 	 			   ("Port", "ElasticSearch Port", 0),
							 	 			   ("Folder", "Rules Folder", 0),
							 	 			   ("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							 	 			   ("Authentication", "Enable or disable authentication method", 0)]

	"""
	Options displayed when "ElasticSearch hosts" option will be modified.
	"""
	OPTIONS_ES_HOSTS_UPDATE = [("1", "Add New Hosts"),
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
	Options displayed when "SSL certificate verification" option is enabled.
	"""
	OPTIONS_VERIFICATE_CERTIFICATE_TRUE = [("Disable", "Disable certificate verification", 0),
								   		   ("Certificate File", "Change certificate file", 0)]

	"""
	Options displayed when "SSL certificate verification" option is disabled.
	"""
	OPTIONS_VERIFICATE_CERTIFICATE_FALSE = [("Enable", "Enable certificate verification", 0)]

	"""
	Options displayed when "Use authentication method" option is enabled.
	"""
	OPTIONS_AUTHENTICATION_TRUE = [("Data", "Modify authentication method", 0),
								   ("Disable", "Disable authentication method", 0)]

	"""
	Options displayed when an authentication method will be modified.
	"""
	OPTIONS_AUTHENTICATION_METHOD_TRUE = [("Data", "Modify authentication method data", 0),
								   	      ("Disable", "Disable authentication method", 0)]

	"""
	Options displayed when "Use authentication method" option is disabled.
	"""
	OPTIONS_AUTHENTICATION_FALSE = [("Enable", "Enable authentication", 0)]

	"""
	Options displayed when the HTTP authentication credentials will be modified.
	"""
	OPTIONS_HTTP_AUTHENTICATION_DATA = [("Username", "Username for HTTP Authentication", 0),
								 		("Password", "User password", 0)]

	"""
	Options displayed when the API Key credentials will be modified.
	"""
	OPTIONS_API_KEY_DATA = [("API Key ID", "API Key Identifier", 0),
							("Api Key", "API Key", 0)]

	"""
	Options displayed in the "Alert Rules" menu.
	"""
	OPTIONS_ALERT_RULES_MENU = [("1", "Create new alert rule"),
					 			("2", "Update alert rule"),
					 			("3", "Alert Rule Data"),
					 			("4", "Delete alert rule(s)"),
					 			("5", "Show all alert rules")]

	"""
	Options that are displayed to select a Alert rule's level.
	"""
	OPTIONS_ALERT_RULE_LEVEL = [["Low", "Low level alert", 1],
							 	["Medium", "Medium level alert", 0],
							 	["High", "High level alert", 0]]

	"""
	Options that are displayed to select a Alert rule's type.
	"""
	OPTIONS_ALERT_RULE_TYPE = [("Frequency", "Perform searches periodically", 1)]

	"""
	Options that are displayed to select an unit time.
	"""
	OPTIONS_UNIT_TIME = [["minutes", "Time expressed in minutes", 1],
					  	 ["hours", "Time expressed in hours", 0],
					  	 ["days", "Time expressed in days", 0]]

	"""
	Options that are displayed to select a Alert rule's query type.
	"""
	OPTIONS_QUERY_TYPE = [("query_string", "Perform the search using Query String", 0),
						  ("aggregations", "Perform the search using Aggregations", 0)]

	"""
	Options displayed when the "Custom Rule" option is enable.
	"""
	OPTIONS_CUSTOM_RULE = [("Hostname", "Restrict by hostname", 0),
					 	   ("Username", "Restrict by username", 0)]

	"""
	Options displayed to select a Alert rule's send type.
	"""
	OPTIONS_SHIPPING_2 = [["only", "A single alert with the total of events found", 1],
						       ["multiple", "An alert for each event found", 0]]

	"""
	Options displayed when a value is gonna be modified in an alert rule.
	"""
	OPTIONS_ALERT_RULE_UPDATE = [("Name", "Alert rule's name", 0),
							  	 ("Level", "Alert rule's level", 0),
							  	 ("Index", "ElasticSearch's index pattern", 0),
							  	 ("Number Events", "Number of events to which the alert is sent", 0),
							  	 ("Time Search", "Time in which the search will be repeated", 0),
							  	 ("Time Range", "Event search's range", 0),
							  	 ("Query Kind", "Query's kind for event search", 0),
							  	 ("Fields Option", "Enable or disable field's option", 0),
							  	 ("Custom Rule", "Enable or disable custom rule's option", 0),
							  	 ("Shipping Way", "How the alert is sent", 0),
							  	 ("Bot Token", "Telegram's Bot Token", 0),
							  	 ("Chat ID", "Telegram's channel identifier", 0)]
	
	"""
	Options displayed when the "fields" option is disable.
	"""
	OPTIONS_FIELDS_OPTION_FALSE = [("Enable", "Enable field's option", 0)]

	"""
	Options displayed when "fields" option is enable.
	"""
	OPTIONS_FIELDS_OPTION_TRUE = [("Disable", "Disable field's option", 0),
								  ("Data", "Modify configured data", 0)]

	"""
	Options displayed when the "fields" option will be modified.
	"""
	OPTIONS_FIELDS_OPTION_UPDATE = [("1", "Add New Field(s)"),
									("2", "Modify Field(s)"),
									("3", "Remove Field(s)")]

	"""
	Options displayed when the "custom rule" option is disable.
	"""
	OPTIONS_CUSTOM_RULE_OPTION_FALSE = [("Enable", "Enable custom rule's option", 0)]

	"""
	Options displayed when the "custom rule" option is enable.
	"""
	OPTIONS_CUSTOM_RULE_OPTION_TRUE = [("Disable", "Disable custom rule's option", 0),
								 	   ("Data", "Modify configured data", 0)]

	"""
	Options displayed when the "restriction by hostname" option is disable.
	"""
	OPTIONS_RESTRICTION_BY_HOSTNAME_FALSE = [("Enable", "Enable restriction by hostname", 0)]

	"""
	Options displayed when the "restriction by hostname" option is enable.
	"""
	OPTIONS_RESTRICTION_BY_HOSTNAME_TRUE = [("Disable", "Disable restriction by hostname", 0),
								 		    ("Data", "Modify configured data", 0)]

	"""
	Options that are displayed when the "restriction by username" option is false.
	"""
	OPTIONS_RESTRICTION_BY_USERNAME_FALSE = [("Enable", "Enable restriction by username", 0)]

	"""
	Options that are displayed when the "restriction by username" option is true.
	"""
	OPTIONS_RESTRICTION_BY_USERNAME_TRUE = [("Disable", "Disable restriction by username", 0),
								 		    ("Data", "Modify configured data", 0)]
	
	"""
	Options displayed when the "restriction by hostname or username" option will be modified.
	"""
	OPTIONS_RESTRICTION_UPDATE = [("Field", "Field's name in the index", 0),
								  ("Events", "Number of events", 0)]

	"""
	Options displayed in the "Service" menu.
	"""
	OPTIONS_SERVICE_MENU = [("1", "Start Service"),
					  		("2", "Restart Service"),
					  		("3", "Stop Service"),
					  		("4", "Service Status")]

	"""
	Options displayed in the "Telk-Alert-Agent" menu.
	"""
	OPTIONS_TELK_ALERT_AGENT_MENU = [("1", "Configuration"),
					  				 ("2", "Telk-Alert Agent Service")]

	"""
	Options that are shown when a value is going to be modified in the Telk-Alert-Agent configuration.
	"""
	OPTIONS_FIELDS_AGENT_UPDATE = [("First Time", "First time the service is validated", 0),
							       ("Second Time", "Second time the service is validated", 0),
							       ("Bot Token", "Telegram bot token", 0),
							       ("Chat ID", "Telegram chat id", 0)]

	"""
	Options displayed in the "Telk-Alert-Report" menu.
	"""
	OPTIONS_TELK_ALERT_REPORT_MENU = [("1", "Configuration"),
					  				 ("2", "Telk-Alert Report Service")]

	"""
	Options that are shown when a value is going to be modified in the Telk-Alert-Report configuration.
	"""
	OPTIONS_FIELDS_REPORT_UPDATE = [("Execution Time", "Time of obtaining the report", 0),
							        ("Bot Token", "Telegram bot token", 0),
							        ("Chat ID", "Telegram chat id", 0)]