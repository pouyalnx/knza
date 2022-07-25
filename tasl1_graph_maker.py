import matplotlib.pyplot as plt
import json
from datetime import datetime,timedelta
import numpy as np


fname="\\Users\\tOpak\\Documents\\mms_project\\mms_meta\\trades_156380.json"
with open(fname) as f:
    trades=json.load(f)
for trade in trades:
    trade[0]=datetime.fromisoformat(trade[0])
    #print(trade)
    
trades.sort(key=lambda x:x[0])
    
    
points=1024
pos_mul=1
neg_mul=1

ix=0
start_date=trades[0][0]
end_date=trades[-1][0]
dif_date=end_date-start_date


value_array=np.zeros((points,1))
index_array=np.arange(0,points)
date_array=[]
tx=timedelta(seconds=(dif_date).total_seconds()/points)

for k in range(points):
    #print(start_date+tx*k)
    date_array.append(start_date+tx*k)

date_array=np.array(date_array)

for k in range(len(trades)):
    pair=trades[k][1]+1
    dir=trades[k][2]
    
    date_open=trades[k][0]
    for j in range(k+1,len(trades)):
        if trades[j][1]==pair:
            break    
    date_close=trades[j][0]
    
    open_dif=date_open-start_date
    close_dif=date_close-start_date
    
    dif_date:timedelta
    open_dif:timedelta
    close_dif:timedelta

    open_div=open_dif.total_seconds()/dif_date.total_seconds()
    close_div=close_dif.total_seconds()/dif_date.total_seconds()

    open_ix=int(open_div*points)
    close_ix=int(close_div*points)

    if dir>0:
        value_array[open_ix:close_ix+1,0]+=pos_mul
    else:
        value_array[open_ix:close_ix+1,0]+=neg_mul


plt.plot(date_array,value_array)
plt.show()