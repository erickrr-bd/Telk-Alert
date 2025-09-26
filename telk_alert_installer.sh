#! /bin/bash

# Date: 26/09/2025
# Author: Erick Roberto Rodriguez Rodriguez
# Installation script. 

# Usage: $ ./telk_alert_installer.sh

clear

# Function that prints a banner.
banner()
{
	echo "+------------------------------------------+"
  	printf "| %-40s |\n" "`date`"
  	echo "|                                          |"
  	printf "|`tput bold` %-40s `tput sgr0`|\n" "$@"
  	echo "+------------------------------------------+"
}

# Application folders and files.
BASE_DIR=/etc/Telk-Alert-Suite
TELK_ALERT_CONFIGURATION=/etc/Telk-Alert-Suite/Telk-Alert/configuration
TELK_ALERT_AGENT_CONFIGURATION=/etc/Telk-Alert-Suite/Telk-Alert-Agent/configuration
TELK_ALERT_LOGS=/var/log/Telk-Alert
TELK_ALERT_KEY=/etc/Telk-Alert-Suite/Telk-Alert/configuration/key
ALERT_RULES_FOLDER="/etc/Telk-Alert-Suite/Telk-Alert/alert_rules"

# Print banner
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo "
 _____    _ _           _    _           _   
|_   _|__| | | __      / \  | | ___ _ __| |_ 
  | |/ _ \ | |/ /____ / _ \ | |/ _ \ '__| __|
  | |  __/ |   <_____/ ___ \| |  __/ |  | |_ 
  |_|\___|_|_|\_\   /_/   \_\_|\___|_|   \__|v4.1                                          
"
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo -e "[*] Author: Erick Roberto Rodriguez Rodriguez"
echo -e "[*] Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com"
echo -e "[*] GitHub: https://github.com/erickrr-bd/Telk-Alert"
echo -e "[*] Installer for Telk-Alert v4.1 - September 2025\n"

echo "Do you want to install or update Telk-Alert? (I/U)"
read opc

if [ $opc = "I" ] || [ $opc = "i" ]; then
	# "telk_alert" user and group creation.
	banner "Creating user and group"
	echo ''
	if grep -w ^telk_alert /etc/group > /dev/null; then
		echo -e "[*] \e[0;31m\"telk_alert\" already exists\e[0m"
	else
		groupadd telk_alert
		echo -e "[*] \e[0;32m\"telk_alert\" group created\e[0m"
	fi
	if id telk_alert &> /dev/null; then
		echo -e "[*] \e[0;31m\"telk_alert\" already exists\e[0m\n"
	else
		useradd -M -s /bin/nologin -g telk_alert -d /opt/Telk-Alert-Suite telk_alert
		echo -e "[*] \e[0;32m\"telk_alert\" user created\e[0m\n"
	fi
	# Copy directories and files.
	banner "Installing Telk-Alert"
	echo ''
	cp -r Telk-Alert-Suite /opt
	echo -e "[*] \e[0;32mInstallation completed\e[0m\n"
	# Creation of folders and files.
	banner "Creation of folders and files"
	echo ''
	mkdir -p $TELK_ALERT_CONFIGURATION
	mkdir -p $TELK_ALERT_AGENT_CONFIGURATION
	mkdir -p $TELK_ALERT_LOGS
	mkdir -p $ALERT_RULES_FOLDER
	encryption_key=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > $TELK_ALERT_KEY
$encryption_key
EOF
	echo -e "[*] \e[0;32mFolders and files created\e[0m\n"
	# Assignment of permits and owner.
	banner "Change of permissions and owner"
	echo ''
	chown telk_alert:telk_alert -R $BASE_DIR
	find $BASE_DIR -type f -exec chmod 640 {} \;
	find $BASE_DIR -type d -exec chmod 750 {} \;
	chown telk_alert:telk_alert -R /opt/Telk-Alert-Suite
	find /opt/Telk-Alert-Suite -type f -exec chmod 640 {} \;
	find /opt/Telk-Alert-Suite -type d -exec chmod 750 {} \;
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert/Telk_Alert.py
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert-Tool/Telk_Alert_Tool.py
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert-Agent/Telk_Alert_Agent.py
	chown telk_alert:telk_alert -R $TELK_ALERT_LOGS
	chmod 750 $TELK_ALERT_LOGS
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
	# Creation of services for Telk-Alert and Telk-Alert-Agent.
	banner "Creation of services for Telk-Alert and Telk-Alert-Agent"
	echo ''
	cp telk-alert.service /etc/systemd/system/
	cp telk-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	systemctl enable telk-alert.service
	systemctl enable telk-alert-agent.service
	echo ''
	echo -e "[*] \e[0;32mServices created\e[0m\n"
	# Creating aliases.
	banner "Creating aliases for Telk-Alert-Tool"
	echo ''
	echo "alias Telk-Alert-Tool='/opt/Telk-Alert-Suite/Telk-Alert-Tool/Telk_Alert_Tool.py'" >> ~/.bashrc
	echo -e "[*] \e[0;32mCreated alias\e[0m\n"
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	# Stop services or daemons.
	banner "Stopping services"
	echo ''
	systemctl stop telk-alert.service
	systemctl stop telk-alert-agent.service
	echo -e "[*] \e[0;32mServices stopped\e[0m\n"
	# "telk_alert" user and group creation.
	banner "Deleting user and group"
	echo ''
	userdel -r telk_alert_user
	groupdel telk_alert_group
	echo -e "[*] \e[0;32mUser and group deleted\e[0m\n"
	banner "Creating user and group"
	echo ''
	if grep -w ^telk_alert /etc/group > /dev/null; then
		echo -e "[*] \e[0;31m\"telk_alert\" already exists\e[0m"
	else
		groupadd telk_alert
		echo -e "[*] \e[0;32m\"telk_alert\" group created\e[0m"
	fi
	if id telk_alert &> /dev/null; then
		echo -e "[*] \e[0;31m\"telk_alert\" already exists\e[0m\n"
	else
		useradd -M -s /bin/nologin -g telk_alert -d /opt/Telk-Alert-Suite telk_alert
		echo -e "[*] \e[0;32m\"telk_alert\" user created\e[0m\n"
	fi
	# Copy directories and files.
	banner "Updating Telk-Alert"
	echo ''
	cp -r Telk-Alert-Suite /opt
	echo -e "[*] \e[0;32mUpdate completed\e[0m\n"
	# Assignment of permits and owner.
	banner "Change of permissions and owner"
	echo ''
	chown telk_alert:telk_alert -R /opt/Telk-Alert-Suite
	find /opt/Telk-Alert-Suite -type f -exec chmod 640 {} \;
	find /opt/Telk-Alert-Suite -type d -exec chmod 750 {} \;
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert/Telk_Alert.py
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert-Tool/Telk_Alert_Tool.py
	chmod +x /opt/Telk-Alert-Suite/Telk-Alert-Agent/Telk_Alert_Agent.py
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
	# Start services or daemons.
	banner "Starting Telk-Alert and Telk-Alert-Agent services"
	echo ''
	systemctl start telk-alert.service
	systemctl start telk-alert-agent.service
	echo -e "[*] \e[0;32mServices started\e[0m\n"
else
	clear
	exit
fi