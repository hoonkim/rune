import requests
import json

HOST = "http://192.168.122.162:9000/invoke"

data = dict()

data["project_id"] = 23
data["code_id"] = 16
data["user_id"] = 50

#param = ["www.google.com"]
param = []

data["params"] = param

jsonData = json.dumps(data)

headers = {"Content-type":"application/json"}

ret = requests.post(HOST,jsonData, headers= headers)

print(ret.text)
