#!/usr/bin/env python

import sys
import os
import json
import re
import urllib
import urllib2

# Basic Dynamic DNS update client. Written around the no-ip.com API.
# Supports determining your public IP by querying an external web service, or by
# using an IP address from a local interface
#
# Reads in config from a JSON file. Required parameters:
#  * method (web or interface)
#  * hostname (dynamic DNS name that will be updated)
#  * username
#  * password
#  * externIf (interface name, only required if using method 'interface')
#
# Author: Thomas Coe
# Created: 2018-08-17

# UserAgent parameters
program = "tac-dyndns"
version = "1.0"
contact = "thomascoe1@gmail.com"

baseUrl = "https://dynupdate.no-ip.com/nic/update"

if (len(sys.argv) != 2):
    print ("usage: %s config.json" % sys.argv[0])
    exit()

# Read in config from file
filename = sys.argv[1]
with open(filename) as json_file:
    config = json.load(json_file)
method      = config["method"]
hostname    = config["hostname"]
username    = config["username"]
password    = config["password"]
if method == "interface":
    externIf    = config["externIf"]

# Figure out what IP we're at. Either use a web query, or the IP from an if
if method == "web":
    ip = urllib2.urlopen('http://ip.42.pl/raw').read()
elif method == "interface":
    # Pull the IP address using the 'ip addr show' command
    ipStr = os.popen("/usr/sbin/ip addr show %s | grep 'inet '" % externIf).read().strip()
    m = re.match("inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", ipStr)
    if m:
        ip = m.group(1)
    else:
        print "No IP address found on interface %s!" % externIf
        exit()
else:
    print "Method %s not known!" % method
    exit()

# If there is a last IP in the config file and it's the same as the IP we've
# detected, then there is no need to continue
if "lastIp" in config:
    if config["lastIp"] == ip:
        print "No IP change detected"
        exit()

# Write new IP to the config file
config["lastIp"] = ip
with open(filename, 'w') as json_file:
    json.dump(config, json_file, indent=4)

# Encode data into URL string
data = {
    'hostname': hostname,
    'myip':     ip
}
updateData = urllib.urlencode(data)

# Create the base64 encoded authentication string, build headers
authStr = "%s:%s" % (username,password)
encodedAuth = authStr.encode("base64").rstrip()
headers = {
    'Authorization':    "Basic %s" % encodedAuth,
    'User-Agent':       "%s/%s %s" % (program, version, contact)
}

# Make the request
request = urllib2.Request(baseUrl, updateData, headers)
try:
    result = urllib2.urlopen(request)
except urllib2.HTTPError as e:
    print "HTTP Error: %s %s" % (e.code,e.reason)
    exit()
print (result.read())
