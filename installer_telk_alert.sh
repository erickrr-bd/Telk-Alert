#! /bin/bash

clear
echo -e '\e[1;33m--------------------------------------------------------------------------------\e[0m'
echo -e "\e[96m@2023 Tekium. All rights reserved.\e[0m"
echo -e '\e[96mInstaller for Telk-Alert v3.3\e[0m'
echo -e '\e[96mAuthor: Erick Rodríguez\e[0m'
echo -e '\e[96mEmail: erodriguez@tekium.mx, erickrr.tbd93@gmail.com\e[0m'
echo -e '\e[96mLicense: GPLv3\e[0m'
echo -e '\e[1;33m--------------------------------------------------------------------------------\e[0m'
echo ''
echo 'Do you want to install or update Telk-Alert on the computer (I/U)?'
read opc
#Variables
telk_alert_configuration_folder=/etc/Telk-Alert-Suite/Telk-Alert/configuration
telk_alert_agent_configuration_folder=/etc/Telk-Alert-Suite/Telk-Alert-Agent/configuration
telk_alert_logs_folder=/var/log/Telk-Alert
telk_alert_key=/etc/Telk-Alert-Suite/Telk-Alert/configuration/key 
#Telk-Alert installation
if [ $opc = "I" ] || [ $opc = "i" ]; then
	echo -e '\e[96mStarting the Telk-Alert installation\e[0m'
	#Packages and libraries instalation
	echo ''
	echo 'Do you want to install the packages and libraries necessary for the operation of Telk-Alert (Y/N)?'
	read opc_lib
	if [ $opc_lib = "Y" ] || [ $opc_lib = "y" ]; then
		echo ''
		echo -e '\e[96mInstalling the necessary libraries and packages\e[0m'
		yum install python3-pip -y
		dnf install dialog -y
		dnf install gcc -y
		dnf install python3-devel -y
		dnf install libcurl-devel -y
		dnf install openssl-devel -y
		pip3 install pythondialog 
		pip3 install pycryptodome
		pip3 install pyyaml 
		pip3 install pycurl 
		pip3 install elasticsearch-dsl 
		pip3 install requests 
		echo ''
		sleep 3
		echo -e '\e[96mLibraries and packages installed\e[0m'
	fi
	#Create user and group telk_alert
	echo ''
	echo -e '\e[96mCreating user and group "telk_alert"\e[0m'
	groupadd telk_alert
	useradd -M -s /bin/nologin -g telk_alert -d /etc/Telk-Alert-Suite telk_alert
	echo ''
	sleep 3
	echo -e '\e[96m"telk_alert" user and group created\e[0m'
	#Create daemon for Telk-Alert and Telk-Alert-Agent
	echo ''
	echo -e '\e[96mCreating the daemon for Telk-Alert and Telk-Alert-Agent\e[0m'
	dir=$(sudo pwd)
	cd $dir
	cp telk-alert.service /etc/systemd/system/
	cp telk-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	systemctl enable telk-alert.service
	systemctl enable telk-alert-agent.service
	echo ''
	sleep 3
	echo -e '\e[96mCreated daemons\e[0m'
	#Copy and creation of files and folders necesaries for Telk-Alert
	echo ''
	echo -e '\e[96mCopying and creating the necessary files and folders\e[0m'
	cp -r Telk-Alert-Suite /etc/
	if [ ! -d "$telk_alert_configuration_folder" ]; 
	then
		mkdir $telk_alert_configuration_folder
	fi
	if [ ! -d "$telk_alert_agent_configuration_folder" ]; 
	then
		mkdir $telk_alert_agent_configuration_folder
	fi
	if [ ! -d "$telk_alert_logs_folder" ]; 
	then
		mkdir $telk_alert_logs_folder
	fi
	echo ''
	sleep 3
	echo -e '\e[96mFiles and folders created\e[0m'
	#Passphrase creation
	echo ''
	echo -e '\e[96mCreating passphrase\e[0m'
	passphrase=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > $telk_alert_key
$passphrase
EOF
	chown telk_alert:telk_alert -R /etc/Telk-Alert-Suite
	chown telk_alert:telk_alert -R /var/log/Telk-Alert
	echo ''
	sleep 3
	echo -e '\e[96mPassphrase created\e[0m'
	#Alias creation for Telk-Alert-Tool
	echo ''
	echo -e '\e[96mCreating aliases for Telk-Alert-Tool\e[0m'
	echo "alias Telk-Alert-Tool='/etc/Telk-Alert-Suite/Telk-Alert-Tool/Telk_Alert_Tool.py'" >> ~/.bashrc
	echo ''
	sleep 3
	echo -e '\e[96mAliases created\e[0m'
	#Instalation finished
	echo ''
	echo -e '\e[96mTelk-Alert installed in your computer\e[0m'
	sleep 3
	#Telk-Alert-Tool execution	
	echo ''
	echo -e '\e[96mRunning Telk-Alert-Tool\e[0m'
	sleep 3
	cd /etc/Telk-Alert-Suite/Telk-Alert-Tool
	python3 Telk_Alert_Tool.py
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	#Telk-Alert update
	echo ''
	echo -e '\e[96mStarting the Telk-Alert update\e[0m'
	echo ''
	#Update daemons for Telk-Alert and Telk-Alert-Agent
	echo -e '\e[96mStopping and updating the daemons for Telk-Alert and Telk-Alert-Agent\e[0m'
	dir=$(sudo pwd)
	systemctl stop telk-alert.service
	systemctl stop telk-alert-agent.service
	cp telk-alert.service /etc/systemd/system/
	cp telk-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	echo ''
	sleep 3
	echo -e '\e[96mDaemons updated\e[0m'
	#Update files and folder necessary for Telk-Alert
	echo ''
	cp -r Telk-Alert-Suite /etc/
	chown telk_alert:telk_alert -R /etc/Telk-Alert-Suite
	sleep 3
	echo -e '\e[96mTelk-Alert updated\e[0m'
	#Telk-Alert-Tool execution	
	echo ''
	echo -e '\e[96mRunning Telk-Alert-Tool\e[0m'
	sleep 3
	cd /etc/Telk-Alert-Suite/Telk-Alert-Tool
	python3 Telk_Alert_Tool.py
else
	clear
	exit
fi 
