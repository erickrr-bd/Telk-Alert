#! /usr/bin/env python3.14

"""
Main function.
"""
import signal
from sys import exit
from modules.Telk_Alert_Agent_Class import TelkAlertAgent

if __name__ == "__main__":
	telk_alert_agent = TelkAlertAgent()
	# systemctl stop (SIGTERM) and Ctrl+C (SIGINT) stop the agent without waiting for the next check.
	for signal_number in (signal.SIGTERM, signal.SIGINT):
		signal.signal(signal_number, lambda *_: telk_alert_agent.stop.set())
	if not telk_alert_agent.start_telk_alert_agent():
		exit(1)
	telk_alert_agent.run()
	