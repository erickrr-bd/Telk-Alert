#! /usr/bin/env python3

import sys
sys.path.append('./modules')
from ServiceClass import Service

"""
Service type object
"""
service = Service()

"""
Main function of the application
"""
if __name__ == "__main__":
	service.sendStatusTelkAlertService()