# Telk-Alert v3.3 (Tekium ELK - Alert)

Telk-Alert is an application to alert about anomalies or patterns of interest in the data stored in ElasticSearch.

Telk-Alert was born as an initiative to have a tool that could alert about possible security events that need to be monitored 24/7.

If you have data in ElasticSearch in real time and need to be alerted when certain events occur, Telk-Alert is the tool for you.

# Applications
## Telk-Alert
Telk-Alert is an application that mades searches using "query string" or "aggregations" in an specific ElasticSearch's index pattern, and when it found events or documents, those are sended to a Telegram channel.

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

Characteristics:
- Use of graphical interface.
- You can create, update or show Telk-Alert and Telk-Alert-Agent configuration file.
- You can create, update, delete and show alert rules.
- Encrypts sensitive data such as passwords so that they are not stored in clear text. It uses a passphrase as key. This key is generated during Telk-Alert's installation, whereby, it is different in each installation. 
- You can start, restart, stop and get current status of Telk-Alert and Telk-Alert-Agent service.
- Generation of application logs.

## Telk-Alert-Agent
Telk-Alert-Agent is an application that validates current status of Telk-Alert's service or demon every minute, and, alerts when it isn't working for any reason.

Characteristics:
- It validates the current status of the Telk-Alert's service or demon every minute.
- When Telk-Alert's service or demon isn't working for any reason, an alert every minute is sent.
- Otherwise, that the service is working correctly, the alert is sent at two configurable hours of the day.
- Send the status of the Telk-Alert service to a Telegram channel.
- Generation of application logs.

# Requirements
- CentOS 8 or Rocky Linux 8
- ElasticSearch 7.x 
- Python 3.9
- Python Libraries
  - libPyDialog 1.2 (https://github.com/erickrr-bd/libPyDialog)
  - libPyElk 1.2 (https://github.com/erickrr-bd/libPyElk)
  - libPyTelegram 1.2 (https://github.com/erickrr-bd/libPyTelegram)
  - libPyLog 1.2 (https://github.com/erickrr-bd/libPyLog)
  - libPyUtils 1.2 (https://github.com/erickrr-bd/libPyUtils)

# Installation or update
Give execution permissions to the "installer_telk_alert.sh" file. Run the following command:

`chmod +x installer_telk_alert.sh`

To install or update Telk-Alert you must run the script "installer_telk_alert.sh". Run the following command:

`./installer_telk_alert.sh`

To install Telk-Alert for first time enter the character 'I', otherwise, when a previous version is already installed on the computer enter the character 'U' to update the tool.

The installer will perform all the necessary actions for Telk-Alert to be implemented on your computer.

# Running
## Telk-Alert

`systemctl start telk-alert.service`

**Note:** Configure before starting the application. Use Telk-Alert-Tool.

## Telk-Alert-Agent

`systemctl start telk-alert-agent.service`

**Note:** Configure before starting the application. Use Telk-Alert-Tool.

## Telk-Alert-Tool

Telk-Alert-Tool will start automatically when the installation or update process finishes.

During the installation process, an alias for Telk-Alert-Tool is created. To use the alias, you must first run the following command:

`source ~/.bashrc`

Run Telk-Alert-Tool using the following alias:

`Telk-Alert-Tool`

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
