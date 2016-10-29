import requests
import json

HOST = "http://127.0.0.1:9000/invoke"

data = dict()

data["project_id"] = 1
data["code_id"] = 1

jsonData = json.dumps(data)

headers = {"Content-type":"application/json"}

ret = requests.post(HOST,jsonData, headers= headers)

print(ret.text)
