#! /usr/bin/env python3
import sys
sys.path.append('./modules')
from FormClass import FormDialogs

if __name__ == "__main__":
	f = FormDialogs
	while True:
		f.mainMenu(f)