#! /usr/bin/env python3
import sys
sys.path.append('./modules')
from ServiceClass import Service

service = Service()

if __name__ == "__main__":
	service.sendStatusTelkAlertService()