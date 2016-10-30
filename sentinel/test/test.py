import requests
import json

#requests.post("http://127.0.0.1:8080/invoke", data)
ret = requests.post("http://127.0.0.1:8000/getInstanceList", {})

print(ret.json())
