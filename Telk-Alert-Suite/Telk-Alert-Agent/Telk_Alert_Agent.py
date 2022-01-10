#! /usr/bin/env python3

from modules.TelkAlertAgentClass import TelkAlertAgent

"""
Property that stores an object of the TelkAlertAgent class.
"""
tel_alert_agent = TelkAlertAgent()

"""
Main function of the application
"""
if __name__ == "__main__":
	tel_alert_agent.startTelkAlertAgent()