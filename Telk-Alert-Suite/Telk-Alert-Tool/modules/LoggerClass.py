import logging
from datetime import date

class Logger:

	def createLogTool(self, message, type_log):
		logger = logging.getLogger('Telk_Alert_Tool_Log')
		fh = logging.FileHandler('/var/log/Telk-Alert/telk_alert_tool_log' + str(date.today()) + '.log')
		logger.addHandler(fh)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		logger.addHandler(fh)
		if type_log == 1:
			logger.debug(message)
		if type_log == 2:
			logger.info(message)
		if type_log == 3:
			logger.warning(message)
		if type_log == 4:
			logger.error(message)
		if type_log == 5:
			logger.critical(message)