from urllib.parse import urlparse, parse_qs
from request import SentinelRequestInformation

string = 'banana?a=b&c=d&e=f/apple?g=h&i=j&k=l/kiwi'

test = string.split('/')

print(test)

print(len(test))

oldObject = None
firstObject = None

for data in test:
    parseResult =  SentinelRequestInformation(data)
    if( oldObject != None ):
        oldObject.addChild(parseResult)
    else:
        firstObject = parseResult
    oldObject = parseResult
#    print(parseResult)

print(firstObject)



