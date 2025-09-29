"""
Class that manages the application's constants.
"""
from dataclasses import dataclass

@dataclass(frozen = True)
class Constants:
	"""
	Telk-Alert's configuration file.
	"""
	TELK_ALERT_CONFIGURATION: str = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert.yaml"

	"""
	Alert rules' path.
	"""
	ALERT_RULES_FOLDER: str = "/etc/Telk-Alert-Suite/Telk-Alert/alert_rules"

	"""
	Encryption key's path.
	"""
	KEY_FILE: str = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/key"

	"""
	Telk-Alert's log file.
	"""
	LOG_FILE: str = "/var/log/Telk-Alert/telk-alert-log"

	"""
	Owner user.
	"""
	USER: str = "telk_alert"

	"""
	Owner group.
	"""
	GROUP: str = "telk_alert"
	