#! /usr/bin/env python3.12

from modules.Telk_Alert_Tool_Class import TelkAlertTool

if __name__ == "__main__":
	telk_alert_tool = TelkAlertTool()
	while True:
		telk_alert_tool.main_menu()