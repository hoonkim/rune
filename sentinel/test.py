import requests
import json

b = {}
b["a"] = 1
b["b"] = True
b["c"] = "Hello"

data = json.dumps(b)

print(data)

#requests.post("http://127.0.0.1:8080/invoke", data)
requests.post("http://127.0.0.1:8080/invoke", b)