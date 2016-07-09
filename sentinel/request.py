from urllib.parse import urlparse, parse_qs

class SentinelRequestInformation:
    name = None
    queries = None
    child = None

    def __init__(self, requestString):
        self.requestString = requestString
        ret = self.parseRequest(requestString)

        name = 'NA'
        queries = {}

        if ret == False:
            return False


    def parseRequest(self, requestString):
        if(requestString.strip() == ''):
            return False

        parseResult = urlparse(requestString)
        self.name = parseResult.path
        self.queries = parse_qs(parseResult.query)


        return True

    def addChild(self, requestObject):
        if not isinstance(requestObject, type(self)):
            print("mismatch type - ", type(requestObject), type(self))
            return False

        self.child = requestObject
        return True


    def __str__(self):
        ret = '<name: ' + str(self.name) + ', queries: ' + str(self.queries)

        if(self.child != None):
            ret += ', child: ' + str(self.child)

        ret += '>'

        return ret

