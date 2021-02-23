# Telk-Alert v3.0

Author: Erick Rodríguez erickrr.tbd93@gmail.com

License: GPLv3

Telk-Alert is an application developed in Python, which allows alerts based on searches made in ElasticSearch.

# Applications
## Telk-Alert
It allows to carry out searches in ElasticSearch from the use of Query String, this search is repeated every so often configurable time, and every time it finds results, send an alert either to a Telegram channel or to email addresses.

## Telk-Alert-Tool
Telk-Alert auxiliary graphic tool that allows the generation of configuration files and alert rules (files where the data for sending alerts are defined), in an intuitive and easy-to-use way. In addition, it allows you to encrypt all sensitive data, such as passwords, and that these are not saved in plain text.

## Telk-Alert-Agent
Telk-Alert auxiliary tool that allows checking the status of the service that allows Telk-Alert to function. This is done at two different times defined by the user, and once the status is validated, it sends a message to a Telegram channel with the result.

# Requirements
- CentOS 8 (So far it has only been tested in this version) 
- Python 3.6
- Python Libraries
  - elasticsearch-dsl
  - requests
  - pycurl
  - pythondialog
  - pycryptodome

# Installation
Run the executable ./installer_telk_alert.sh, which is in charge of installing the packages and libraries necessary for the operation of Telk-Alert (these can also be installed manually). It also creates all the necessary resources so it must be run with administrator permissions.

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
