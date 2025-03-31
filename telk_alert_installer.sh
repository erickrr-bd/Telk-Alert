#! /bin/bash

# Date: 03/03/2025
# Author: Erick Roberto Rodriguez Rodriguez
# Script that installs Telk-Alert. 
# Create and configure all the resources necessary for its operation.

# Usage: $ ./telk_alert_installer.sh

clear

# Function that generates a banner.
banner()
{
	echo "+------------------------------------------+"
  	printf "| %-40s |\n" "`date`"
  	echo "|                                          |"
  	printf "|`tput bold` %-40s `tput sgr0`|\n" "$@"
  	echo "+------------------------------------------+"
}

# Folders and files necessary for the operation of Telk-Alert.
TELK_ALERT_CONFIGURATION_FOLDER=/etc/Telk-Alert-Suite/Telk-Alert/configuration
TELK_ALERT_AGENT_CONFIGURATION_FOLDER=/etc/Telk-Alert-Suite/Telk-Alert-Agent/configuration
TELK_ALERT_LOGS_FOLDER=/var/log/Telk-Alert
TELK_ALERT_KEY=/etc/Telk-Alert-Suite/Telk-Alert/configuration/key
ALERT_RULES_FOLDER="/etc/Telk-Alert-Suite/Telk-Alert/alert_rules"

# Print banner
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo "
 _____    _ _           _    _           _   
|_   _|__| | | __      / \  | | ___ _ __| |_ 
  | |/ _ \ | |/ /____ / _ \ | |/ _ \ '__| __|
  | |  __/ |   <_____/ ___ \| |  __/ |  | |_ 
  |_|\___|_|_|\_\   /_/   \_\_|\___|_|   \__|v4.0                                          
"
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo -e "[*] Author: Erick Roberto Rodriguez Rodriguez"
echo -e "[*] Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com"
echo -e "[*] GitHub: https://github.com/erickrr-bd/Telk-Alert"
echo -e "[*] Installer for Telk-Alert v4.0 - March 2025\n"

echo "Do you want to install or update Telk-Alert? (I/U)"
read opc
# Option to install Telk-Alert for the first time
if [ $opc = "I" ] || [ $opc = "i" ]; then
	# Creation of the user and group "telk_alert"
	banner "Creating user and group"
	echo ''
	if grep -w ^telk_alert_group /etc/group > /dev/null; then
		echo -e "[*] \e[0;31m\"telk_alert_group\" already exists\e[0m"
	else
		groupadd telk_alert_group
		echo -e "[*] \e[0;32m\"telk_alert_group\" group created\e[0m"
	fi
	if id telk_alert_user &> /dev/null; then
		echo -e "[*] \e[0;31m\"telk_alert_user\" already exists\e[0m\n"
	else
		useradd -M -s /bin/nologin -g telk_alert_group -d /opt/Telk-Alert-Suite telk_alert_user
		echo -e "[*] \e[0;32m\"telk_alert_user\" user created\e[0m\n"
	fi
	# Copy the files necessary for Telk-Alert to work.
	banner "Installation of Telk-Alert"
	echo ''
	cp -r Telk-Alert-Suite /opt
	echo -e "[*] \e[0;32mInstallation complete\e[0m\n"
	# Creation of required folders and files
	banner "Creation of folders and files"
	echo ''
	mkdir -p $TELK_ALERT_CONFIGURATION_FOLDER
	mkdir -p $TELK_ALERT_AGENT_CONFIGURATION_FOLDER
	mkdir -p $TELK_ALERT_LOGS_FOLDER
	mkdir -p $ALERT_RULES_FOLDER
	encryption_key=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > $TELK_ALERT_KEY
$encryption_key
EOF
	echo -e "[*] \e[0;32mFolders and files created\e[0m\n"
	# Change of permissions and owner
	banner "Change of permissions and owner"
	echo ''
	chown telk_alert_user:telk_alert_group -R /etc/Telk-Alert-Suite
	chown telk_alert_user:telk_alert_group -R /opt/Telk-Alert-Suite
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert/Telk_Alert.py
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert-Tool/Telk_Alert_Tool.py
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert-Agent/Telk_Alert_Agent.py
	chown telk_alert_user:telk_alert_group -R $TELK_ALERT_LOGS_FOLDER
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
	# Creation of services for Telk-Alert and Telk-Alert-Agent.
	banner "Creation of services for Telk-Alert and Telk-Alert-Agent"
	echo ''
	cp telk-alert.service /etc/systemd/system/
	cp telk-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	systemctl enable telk-alert.service
	systemctl enable telk-alert-agent.service
	echo -e "[*] \e[0;32mServices created\e[0m\n"
	# Creating aliases for Telk-Alert-Tool
	banner "Creating aliases for Telk-Alert-Tool"
	echo ''
	echo "alias Telk-Alert-Tool='/opt/Telk-Alert-Suite/Telk-Alert-Tool/Telk_Alert_Tool.py'" >> ~/.bashrc
	echo -e "[*] \e[0;32mCreated alias\e[0m\n"
fi