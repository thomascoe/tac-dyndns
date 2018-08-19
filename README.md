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
