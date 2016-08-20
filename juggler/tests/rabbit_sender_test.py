import json
import sys

sys.path.append("../")
sys.path.append("../../runeHTTP")

from rabbit_sender import FunctionCaller

uid = "DCASWW12SDV"
funcResult = json.dumps({"func1":1,"func2":2})
funcResultData = json.loads(funcResult)
print(type(funcResultData))

fc = FunctionCaller()
fc.ResponseFunctionCall(funcResultData, uid)




