#! /usr/bin/env python3

import sys
sys.path.append('./modules')
from FormClass import FormDialogs

"""
FormDialogs type object
"""
forms = FormDialogs()

"""
Main function of the application
"""
if __name__ == "__main__":	
	while True:
		forms.mainMenu()