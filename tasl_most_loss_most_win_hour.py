import matplotlib.pyplot as plt
import json
from datetime import datetime
fname="\\Users\\tOpak\\Documents\\mms_project\\mms_meta\\trades_156380.json"
with open(fname) as f:
    trades=json.load(f)
for trade in trades:
    trade[0]=datetime.fromisoformat(trade[0])

data_win=[0 for i in range(24)]
data_los=[0 for i in range(24)]


for trade in trades:
    if trade[1]%2==0:
        if trade[2]==1:
            data_win[trade[0].hour]+=1
        else:
            data_los[trade[0].hour]+=1
            




print("+-----------------+")
for i in range(24):
    print("| h:%.2d w:%.3d l:%.3d |"%(i,data_win[i],data_los[i]))
print("+-----------------+")    
            