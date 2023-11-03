# Telk-Alert v3.3 (Tekium ELK - Alert)

Telk-Alert is an application to alert about anomalies or patterns of interest in the data stored in ElasticSearch.

Telk-Alert was born as an initiative to have a tool that could alert about possible security events that need to be monitored 24/7.

If you have data in ElasticSearch in real time and need to be alerted when certain events occur, Telk-Alert is the tool for you.

# Applications
## Telk-Alert
Telk-Alert is an application that periodically searches for defined events and sends alerts via Telegram.

Characteristics:
- The connection to ElasticSearch can be established using the SSL/TLS protocol. **Note:** This must be configured on the cluster.
- The connection with ElasticSearch can be established using an authentication method (HTTP Authentication or API Key). **Note:** This must be configured on the cluster.
- The SSL certificate can be verified or not. **Note:** It's recommended to verify the certificate, for security reasons.
- Telk-Alert works with any index or index pattern.
- Use of [Query String](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/query-dsl-simple-query-string-query.html) to search for defined events. 
- Each alert can be sent to a different Telegram channel.
- Each alert rule is assigned a criticality level (High, medium and low).
- N alert rules can be running at the same time, because Telk-Alert uses threads.
- The search result can be configured to only show certain fields and not all.
- Telk-Alert has an option known as "Custom Search", which uses aggregations. For example, if an alert rule for failed logins is required when these are generated on the same host and with the same user in a period of time, this option is indicated.
- The Telk-Alert daemon runs with a user defined for that purpose, for security reasons.
- You can configure sending a single alert for all events found or one alert for each event found.
- Generation of application logs in `/var/log/Telk-Alert`.

## Telk-Alert-Tool
Telk-Alert-Tool is a graphical application that manages Telk-Alert and Telk-Alert-Agent.

Characteristics:
- Create, update and display Telk-Alert configuration.
- Create, update and display Telk-Alert-Agent configuration.
- Create, update, display and delete alert rules.
- Encrypt sensitive data such as passwords. 
- Start, restart, stop and display the current status of the Telk-Alert daemon.
- Start, restart, stop and display the current status of the Telk-Alert-Agent daemon.
- Generation of application logs in `/var/log/Telk-Alert`.

## Telk-Alert-Agent
Telk-Alert-Agent is an application that periodically monitors the health of Telk-Alert.

Characteristics:
- The validation time period is configurable, for example, every minute or every hour.
- The Telegram channel to which the alerts are sent is configurable.
- Validates the health status of the Telk-Alert daemon. In case, it isn't working for some reason, Telk-Alert-Agent sends an alert to a Telegram channel.
- Validates the number of threads working on Telk-Alert as well as the number of alert rules that should be working. If this number doesn't match, Telk-Alert-Agent sends an alert to a Telegram channel and automatically restarts the Telk-Alert daemon. Ideal, when Telk-Alert is working but an alert rule stopped working.
- Generation of application logs in `/var/log/Telk-Alert`.

# Requirements
- CentOS 8 or Rocky Linux 8 (Tested in these versions)
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
