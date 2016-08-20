import sys
sys.path.append("../")
sys.path.append("../../runeHTTP")
from instanceMonitor import Monitor


# NOTICE 
# Please run server before the test
# to execute server, run this file ( ../../runeHTTP/run.py )


# transfer system state 
mon = Monitor()

for x in range(5) :
	mon.GetSystemState()
	json = mon.MakeJSON()
	print(json)
	print("Send JSON Data Test")
	mon.SendJSON(json)
 
