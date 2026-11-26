"""
Class that manages the application's constants.
"""
from dataclasses import dataclass

@dataclass(frozen = True)
class Constants:
	"""
	Application's constants. Every value is immutable (strings and integers).
	"""

	# Application's version and release date.
	VERSION: str = "4.2"
	RELEASE_DATE: str = "November 2026"

	# Telk-Alert-Agent's configuration file (same path as in Telk-Alert-Tool).
	TELK_ALERT_AGENT_CONFIGURATION: str = "/opt/Telk-Alert-Suite/Telk-Alert-Agent/configuration/telk_alert_agent.yaml"

	# Encryption key's path (same path as in Telk-Alert-Tool).
	KEY_FILE: str = "/opt/Telk-Alert-Suite/Telk-Alert/configuration/key"

	# Telk-Alert-Agent's log file.
	LOG_FILE: str = "/var/log/Telk-Alert/telk-alert-agent-log"

	# Owner user.
	USER: str = "telk_alert"

	# Owner group.
	GROUP: str = "telk_alert"

	# Encryption context (AES-GCM authenticated data). The field's name is appended. It must match Telk-Alert-Tool.
	CTX_AGENT: str = "telk_alert_agent"

	# systemd unit monitored.
	TELK_ALERT_SERVICE: str = "telk-alert.service"

	# Heartbeat written by Telk-Alert.
	HEARTBEAT_FILE: str = "/run/telk-alert/heartbeat.yaml"

	# Seconds without heartbeat updates after which Telk-Alert is considered hung (Telk-Alert writes it every 60 s).
	HEARTBEAT_MAX_AGE: int = 180

	# Consecutive checks with alert rules not running before restarting Telk-Alert (avoids restarting on a transient delay).
	STALE_CHECKS_BEFORE_RESTART: int = 2