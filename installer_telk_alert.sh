#! /bin/bash

clear
echo "@2021 Tekium. All rights reserved."
echo ''
echo 'Installer for Telk-Alert v3.0'
echo ''
echo 'Author: Erick Rodríguez'
echo ''
echo '--------------------------------------------------------'
read opc
if [ $opc = "I" ]; then
	passphrase=$(cat /dev/random | tr -dc '[:alpha:]' | head -c 30; echo)
	cat << EOF > /etc/Telk-Alert-Suite/Telk-Alert/conf/key 
$passphrase
EOF
fi 
