from instanceMonitor import Monitor
from runeHTTP.request import RuneRequest
from runeHTTP.request import RuneRequestSender





# transfer system state 
mon = Monitor()

for x in range(5) :
	mon.GetSystemState()
	json = mon.MakeJSON()
	print(json)
	print("Send JSON Data Test")
	mon.SendJSON(json)
 
