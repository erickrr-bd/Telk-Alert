#! /usr/bin/env python3

from modules.TelkAlertClass import TelkAlert 

"""
Property that stores an object of the TelkAlert class.
"""
telkalert = TelkAlert()

"""
Main function of the application.
"""
if __name__ == "__main__":
	telkalert.startTelkAlert()