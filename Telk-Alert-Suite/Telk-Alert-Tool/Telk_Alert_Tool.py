#! /usr/bin/env python3.14

"""
Main function.
"""
from os import geteuid
from sys import exit
from modules.Telk_Alert_Tool_Class import TelkAlertTool

if __name__ == "__main__":
	if geteuid() != 0:
		exit("Telk-Alert-Tool must be run as root.")
	telk_alert_tool = TelkAlertTool()
	try:
		while True:
			telk_alert_tool.main_menu()
	except KeyboardInterrupt:
		exit(0)
		