#! /usr/bin/env python3

import sys
sys.path.append('./modules')
from RulesClass import Rules

"""
Rules type object.
"""
rules = Rules()

"""
Main function of the application.
"""
if __name__ == "__main__":
	rules.readAllAlertRules()