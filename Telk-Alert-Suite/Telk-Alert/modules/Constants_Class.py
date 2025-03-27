from dataclasses import dataclass

@dataclass(frozen = True)
class Constants:
	"""
	Telk-Alert configuration file.
	"""
	TELK_ALERT_CONFIGURATION: str = "/etc/Telk-Alert-Suite/Telk-Alert/configuration/telk_alert.yaml"

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
	LOG_FILE: str = "/var/log/Telk-Alert/telk-alert-log"

	"""
	Owner user.
	"""
	USER: str = "telk_alert_user"

	"""
	Owner group.
	"""
	GROUP: str = "telk_alert_group"