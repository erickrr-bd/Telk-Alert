#! /usr/bin/env python3

import sys
sys.path.append('./modules')
from FormClass import FormDialogs

forms = FormDialogs()

if __name__ == "__main__":	
	while True:
		forms.mainMenu()