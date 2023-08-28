#! /bin/bash

clear

#Constants
telk_alert_configuration_folder=/etc/Telk-Alert-Suite/Telk-Alert/configuration
telk_alert_agent_configuration_folder=/etc/Telk-Alert-Suite/Telk-Alert-Agent/configuration
telk_alert_logs_folder=/var/log/Telk-Alert
telk_alert_key=/etc/Telk-Alert-Suite/Telk-Alert/configuration/key
dir=$(sudo pwd)

echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m"
echo -e "\e[96m@2023 Tekium. All rights reserved.\e[0m"
echo -e "\e[96mAuthor: Erick Roberto Rodríguez Rodríguez\e[0m"
echo -e "\e[96mEmail: erodriguez@tekium.mx, erickrr.tbd93@gmail.com\e[0m"
echo -e "\e[96mGitHub: https://github.com/erickrr-bd/Telk-Alert"
echo -e "\e[96mInstaller for Telk-Alert v3.3 - July 2023\e[0m"
echo -e "\e[96mLicense: GPLv3\e[0m"
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo "Do you want to install or update Telk-Alert? (I/U)"
read opc
if [ $opc = "I" ] || [ $opc = "i" ]; then
	echo -e "\e[96mStarting the Telk-Alert installation process\e[0m\n"
	echo -e "\e[96mCreating user and group \"telk_alert\"\e[0m\n"
	if id telk_alert &> /dev/null; then
		echo -e "\e[0;31mUser \"telk_alert\" already exists\e[0m"
	else
		useradd -M -s /bin/nologin -g telk_alert -d /opt/Telk-Alert-Suite telk_alert
		echo -e "\e[0;32mUser \"telk_alert\" created\e[0m\n"
	fi
	if grep -w ^telk_alert /etc/group > /dev/null; then
		echo -e "\e[0;31mGroup \"telk_alert\" already exists\e[0m\n"
	else
		groupadd telk_alert
		echo -e "\e[0;32mGroup \"telk_alert\" created\e[0m\n"
	fi
	sleep 3
	echo -e "\e[96mCreating the service for Telk-Alert and Telk-Alert-Agent\e[0m\n"
	cd $dir
	cp telk-alert.service /etc/systemd/system/
	cp telk-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	systemctl enable telk-alert.service
	systemctl enable telk-alert-agent.service
	echo -e "\e[96mServices created\e[0m\n"
	sleep 3
	echo -e "\e[96mInstalling Telk-Alert\e[0m\n"
	cp -r Telk-Alert-Suite /opt
	if [ ! -d "$telk_alert_configuration_folder" ]; 
	then
		mkdir -p $telk_alert_configuration_folder
	fi
	if [ ! -d "$telk_alert_agent_configuration_folder" ]; 
	then
		mkdir -p $telk_alert_agent_configuration_folder
	fi
	if [ ! -d "$telk_alert_logs_folder" ]; 
	then
		mkdir -p $telk_alert_logs_folder
	fi
	echo -e "\e[96mTelk-Alert installed\e[0m\n"
	sleep 3
	echo -e "\e[96mCreating encryption key\e[0m\n"
	encryption_key=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > $telk_alert_key
	$encryption_key
EOF
	echo -e "\e[96mEncryption key created\e[0m\n"
	sleep 3
	echo -e "\e[96mMaking changes to Telk-Alert\e[0m\n"
	chown telk_alert:telk_alert -R /opt/Telk-Alert-Suite
	chown telk_alert:telk_alert -R /etc/Telk-Alert-Suite
	chown telk_alert:telk_alert -R /var/log/Telk-Alert
	echo -e "\e[96mChanges made\e[0m\n"
	sleep 3
	echo -e "\e[96mCreating aliases for Telk-Alert-Tool\e[0m\n"
	echo "alias Telk-Alert-Tool='/opt/Telk-Alert-Suite/Telk-Alert-Tool/Telk_Alert_Tool.py'" >> ~/.bashrc
	echo -e "\e[96mAlias created\e[0m\n"
	sleep 3
	echo -e "\e[96mRunning Telk-Alert-Tool\e[0m\n"
	sleep 3
	cd /opt/Telk-Alert-Suite/Telk-Alert-Tool
	python3 Telk_Alert_Tool.py
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	echo -e "\e[96mStarting the Telk-Alert update process\e[0m\n"
	echo -e "\e[96mStopping and updating the Telk-Alert and Telk-Alert-Agent service\e[0m\n"
	systemctl stop telk-alert.service
	systemctl stop telk-alert-agent.service
	cp telk-alert.service /etc/systemd/system/
	cp telk-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	echo -e "\e[96mUpdated services\e[0m\n"
	sleep 3
	echo -e "\e[96mUpdating Telk-Alert\e[0m\n"
	cp -r Telk-Alert-Suite /opt
	chown telk_alert:telk_alert -R /opt/Telk-Alert-Suite
	echo -e "\e[96mTelk-Alert updated\e[0m\n"
	sleep 3
	echo -e "\e[96mRunning Telk-Alert-Tool\e[0m\n"
	sleep 3
	cd /opt/Telk-Alert-Suite/Telk-Alert-Tool
	python3 Telk_Alert_Tool.py
fi