#! /usr/bin/env python3.12

from modules.Telk_Alert_Agent_Class import TelkAlertAgent

"""
Main function.
"""
if __name__ == "__main__":
	telk_alert_agent = TelkAlertAgent()
	telk_alert_agent.run_as_daemon()
