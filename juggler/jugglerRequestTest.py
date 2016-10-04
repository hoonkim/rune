from urllib.parse import urlparse, parse_qs
from jugglerRequest import RuneRequest
from jugglerRequest import RuneRequestSender
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

#**
requestObject = RuneRequest()


functionObject = {"uFid" : "uid", "function_path": "./", "revision_seq": 3, "validation_required": "T"}

data = json.dumps({"user" :"armin" , 'project' :'rune' , 'function_object': '{"uFid" : "uid", "function_path": "./", "revision_seq": 3, "validation_required": "T"}' , 'params' : '[ "seoul", "kr", "nano" ]' })
#data = json.dumps("{'user' :'armin'}")


print("json data :  " + data)
data = json.loads(data)

requestObject.insertRequest(data)

#req = RuneRequestSender()
#ret = req.sendGET("http://127.0.0.1:8000/test_get")

#print("GET REQUEST", ret.content)

req = RuneRequestSender(requestObject)
ret = req.sendPOST("http://127.0.0.1:8000/test_post")

print("POST REQUEST", ret.content)

#req = RuneRequestSender(requestObject)
#ret = req.sendPOST("http://127.0.0.1:8000/test_post/test_again")

#print("POST REQUEST", ret.content)

