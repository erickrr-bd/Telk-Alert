"""
Class that manages the application's constants.
"""
from typing import Tuple
from dataclasses import dataclass

@dataclass(frozen = True)
class Constants:
	"""
	Application's constants. Every value is immutable (strings, integers and tuples).
	"""

	# Application's version and release date.
	VERSION: str = "4.2"
	RELEASE_DATE: str = "November 2026"

	# Message displayed in the background.
	BACKTITLE: str = f"TELK-ALERT-TOOL v{VERSION} by Erick Rodriguez"

	# Telk-Alert's configuration file.
	TELK_ALERT_CONFIGURATION: str = "/opt/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert.yaml"

	# Telk-Alert-Agent's configuration file.
	TELK_ALERT_AGENT_CONFIGURATION: str = "/opt/Telk-Alert-Suite/Telk-Alert-Agent/configuration/telk_alert_agent.yaml"

	# Folder where the CA certificate used by Telk-Alert is copied.
	CERTIFICATE_DIR: str = "/opt/Telk-Alert-Suite/Telk-Alert/configuration/certs"

	# Alert rules' path.
	ALERT_RULES_FOLDER: str = "/opt/Telk-Alert-Suite/Telk-Alert/alert_rules"

	# Encryption key's path.
	KEY_FILE: str = "/opt/Telk-Alert-Suite/Telk-Alert/configuration/key"

	# Telk-Alert-Tool's log file.
	LOG_FILE: str = "/var/log/Telk-Alert/telk-alert-tool-log"

	# Owner user.
	USER: str = "telk_alert"

	# Owner group.
	GROUP: str = "telk_alert"

	# systemd unit of Telk-Alert.
	TELK_ALERT_SERVICE: str = "telk-alert.service"

	# systemd unit of Telk-Alert-Agent.
	TELK_ALERT_AGENT_SERVICE: str = "telk-alert-agent.service"

	# Maximum number of events that can trigger an alert rule.
	MAX_TOTAL_EVENTS: int = 100000

	# Maximum number of fields allowed in an alert rule.
	MAX_FIELDS: int = 50

	# Encryption contexts (AES-GCM authenticated data). Each one is a prefix: the field's name is appended (e.g. "telk_alert_rule:telegram_bot_token").
	# The services that decrypt the secrets must use the same values.
	CTX_TELK_ALERT: str = "telk_alert"
	CTX_AGENT: str = "telk_alert_agent"
	CTX_ALERT_RULE: str = "telk_alert_rule"

	# Options displayed in the "Main" menu.
	MAIN_MENU_OPTIONS: Tuple[Tuple[str, str], ...] = (("1", "Configuration"), ("2", "Alert Rules"), ("3", "Service"), ("4", "About"), ("5", "Exit"))

	# Options displayed in the "Configuration" and "Service" menus (choose the component).
	COMPONENT_MENU_OPTIONS: Tuple[Tuple[str, str], ...] = (("1", "Telk-Alert"), ("2", "Telk-Alert-Agent"))

	# Options that are displayed when the configuration file doesn't exist.
	CONFIGURATION_OPTIONS_FALSE: Tuple[Tuple[str, str, int], ...] = (("Create", "Create the configuration file", 0),)

	# Options that are displayed when the configuration file exists.
	CONFIGURATION_OPTIONS_TRUE: Tuple[Tuple[str, str, int], ...] = (("Modify", "Modify the configuration file", 0), ("Display", "Display the configuration file", 0))

	# Options displayed in the "Alert Rules" menu.
	ALERT_RULES_MENU_OPTIONS: Tuple[Tuple[str, str], ...] = (("1", "Create alert rule"), ("2", "Modify alert rule"), ("3", "Display alert rule configuration"), ("4", "Delete alert rule(s)"), ("5", "Disable/Enable Alert Rule(s)"), ("6", "Display alert rule(s)"))

	# Options displayed in the "Create Alert Rule" menu.
	CREATE_ALERT_RULE_MENU_OPTIONS: Tuple[Tuple[str, str], ...] = (("1", "Create Alert Rule"), ("2", "Load from template"))

	# Options displayed in the "Disable/Enable Alert Rule(s)" menu.
	DISABLE_ENABLE_MENU_OPTIONS: Tuple[Tuple[str, str], ...] = (("1", "Disable Alert Rule(s)"), ("2", "Enable Alert Rule(s)"))

	# Alert rule's level: (tag, description). The selected one is marked at runtime.
	ALERT_RULE_LEVEL: Tuple[Tuple[str, str], ...] = (("Low", "Low level alert"), ("Medium", "Medium level alert"), ("High", "High level alert"))

	# Unit time: (tag, description). The selected one is marked at runtime.
	UNIT_TIME: Tuple[Tuple[str, str], ...] = (("minutes", "Time expressed in minutes"), ("hours", "Time expressed in hours"), ("days", "Time expressed in days"))

	# Query type: (tag, description). The selected one is marked at runtime.
	QUERY_TYPE: Tuple[Tuple[str, str], ...] = (("query_string", "Using Query String"),)

	# Alert rule's fields.
	ALERT_RULE_FIELDS: Tuple[Tuple[str, str, int], ...] = (("Name", "Alert rule's name", 0), ("Level", "Alert rule's level", 0), ("Index", "ElasticSearch's index pattern", 0), ("Timestamp", "Timestamp's Field", 0), ("Total Events", "Number of events to which the alert is sent", 0), ("Search Time", "Time in which the search is repeated", 0), ("Range Time", "Search range time", 0), ("Query", "Query type", 0), ("Fields Selection", "Enable or disable fields selection", 0), ("Bot Token", "Telegram Bot Token", 0), ("Chat ID", "Telegram channel identifier", 0))

	# Options displayed when the field restriction's option is enabled.
	OPTIONS_FIELDS_TRUE: Tuple[Tuple[str, str, int], ...] = (("Disable", "Disable fields option", 0), ("Fields", "Modify fields", 0))

	# Options displayed when the field restriction's option is disabled.
	OPTIONS_FIELDS_FALSE: Tuple[Tuple[str, str, int], ...] = (("Enable", "Enable fields option", 0),)

	# Options displayed in the "Fields" menu.
	FIELDS_OPTIONS: Tuple[Tuple[str, str], ...] = (("1", "Add New Field(s)"), ("2", "Modify Field(s)"), ("3", "Remove Field(s)"))

	# Options displayed in the "Service" menu.
	SERVICE_MENU_OPTIONS: Tuple[Tuple[str, str], ...] = (("1", "Start Service"), ("2", "Restart Service"), ("3", "Stop Service"), ("4", "Service Status"))