# Telk-Alert v3.3 (Tekium ELK - Alert)

Author: Erick Rodríguez 

Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com

License: GPLv3

Telk-Alert is an application to alert about anomalies or patterns of interest in the data stored in ElasticSearch.

Telk-Alert was born as an initiative to have a tool that could alert about possible security events that need to be monitored 24/7.

If you have data in ElasticSearch in real time and need to be alerted when certain events occur, Telk-Alert is the tool for you.

# Applications
## Telk-Alert
Telk-Alert is an application that mades searches using "query string" or "aggregations" in an specific ElasticSearch's index pattern, and when it found events or documents, those are sended to a Telegram channel.

![Telk-Alert](https://github.com/erickrr-bd/Telk-Alert/blob/master/screens/screen2.jpg)

Characteristics:
- The connection with ElasticSearch can set using HTTPS (SSL/TLS), it means that all data travel through a secure channel and encripted.
- The connection with ElasticSearch can set using an authentication method (HTTP Authentication or API Key). Note: It must be configured in ElasticSearch's cluster.
- The connection with ElasticSearch can set using a certificate file (PEM file) and it can be verficated or no. Note: The recomendation is verificates the cerficate file for more security in the connection.
- It works with any index or index pattern.
- It can use "query string" or "aggregations" to make searches.
- Every alert can send to a specific telegram channel.
- N alert rules can be configured, each with a specific or different purpose.
- You can configure the search so that it only shows specific fields of the event in the Telegram message.
- Use of "custom rules", for example, to configure an alert rule that alerts failed logins when they are on the same host and by the same user.
- Telk Alert's service or daemon runs using the "telk_alert" user. It was created for this purpose, and more security.
- You can set send an alert for all the events or an alert for each one.
- Generation of application logs.

## Telk-Alert-Tool
Telk-Alert-Tool is a graphical application that allows to the user manages Telk-Alert and Telk-Alert-Agent configuration, alert rules (create, update, delete, show), Telk-Alert and Telk-Alert-Agent service and others, everything in an easy way for the user.

![Telk-Alert-Tool](https://github.com/erickrr-bd/Telk-Alert/blob/master/screens/screen1.jpg)

Characteristics:
- Use of graphical interface.
- You can create, update or show Telk-Alert and Telk-Alert-Agent configuration file.
- You can create, update, delete and show alert rules.
- Encrypts sensitive data such as passwords so that they are not stored in clear text. It uses a passphrase as key. This key is generated during Telk-Alert's installation, whereby, it is different in each installation. 
- You can start, restart, stop and get current status of Telk-Alert and Telk-Alert-Agent service.
- Generation of application logs.

## Telk-Alert-Agent
Telk-Alert-Agent is an application that validates current status of Telk-Alert's service or demon every minute, and, alerts when it isn't working for any reason.

![Telk-Alert-Agent](https://github.com/erickrr-bd/Telk-Alert/blob/master/screens/screen3.jpg)

Characteristics:
- It validates the current status of the Telk-Alert's service or demon every minute.
- When Telk-Alert's service or demon isn't working for any reason, an alert every minute is sent.
- Otherwise, that the service is working correctly, the alert is sent at two configurable hours of the day.
- Send the status of the Telk-Alert service to a Telegram channel.
- Generation of application logs.

# Requirements
- CentOS 8 or Red Hat 8 (So far it has only been tested in this version)
- ElasticSearch 7.x 
- Python 3.6
- Python Libraries
  - libPyDialog (https://github.com/erickrr-bd/libPyDialog)
  - libPyElk (https://github.com/erickrr-bd/libPyElk)
  - libPyTelegram (https://github.com/erickrr-bd/libPyTelegram)
  - libPyLog (https://github.com/erickrr-bd/libPyLog)
  - libPyUtils (https://github.com/erickrr-bd/libPyUtils)

# Installation
To install or update Telk-Alert you must run the script "installer_telk_alert.sh" for this you can use any of the following commands:

`./installer_telk_alert.sh` or `sh installer_telk_alert.sh`

The installer performs the following actions on the computer:

- Download the libraries and packages necessary for the operation of Telk-Alert (if so indicated).
- Copy and creation of directories and files necessary for the operation of Telk-Alert.
- Creation of user and specific group for the operation of Telk-Alert.
- It changes the owner of the files and directories necessary for the operation of Telk-Alert, assigning them to the user created for this purpose.
- Creation of passphrase for the encryption and decryption of sensitive information, which is generated randomly, so it is unique for each installed Telk-Alert installation.
- Creation of Telk-Alert and Telk-Alert-Agent services.
- Creation of the alias for the execution of Telk-Alert-Tool.
- Creation of the /var/log/Telk-Alert directory where the application logs are generated.

# Running
## Telk-Alert

- Run as service:

`systemctl start telk-alert.service`

- To execute manually, first you must go to the path /etc/Telk-Alert-Suite/Telk-Alert and execute using the following commands:

`python3 Telk_Alert.py` or `./Telk_Alert.py`

## Telk-Alert-Agent

- Run as service:

`systemctl start telk-alert-agent.service`

- To execute manually, first you must go to the path /etc/Telk-Alert-Suite/Telk-Alert-Agent and execute using the following commands:

`python3 Telk_Alert_Agent.py` or `./Telk_Alert_Agent.py`

## Telk-Alert-Tool

- The first way to run Telk-Alert-Tool, you must go to the path /etc/Telk-Alert-Suite/Telk-Alert-Tool and execute using the following commands:

`python3 Telk_Alert_Tool.py` or `./Telk_Alert_Tool.py`

- The second way to run Telk-Alert-Tool is upon installation of Telk-Alert an alias for Telk-Alert-Tool is created. To use it, you must first execute the following command once the installation is complete:

`source ~/.bashrc`

Later, Telk-Alert-Tool can be executed only by using the following command:

`Telk-Alert-Tool`

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
