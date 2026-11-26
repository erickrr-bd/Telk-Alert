"""
Class that manages everything related to Telk-Alert-Tool.
"""
from os import path
from sys import exit
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog, DialogCancelled
from libPyConfiguration import libPyConfiguration
from libPyAgentConfiguration import libPyAgentConfiguration
from .Constants_Class import Constants
from .Alert_Rules_Class import AlertRules


class TelkAlertTool:

	def __init__(self) -> None:
		"""
		Class constructor. The dialog, logger and utils instances are shared with the alert rules.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants
		self.dialog = libPyDialog(Constants.BACKTITLE)


	# --- Internal helpers ----------------------------------------------------------------------
	def _log(self, message, level: int, tag: str) -> None:
		self.logger.create_log(message, level, tag, use_file_handler = True, file_name = Constants.LOG_FILE, user = Constants.USER, group = Constants.GROUP)


	def _menu(self, height: int, options: tuple, title: str) -> int:
		return int(self.dialog.create_menu("Select a option:", height, 50, options, title))


	def _alert_rules(self) -> AlertRules:
		return AlertRules(self.dialog, self.logger, self.utils)


	def _configuration(self) -> libPyConfiguration:
		"""
		Telk-Alert's configuration object (create, modify and display must use the same context).
		"""
		return libPyConfiguration(Constants.BACKTITLE, context = Constants.CTX_TELK_ALERT, certificate_dir = Constants.CERTIFICATE_DIR)


	def _agent_configuration(self) -> libPyAgentConfiguration:
		"""
		Telk-Alert-Agent's configuration object (create, modify and display must use the same context).
		"""
		return libPyAgentConfiguration(Constants.BACKTITLE, context = Constants.CTX_AGENT)


	def _configuration_action(self, configuration_file: str, title: str) -> str:
		"""
		Method that asks what to do with a configuration file depending on whether it exists.
		"""
		if not path.exists(configuration_file):
			return self.dialog.create_radiolist("Select a option:", 8, 50, Constants.CONFIGURATION_OPTIONS_FALSE, title)
		return self.dialog.create_radiolist("Select a option:", 9, 50, Constants.CONFIGURATION_OPTIONS_TRUE, title)


	# --- Menus ---------------------------------------------------------------------------------
	def main_menu(self) -> None:
		"""
		Main menu. Cancelling any dialog returns here; a real Ctrl+C ends the application.
		"""
		try:
			option = self._menu(12, Constants.MAIN_MENU_OPTIONS, "Main Menu")
			self.switch_main_menu(option)
		except DialogCancelled:
			pass
		except Exception as exception:
			self.dialog.create_message("\nUnexpected error. For more information, see the logs.", 8, 50, "Error Message")
			self._log(exception, 4, "_mainMenu")


	def switch_main_menu(self, option: int) -> None:
		match option:
			case 1:
				self.configuration_menu()
			case 2:
				self.alert_rules_menu()
			case 3:
				self.service_menu()
			case 4:
				self.display_about()
			case 5:
				exit(0)


	def configuration_menu(self) -> None:
		option = self._menu(9, Constants.COMPONENT_MENU_OPTIONS, "Configuration Menu")
		self.define_configuration() if option == 1 else self.define_agent_configuration()


	def alert_rules_menu(self) -> None:
		option = self._menu(13, Constants.ALERT_RULES_MENU_OPTIONS, "Alert Rules Menu")
		match option:
			case 1:
				self.create_alert_rule_menu()
			case 2:
				self._alert_rules().modify_alert_rule()
			case 3:
				self._alert_rules().display_configuration()
			case 4:
				self._alert_rules().delete_alert_rules()
			case 5:
				self.disable_enable_alert_rule_menu()
			case 6:
				self._alert_rules().display_alert_rules()


	def create_alert_rule_menu(self) -> None:
		option = self._menu(9, Constants.CREATE_ALERT_RULE_MENU_OPTIONS, "Create Alert Rule Menu")
		match option:
			case 1:
				self.create_alert_rule()
			case 2:
				self.dialog.create_message("\nOption not available yet.", 7, 50, "Notification Message")


	def disable_enable_alert_rule_menu(self) -> None:
		option = self._menu(9, Constants.DISABLE_ENABLE_MENU_OPTIONS, "Disable/Enable Alert Rule Menu")
		alert_rules = self._alert_rules()
		alert_rules.disable_alert_rule() if option == 1 else alert_rules.enable_alert_rule()


	def service_menu(self) -> None:
		option = self._menu(9, Constants.COMPONENT_MENU_OPTIONS, "Service Menu")
		daemon, label = (Constants.TELK_ALERT_SERVICE, "Telk-Alert") if option == 1 else (Constants.TELK_ALERT_AGENT_SERVICE, "Telk-Alert-Agent")
		action = self._menu(11, Constants.SERVICE_MENU_OPTIONS, f"{label} Service Menu")
		self._manage_service(daemon, label, action)


	# --- Service -------------------------------------------------------------------------------
	def _manage_service(self, daemon: str, label: str, option: int) -> None:
		"""
		Method that starts, restarts, stops or shows the status of a service (failures are shown and logged).
		"""
		if option == 4:
			self.dialog.create_scrollbox(self.utils.get_detailed_status_by_daemon(daemon), 18, 70, f"{label} Service")
			return
		action = {1: "started", 2: "restarted", 3: "stopped"}[option]
		if self.utils.manage_daemon(daemon, option) == 0:
			self.dialog.create_message(f"\n{label} service {action}.", 7, 50, "Notification Message")
			self._log(f"{label} service {action}", 3 if option == 3 else 2, "_manageService")
		else:
			error = self.utils.last_error or "Unknown error."
			self.dialog.create_message(f"\nError managing {label} service:\n\n{error[:200]}", 12, 60, "Error Message")
			self._log(f"Error managing {label} service ({action}): {error}", 4, "_manageService")


	# --- Telk-Alert configuration --------------------------------------------------------------
	def define_configuration(self) -> None:
		match self._configuration_action(Constants.TELK_ALERT_CONFIGURATION, "Telk-Alert Configuration"):
			case "Create":
				self.create_configuration()
			case "Modify":
				self._configuration().modify_configuration(Constants.TELK_ALERT_CONFIGURATION, Constants.KEY_FILE, Constants.LOG_FILE, Constants.USER, Constants.GROUP)
			case "Display":
				self._configuration().display_configuration(Constants.TELK_ALERT_CONFIGURATION, Constants.LOG_FILE, Constants.USER, Constants.GROUP)


	def create_configuration(self) -> None:
		telk_alert_data = self._configuration()
		telk_alert_data.define_es_host()
		telk_alert_data.define_verificate_certificate()
		telk_alert_data.define_use_authentication(Constants.KEY_FILE, owner = Constants.USER)
		telk_alert_data.create_file(telk_alert_data.convert_object_to_dict(), Constants.TELK_ALERT_CONFIGURATION, Constants.LOG_FILE, Constants.USER, Constants.GROUP)


	# --- Telk-Alert-Agent configuration --------------------------------------------------------
	def define_agent_configuration(self) -> None:
		match self._configuration_action(Constants.TELK_ALERT_AGENT_CONFIGURATION, "Telk-Alert-Agent Configuration"):
			case "Create":
				self.create_agent_configuration()
			case "Modify":
				self._agent_configuration().modify_agent_configuration(Constants.TELK_ALERT_AGENT_CONFIGURATION, Constants.KEY_FILE, Constants.LOG_FILE, Constants.USER, Constants.GROUP)
			case "Display":
				self._agent_configuration().display_agent_configuration(Constants.TELK_ALERT_AGENT_CONFIGURATION, Constants.LOG_FILE, Constants.USER, Constants.GROUP)


	def create_agent_configuration(self) -> None:
		telk_alert_agent_data = self._agent_configuration()
		telk_alert_agent_data.define_frequency_time()
		telk_alert_agent_data.define_telegram_bot_token(Constants.KEY_FILE, Constants.USER)
		telk_alert_agent_data.define_telegram_chat_id(Constants.KEY_FILE, Constants.USER)
		telk_alert_agent_data.create_file(telk_alert_agent_data.convert_object_to_dict(), Constants.TELK_ALERT_AGENT_CONFIGURATION, Constants.LOG_FILE, Constants.USER, Constants.GROUP)


	# --- Alert rules ---------------------------------------------------------------------------
	def create_alert_rule(self) -> None:
		alert_rule = self._alert_rules()
		alert_rule.define_name()
		alert_rule.define_level()
		alert_rule.define_index_pattern()
		alert_rule.define_timestamp_field()
		alert_rule.define_total_events()
		alert_rule.define_search_time()
		alert_rule.define_range_time()
		alert_rule.define_query_type()
		alert_rule.define_use_fields()
		alert_rule.define_telegram_bot_token()
		alert_rule.define_telegram_chat_id()
		alert_rule.create_file(alert_rule.convert_object_to_dict())


	# --- About ---------------------------------------------------------------------------------
	def display_about(self) -> None:
		text = ("\nAuthor: Erick Roberto Rodríguez Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\nGithub: https://github.com/erickrr-bd/Telk-Alert"
			f"\nTelk-Alert v{Constants.VERSION} - {Constants.RELEASE_DATE}\n\nEasy alerting with ElasticSearch and Python.")
		self.dialog.create_scrollbox(text, 12, 60, "About")