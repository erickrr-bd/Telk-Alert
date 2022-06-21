#! /usr/bin/env python3

from modules.Telk_Alert_Agent_Class import TelkAlertAgent

"""
Attribute that stores an object of the TelkAlertAgent class.
"""
tel_alert_agent = TelkAlertAgent()

"""
Main function of the application
"""
if __name__ == "__main__":
	tel_alert_agent.startTelkAlertAgent()