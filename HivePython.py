"""
Hive

Reads data from Hive
Prints out inside and outside temperatures

Author:  @HarmlessSaucer

"""

 # Required Python Imports
import cookielib
import urllib
import urllib2
import json
import os

 # Hive Authentication
hiveuser = "USERNAME@EMAIL.NONE"
hivepass = "123456789"

def makeRequest(url,payload):
   global urllib2
   global opener
   if payload:
	# Use urllib to encode
	data = urllib.urlencode(payload)
	req = urllib2.Request(url, data)
   else:
	req = urllib2.Request(url)

   # Make a request to the Hive API
   try:
	      resp = urllib2.urlopen(req)
   except urllib2.URLError, e:
	      print e.code
   else:
	      body = resp.read()
	      return body;
   return None;

# Cookies
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# Pretend to be a browser by adding headers
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')]

# URL Opener
urllib2.install_opener(opener)

url = 'https://api.hivehome.com/v5/login'
payload = {
  'username':hiveuser,
  'password':hivepass
  }

# Login to the Hive system
makeRequest(url,payload)

# Get temperature data for inside and outside the house
opener.addheaders = [('X-Requested-With', 'XMLHttpRequest')];
url = 'https://api.hivehome.com/v5/users/' + hiveuser + '/widgets/temperature'
body = makeRequest(url,None)
jsonData = json.loads(body)
temperature = json.loads(body)
inside = temperature['inside']['now']
outside = temperature['outside']['now']

# Get heating target temperature
url = 'https://api.hivehome.com/v5/users/' + hiveuser + '/widgets/climate/targetTemperature?precision=0.5'
body = makeRequest(url,None)
target = json.loads(body)
target = target['temperature']

#print inside, outside and then target heating temperature
print "Inside Temperature:", inside
print "Outside Temperature:", outside
print "Target Temperature:", target


# Logout of Hive
url = 'https://my.hivehome.com/logout'
makeRequest(url,None)
