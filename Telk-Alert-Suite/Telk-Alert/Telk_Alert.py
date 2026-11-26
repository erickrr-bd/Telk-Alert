#! /usr/bin/env python3.14

"""
Main function.
"""
import signal
from sys import exit
from modules.Telk_Alert_Class import TelkAlert

if __name__ == "__main__":
	telk_alert = TelkAlert()
	# systemctl stop (SIGTERM) and Ctrl+C (SIGINT) stop the alert rules cleanly.
	for signal_number in (signal.SIGTERM, signal.SIGINT):
		signal.signal(signal_number, lambda *_: telk_alert.stop.set())
	if not telk_alert.start_telk_alert():
		exit(1)
	telk_alert.stop.wait()
	telk_alert.logger.create_log("Telk-Alert stopped", 2, "_stop", use_stream_handler = True)