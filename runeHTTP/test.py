from urllib.parse import urlparse, parse_qs
from request import RuneRequest
from request import RuneRequestSender
import json

# Http parse test

string = 'banana?a=b&c=d&e=f/apple?g=h&i=j&k=l/kiwi'

test = string.split('/')

print(test)

print(len(test))

oldObject = None
firstObject = None

for data in test:
    parseResult =  RuneRequest(data)
    if( oldObject != None ):
        oldObject.addChild(parseResult)
    else:
        firstObject = parseResult
    oldObject = parseResult
#    print(parseResult)

print(firstObject)



# process distribute test


# request generate test

requestObject = RuneRequest()
data = '{"test": "go", "index": 3, "arr": [1,2,3,4,5,6] , "arr2": [{"a":1}, {"b":"2"}]}'
data = json.loads(data)

requestObject.insertRequest(data)

req = RuneRequestSender()
ret = req.sendGET("http://127.0.0.1:8000/test_get")

print("GET REQUEST", ret.content)

req = RuneRequestSender(requestObject)
ret = req.sendPOST("http://127.0.0.1:8000/test_post")

print("POST REQUEST", ret.content)

req = RuneRequestSender(requestObject)
ret = req.sendPOST("http://127.0.0.1:8000/test_post/test_again")

print("POST REQUEST", ret.content)
