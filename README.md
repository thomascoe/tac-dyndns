# tac-dyndns
Basic Dynamic DNS Updater Client in Python. Written to support the no-ip.com API, but should be easily extensible to other dynamic DNS providers

# Usage
`./dyndns.py config.json`

You must provide a JSON file with your configuration parameters. Required:
* method (web or interface)
* hostname (dynamic DNS name that will be updated)
* username
* password
* externIf (interface name, only required if using method 'interface')

Note: the JSON file must be writable by the user running the program. The program stores the last detected IP in this file so that unnecessary updates are not sent
