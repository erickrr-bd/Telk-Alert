from typing import List
from dataclasses import dataclass, field

@dataclass(frozen = True)
class Constants:
	"""
	Message displayed in the background.
	"""
	BACKTITLE: str = "TELK-ALERT-TOOL v4.0 by Erick Rodriguez"

	"""
	Telk-Alert configuration file.
	"""
	TELK_ALERT_CONFIGURATION: str = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert.yaml"

	"""
	Telk-Alert-Agent configuration file.
	"""
	TELK_ALERT_AGENT_CONFIGURATION: str = "/etc/Telk-Alert-Suite/Telk-Alert-Agent/configuration/telk_alert_agent.yaml"

	"""
	Alert rules path.
	"""
	ALERT_RULES_FOLDER: str = "/etc/Telk-Alert-Suite/Telk-Alert/alert_rules"

	"""
	Encryption key path.
	"""
	KEY_FILE: str = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/key"

	"""
	Telk-Alert-Tool log file.
	"""
	LOG_FILE: str = "/var/log/Telk-Alert/telk-alert-tool-log"

	"""
	Owner user.
	"""
	USER: str = "telk_alert_user"

	"""
	Owner group.
	"""
	GROUP: str = "telk_alert_group"

	"""
	Options displayed in the "Main" menu.
	"""
	MAIN_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Configuration"), ("2", "Alert Rules"), ("3", "Service"), ("4", "About"), ("5", "Exit")])

	"""
	Options displayed in the "Configuration" menu.
	"""
	CONFIGURATION_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Telk-Alert"), ("2", "Telk-Alert-Agent")])

	"""
	Options that are displayed when the configuration file doesn't exist.
	"""
	CONFIGURATION_OPTIONS_FALSE: List = field(default_factory = lambda : [("Create", "Create the configuration file", 0)])

	"""
	Options that are displayed when the configuration file exists.
	"""
	CONFIGURATION_OPTIONS_TRUE: List = field(default_factory = lambda : [("Modify", "Modify the configuration file", 0), ("Display", "Display the configuration file", 0)])

	"""
	Options displayed in the "Alert Rules" menu.
	"""
	ALERT_RULES_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Create alert rule"), ("2", "Modify alert rule"), ("3", "Display alert rule configuration"), ("4", "Delete alert rule(s)"), ("5", "Disable/Enable Alert Rule(s)"), ("6", "Display alert rule(s)")])

	"""
	Options displayed in the "Create Alert Rule" menu.
	"""
	CREATE_ALERT_RULE_MENU_OPTIONS: List = field(default_factory = lambda: [("1", "Create Alert Rule"), ("2", "Create Custom Alert Rule"), ("3", "Load from template")])

	"""
	Options displayed in the "Disable/Enable Alert Rule(s)" menu.
	"""
	DISABLE_ENABLE_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Disable Alert Rule(s)"), ("2", "Enable Alert Rule(s)")])

	"""
	Alert rule level.
	"""
	ALERT_RULE_LEVEL: List = field(default_factory = lambda : [["Low", "Low level alert", 1], ["Medium", "Medium level alert", 0], ["High", "High level alert", 0]])

	"""
	Unit time.
	"""
	UNIT_TIME: List = field(default_factory = lambda: [["minutes", "Time expressed in minutes", 1], ["hours", "Time expressed in hours", 0], ["days", "Time expressed in days", 0]])

	"""
	Query type.
	"""
	QUERY_TYPE: List = field(default_factory = lambda : [("query_string", "Using Query String", 0), ("wildcard_query", "Using Wildcard Query", 0)])

	"""
	Alert rule fields.
	"""
	ALERT_RULE_FIELDS: List = field(default_factory = lambda : [("Name", "Alert rule's name", 0), ("Level", "Alert rule's level", 0), ("Index", "ElasticSearch's index pattern", 0), ("Timestamp", "Timestamp's Field", 0), ("Total Events", "Number of events to which the alert is sent", 0), ("Search Time", "Time in which the search is repeated", 0), ("Range Time", "Search range time", 0), ("Query", "Query type", 0), ("Fields Selection", "Enable or disable fields selection", 0), ("Bot Token", "Telegram Bot Token", 0), ("Chat ID", "Telegram channel identifier", 0)])