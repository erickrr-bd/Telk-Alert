#! /usr/bin/env python3

from modules.ServiceClass import Service

"""
Service type object.
"""
service = Service()

"""
Main function of the application
"""
if __name__ == "__main__":
	service.sendStatusTelkAlertService()