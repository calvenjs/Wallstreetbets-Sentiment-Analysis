import json
import urllib
from urllib.parse import urlparse
import httplib2 as http

keys_file = open("apiKey.txt")
lines = keys_file.readlines()[0].rstrip()


if __name__=="__main__":
 #Authentication parameters
 headers = { 'AccountKey' : lines,
 'accept' : 'application/json'} #this is by default


 #API parameters
 path = 'http://datamall2.mytransport.sg/ltaodataservice/PV/Bus' #Resource URL
 #Build query string & specify type of API call
 target = urlparse( path)
 print(target.geturl())
 method = 'GET'
 body = ''

 #Get handle to http
 h = http.Http()
 #Obtain results
 response, content = h.request(
 target.geturl(),
 method,
 body,
 headers)
 #Parse JSON to print
 jsonObj = json.loads(content)
 print (json.dumps(jsonObj, sort_keys=True, indent=4))
 #Save result to file
 with open("bus_routes.json","w") as outfile:
     print(outfile)
     json.dump(jsonObj, outfile, sort_keys=True, indent=4,ensure_ascii=False)

