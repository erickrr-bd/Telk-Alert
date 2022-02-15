# Telk-Alert v3.1 (Tekium ELK - Alert)

Author: Erick Rodríguez 

Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com

License: GPLv3

Telk-Alert is an application to alert about anomalies or patterns of interest in the data stored in ElasticSearch.

Telk-Alert was born as an initiative to have a tool that could alert about possible security events that need to be monitored 24/7.

If you have data in ElasticSearch in real time and need to be alerted when certain events occur, Telk-Alert is the tool for you.

# Applications
## Telk-Alert
Telk-Alert is an application that performs searches by query string in ElasticSearch, and when it finds results, send those results to a Telegram channel.

![Telk-Alert](https://github.com/erickrr-bd/Telk-Alert/blob/master/screens/screen2.jpg)

Characteristics:
- The connection with ElasticSearch can be done through HTTPS and HTTP authentication (It must be configured in ElasticSearch).
- You can enable or not the validation of the SSL certificate.
- It works with any index or index pattern.
- The search in ElasticSearch is done through "Query String".
- Match where there are at least X events in Y time" (frequency type).
- The alert can be sent to a specific telegram channel.
- N alert rules can be configured, each with a specific purpose.
- You can configure the search so that it only shows specific fields of the event.
- Use of "custom rules", for example, to configure an alert rule that alerts failed logins when they are on the same host and by the same user.
- For security reasons, a user is created for the Telk-Alert service to work with.
- In case of finding more than one event, the alert can be configured to send only one message and the total number of events or one message for each event found.
- Parse data that will be sent in the alert to give you a better view.
- Generation of application logs.

## Telk-Alert-Tool
Telk-Alert-Tool is a graphical application that allows the management of the Telk-Alert and Telk-Alert-Agent configuration, the alert rules, as well as the Telk-Alert and Telk-Alert-Agent service, all this in an easy way for the user.

![Telk-Alert-Tool](https://github.com/erickrr-bd/Telk-Alert/blob/master/screens/screen1.jpg)

Characteristics:
- Creation and modification of the Telk-Alert and Telk-Alert-Agent configuration file.
- Alert rules can be created, modified, deleted, or viewed.
- Encrypts sensitive data such as passwords so that they are not stored in plain text.
- Allows you to start, restart, stop and get the status of the Telk-Alert service.
- Allows you to start, restart, stop and get the status of the Telk-Alert-Agent service.
- Generation of application logs.

## Telk-Alert-Agent
Telk-Alert-Agent is an application that validates the status of the Telk-Alert service every minute and alerts in case it has stopped for any reason.

![Telk-Alert-Agent](https://github.com/erickrr-bd/Telk-Alert/blob/master/screens/screen3.jpg)

Characteristics:
- Validate the status of the Telk-Alert service every minute.
- In case the service stops or fails for any reason, an alert every minute is sent until the service starts again.
- Otherwise, that the service is working correctly, the alert is sent at two configurable hours of the day.
- Send the status of the Telk-Alert service to a Telegram channel.
- Generation of application logs.

# Requirements
- CentOS 8 or Red Hat 8 (So far it has only been tested in this version)
- ElasticSearch 7.x 
- Python 3.6
- Python Libraries
  - elasticsearch
  - elasticsearch-dsl
  - requests
  - pycurl
  - pythondialog
  - pycryptodome
  - pyyaml

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
