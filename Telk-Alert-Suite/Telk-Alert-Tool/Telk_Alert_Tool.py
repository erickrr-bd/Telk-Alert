#! /usr/bin/env python3

from modules.Telk_Alert_Tool_Class import TelkAlertTool

"""
Attribute that stores an object of the TelkAlertTool class.
"""
telk_alert_tool = TelkAlertTool()

"""
Main function of the application
"""
if __name__ == "__main__":	
	while True:
		telk_alert_tool.mainMenu()