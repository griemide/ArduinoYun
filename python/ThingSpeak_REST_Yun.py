#-------------------------------------------------------------------------------
# Name:       ThingSpeak_REST_Yun.py
# Purpose:    sent monitoring data to ThingSpeak server via RESTful api
#
# Author:     Michael Gries (griesu62)
# Copyright:  (c) 2017-2017, Michael Gries
#
# History:
# 2017-05-01  first creation (based on google example
# 2017-05-01  header added
#-------------------------------------------------------------------------------

import httplib, urllib
from time import localtime, strftime
import time

key = 'Z3I57LR93EENKKJB'

field1 = 12  # Aussentemperatur
field2 = 52  # Wassertemperatur
field3 = 74  # Kesseltemperatur
field4 = 44  # Heizkurve
field5 = 00  # VRC status (nummeric)
status = 'new test' # VRC status (plain text)

params = urllib.urlencode(
        {
        'key':    key,
        'field1': field1,
        'field2': field2,
        'field3': field3,
        'field4': field4,
        'field5': field4,
        'status': status
        }
)

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}

conn = httplib.HTTPConnection("api.thingspeak.com:80")
	
try:
	conn.request("POST", "/update", params, headers)
	response = conn.getresponse()
	print strftime("%a, %d %b %Y %H:%M:%S", localtime())
	print response.status, response.reason
	data = response.read()
	conn.close()
except:
	print "connection failed"

