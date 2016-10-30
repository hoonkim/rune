import requests
import json

machineA = {}
machineA["uuid"] = "kimothy"
machineA["address"] = "192.168.0.5"
machineA["core"] = 16
machineA["memory"] = 4096
machineA["storage"] = 512

machineB = {}
machineB["uuid"] = "armin"
machineB["address"] = "192.168.0.9"
machineB["core"] = 8
machineB["memory"] = 8192
machineB["storage"] = 1024

machineC = {}
machineC["uuid"] = "teo"
machineC["address"] = "192.168.0.11"
machineC["core"] = 4
machineC["memory"] = 4096
machineC["storage"] = 1024

#requests.post("http://127.0.0.1:8080/invoke", data)

print("add exist instance machineA")
ret = requests.post("http://127.0.0.1:8888/addExistInstance", json=machineA)
print(ret.json())

print("add exist instance machineB")
ret = requests.post("http://127.0.0.1:8888/addExistInstance", json=machineB)
print(ret.json())

print("add exist instance machineC")
ret = requests.post("http://127.0.0.1:8888/addExistInstance", json=machineC)
print(ret.json())

print("get instance list")
ret = requests.post("http://127.0.0.1:8888/getInstanceList", {})
print(ret.json())
