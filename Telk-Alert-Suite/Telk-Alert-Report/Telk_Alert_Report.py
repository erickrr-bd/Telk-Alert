#! /usr/bin/env python3

from modules.Telk_Alert_Report_Class import TelkAlertReport

"""
Attribute that stores an object of the TelkAlertReport class.
"""
tel_alert_report = TelkAlertReport()

"""
Main function of the application
"""
if __name__ == "__main__":
	tel_alert_report.startTelkAlertReport()