#--------------------------------------------------------------------------------------------------------------------------
# Name:       sendSMSviaNexmo.py
# Purpose:    send sms via Nexmo service
#
# Author:     Michael Gries (griemide)
# Copyright:  (c) 2015-2017, Michael Gries
#
# History:
# 2015-04-02  creation (ref: http://isbullsh.it/2012/06/Rest-api-in-python/  )
# 2015-04-03  test successful using urllib2 (it's base package of Arduino Yun)
# 2015-04-04  configuration for service request send by VRC-Monitor
# 2017-01-29  link added to test Nexmo service via Mirosoft IE on BBMAG2083 
#---------------------------------------------------------------------------------------------------------------------------

import urllib2 

SMSfrom = '&from=VRC'
SMSto = '&to=00491754193945'
SMStext = '&text=Wartung Heizung (VKO unit)'
SMStextTest = '&Test'

#following two lines only used for testing handler function in generell (not related to Nexmo service)
#test_url = 'https://api.github.com/events' # OK (tested 2015-04-03)
#handler = urllib2.urlopen(test_url) 

#following line can be used to test nexmo service via Microsoft IE on i.e. BBMAG2083 
#https://rest.nexmo.com/sms/json?api_key=17658d32&api_secret=6a75a7ad&from=BBMAG2083&to=00491754193945&text=Service Test https
#http://rest.nexmo.com/sms/json?api_key=17658d32&api_secret=6a75a7ad&from=BBMAG2083&to=00491754193945&text=Service Test

# attention: no blanks allowed in URL (will result in HTTP 400: Bad Request)
# https://de.wikipedia.org/wiki/HTTP-Statuscode
# but blanks will work in Microsoft IE Browser (so mismatch in behaviour not checked yet)
nexmoAPI_url = 'https://rest.nexmo.com/sms/json?api_key=17658d32&api_secret=6a75a7ad'
# TODO: using https will raise handler error due to wrong type. http wille result in 404 (Not Found) 

#nexmoAPI_request = nexmoAPI_url + SMSfrom + SMSto + SMStext.replace(' ', '%20') 
nexmoAPI_request = nexmoAPI_url + SMSfrom + SMSto + SMStextTest 
handler = urllib2.urlopen(nexmoAPI_request) 

response = handler.read()
print response

# file content example (json.json file) replied by nexmo service:
# {"message-count":"1",
#  "messages":
#  [
#   {"to":"491754193945",
#    "message-id":"0300000037BCE278",
#    "status":"0",
#    "remaining-balance":"1.01600000",
#    "message-price":"0.05500000",
#    "network":"26201"
#   }
#  ]
# }