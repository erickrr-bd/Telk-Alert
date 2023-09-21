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
	Options displayed to select a tool from the Telk-Alert suite.
	"""
	OPTIONS_TOOLS_MENU = [("1", "Telk-Alert"),
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

	"""
	Options that are displayed in the "Alert Rules" menu.
	"""
	OPTIONS_ALERT_RULES_MENU = [("1", "Create new alert rule"),
					 			("2", "Update alert rule"),
					 			("3", "Display alert rule data"),
					 			("4", "Remove alert rule(s)"),
					 			("5", "Show all alert rules")]

	"""
	Options that display the criticality levels of the alert rules.
	"""
	OPTIONS_ALERT_RULE_LEVEL = [["Low", "Low level alert", 1],
							 	["Medium", "Medium level alert", 0],
							 	["High", "High level alert", 0]]

	"""
	Options that display alert rule types.
	"""
	OPTIONS_ALERT_RULE_TYPE = [("Frequency", "Search for events periodically", 1)]

	"""
	Options that display the query types.
	"""
	OPTIONS_QUERY_TYPE = [("query_string", "Perform the search using Query String", 0)]

	"""
	Options that show when the custom search option is chosen.
	"""
	OPTIONS_CUSTOM_SEARCH = [("Hostname", "Restrict by hostname", 0),
					 	     ("Username", "Restrict by username", 0)]

	"""
	Options that show the types of alert delivery.
	"""
	OPTIONS_ALERT_DELIVERY_TYPE = [["only", "A single alert with the total of events found", 1],
						           ["multiple", "An alert for each event found", 0]]

	"""
	Options that are displayed when the option to update an alert rule is chosen.
	"""
	OPTIONS_ALERT_RULE_UPDATE = [("Name", "Alert rule's name", 0),
							  	 ("Level", "Alert rule's level", 0),
							  	 ("Index", "ElasticSearch's index pattern", 0),
							  	 ("Total Events", "Number of events to which the alert is sent", 0),
							  	 ("Search Time", "Time in which the search is repeated", 0),
							  	 ("Range Time", "Search range time", 0),
							  	 ("Query", "Query type", 0),
							  	 ("Fields Selection", "Enable or disable fields selection", 0),
							  	 ("Custom Search", "Enable or disable custom search option", 0),
							  	 ("Delivery", "How the alert is sent", 0),
							  	 ("Bot Token", "Telegram Bot Token", 0),
							  	 ("Chat ID", "Telegram channel identifier", 0)]

	"""
	Options displayed when the use of field selection is disabled.
	"""
	OPTIONS_FIELDS_SELECTION_FALSE = [("Enable", "Enable fields selection", 0)]

	"""
	Options displayed when the use of field selection is enabled.
	"""
	OPTIONS_FIELDS_SELECTION_TRUE = [("Disable", "Disable fields selection", 0),
								     ("Data", "Modify data", 0)]

	"""
	Options displayed when the field selection usage is to be modified.
	"""
	OPTIONS_FIELDS_SELECTION_UPDATE = [("1", "Add New Field(s)"),
									   ("2", "Modify Field(s)"),
									   ("3", "Remove Field(s)")]

	"""
	Options that are displayed when the use of custom search is disabled.
	"""
	OPTIONS_CUSTOM_SEARCH_FALSE = [("Enable", "Enable custom search", 0)]

	"""
	Options that are displayed when the use of custom search is enabled.
	"""
	OPTIONS_CUSTOM_SEARCH_TRUE = [("Disable", "Disable custom search", 0),
								  ("Data", "Modify data", 0)]

	"""
	Options displayed when hostname restriction is disabled.
	"""
	OPTIONS_RESTRICTION_BY_HOSTNAME_FALSE = [("Enable", "Enable restriction by hostname", 0)]

	"""
	Options displayed when hostname restriction is enabled.
	"""
	OPTIONS_RESTRICTION_BY_HOSTNAME_TRUE = [("Disable", "Disable restriction by hostname", 0),
								 		    ("Data", "Modify configured data", 0)]

	"""
	Options displayed when username restriction is disabled.
	"""
	OPTIONS_RESTRICTION_BY_USERNAME_FALSE = [("Enable", "Enable restriction by username", 0)]

	"""
	Options that are displayed when username restriction is enabled.
	"""
	OPTIONS_RESTRICTION_BY_USERNAME_TRUE = [("Disable", "Disable restriction by username", 0),
								 		    ("Data", "Modify configured data", 0)]
	
	"""
	Options that are displayed when a value of a restriction type is to be updated.
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