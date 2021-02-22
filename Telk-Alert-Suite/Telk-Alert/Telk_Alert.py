#! /usr/bin/env python3

from modules.RulesClass import Rules 

"""
Rules type object.
"""
rules = Rules()

"""
Main function of the application.
"""
if __name__ == "__main__":
	rules.readAllAlertRules()