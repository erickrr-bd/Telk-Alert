#! /usr/bin/env python3.9

from modules.Telk_Alert_Agent_Class import TelkAlertAgent

telk_alert_agent = TelkAlertAgent()

"""
Main function.
"""
if __name__ == "__main__":
	telk_alert_agent.start_telk_alert_agent()