#-------------------------------------------------------------------------------
# Name:       ThingSpeak_REST_Yun.py
# Purpose:    sent monitoring data to ThingSpeak server via RESTful api
#
# Author:     Michael Gries (griesu62)
# Copyright:  (c) 2017-2017, Michael Gries
#
# History:
# 2017-05-01  first creation (based on google example
# 2017-05-02  header added, argv[] added 
#-------------------------------------------------------------------------------

import sys
value0 = str(sys.argv[0])
print("argv[0]: " + value0)
value1 = str(sys.argv[1])
print("argv[1]: " + value1)
value2 = str(sys.argv[2])
print("argv[2]: " + value2)
value3 = str(sys.argv[3])
print("argv[3]: " + value3)
value4 = str(sys.argv[4])
print("argv[4]: " + value4)
value5 = str(sys.argv[5])
print("argv[5]: " + value5)


import httplib, urllib
from time import localtime, strftime
import time

key = 'Z3I57LR93EENKKJB'

field1 = value1     # Aussentemperatur
field2 = value2     # Wassertemperatur
field3 = value3     # Kesseltemperatur
field4 = value4     # Heizkurve
field5 = value5     # VRC status (nummeric)
status = 'test 17.5.2' # VRC status (plain text)

params = urllib.urlencode(
        {
        'key':    key,
        'field1': field1,
        'field2': field2,
        'field3': field3,
        'field4': field4,
        'field5': field5,
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

