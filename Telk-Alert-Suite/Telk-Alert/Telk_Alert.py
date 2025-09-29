#! /usr/bin/env python3.12

"""
Main function.
"""
from modules.Telk_Alert_Class import TelkAlert

if __name__ == "__main__":
	telk_alert = TelkAlert()
	telk_alert.run_as_daemon()
	