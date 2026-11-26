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

	# Telk-Alert's configuration file (same path as in Telk-Alert-Tool).
	TELK_ALERT_CONFIGURATION: str = "/opt/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert.yaml"

	# Alert rules' path (same path as in Telk-Alert-Tool).
	ALERT_RULES_FOLDER: str = "/opt/Telk-Alert-Suite/Telk-Alert/alert_rules"

	# Encryption key's path (same path as in Telk-Alert-Tool).
	KEY_FILE: str = "/opt/Telk-Alert-Suite/Telk-Alert/configuration/key"

	# Telk-Alert's log file.
	LOG_FILE: str = "/var/log/Telk-Alert/telk-alert-log"

	# Owner user.
	USER: str = "telk_alert"

	# Owner group.
	GROUP: str = "telk_alert"

	# Python >= 3.13 rejects CA certificates that don't fully follow RFC 5280 (e.g. without the Key Usage extension).
	# True: accept the cluster's CA anyway. The chain of trust and the hostname are still verified.
	# Set it to False once the cluster's CA is regenerated with its extensions.
	RELAX_X509_STRICT: bool = True

	# Encryption contexts (AES-GCM authenticated data). Each one is a prefix: the field's name is appended.
	# They must match the values used by Telk-Alert-Tool.
	CTX_TELK_ALERT: str = "telk_alert"
	CTX_ALERT_RULE: str = "telk_alert_rule"

	# Maximum number of events sent to Telegram per alert (they are grouped in as few messages as possible).
	MAX_EVENTS_PER_ALERT: int = 50

	# Maximum length of a Telegram message (Telegram's limit is 4096; the margin covers the counting of emojis).
	TELEGRAM_MAX_LENGTH: int = 4000

	# Seconds between two messages sent to the same chat (3 = 20 messages per minute, Telegram's limit for groups).
	TELEGRAM_SEND_INTERVAL: float = 3.0

	# Maximum number of messages waiting in the sending queue of each chat.
	MAX_QUEUE_SIZE: int = 200

	# Maximum number of event IDs remembered per alert rule to avoid sending the same event twice.
	MAX_SENT_IDS: int = 5000

	# Heartbeat read by Telk-Alert-Agent (/run/telk-alert is created by systemd with RuntimeDirectory=telk-alert).
	HEARTBEAT_FILE: str = "/run/telk-alert/heartbeat.yaml"

	# Seconds between heartbeat updates.
	HEARTBEAT_INTERVAL: int = 60