import sys
sys.path.append("../../runeHTTP")
sys.path.append("../")
from instanceMonitor import Monitor


#Test it after to execute run.py in runeHTTP directory
m = Monitor()
m.GetSystemState()
m.DetailState()


