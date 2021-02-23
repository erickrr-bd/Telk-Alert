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
