import requests
import json

HOST = "127.0.0.1:9000/invoke"

data = dict()

data["project_id"] = 1
data["code_id"] = 1

jsonData = json.dumps(data)

ret = requests.post(HOST, json=jsonData)

print(ret)