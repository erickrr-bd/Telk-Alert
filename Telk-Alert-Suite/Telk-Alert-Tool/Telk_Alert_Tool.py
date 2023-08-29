#! /usr/bin/env python3.9

from modules.Telk_Alert_Tool_Class import TelkAlertTool

telk_alert_tool = TelkAlertTool()

"""
Main function.
"""
if __name__ == "__main__":
	while True:
		telk_alert_tool.main_menu()
