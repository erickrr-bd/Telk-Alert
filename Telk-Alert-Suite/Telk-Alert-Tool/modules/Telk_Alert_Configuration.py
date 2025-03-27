from .Constants_Class import Constants
from dataclasses import dataclass, field
from libPyConfiguration import libPyConfiguration

@dataclass
class TelkAlertConfiguration:
	"""
	Class that manages Telk-Alert configuration.
	"""
	constants: Constants = field(default_factory = Constants)

	def create(self) -> None:
		"""
		Method that creates the Telk-Alert configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.define_es_host()
		telk_alert_data.define_verificate_certificate()
		telk_alert_data.define_use_authentication(self.constants.KEY_FILE)
		telk_alert_data.create_file(telk_alert_data.convert_object_to_dict(), self.constants.TELK_ALERT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify(self) -> None:
		"""
		Method that updates or modifies the Telk-Alert configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.modify_configuration(self.constants.TELK_ALERT_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display(self) -> None:
		"""
		Method that displays the Telk-Alert configuration.
		"""
		telk_alert_data = libPyConfiguration(self.constants.BACKTITLE)
		telk_alert_data.display_configuration(self.constants.TELK_ALERT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)