import datetime
import pandas as pd
import json
from datetime import datetime


fnames=["\\Users\\tOpak\\Documents\\mms_project\\mms_input\\x12_xauusd_stf9f16fMACD_60.xlsx"]
"""
fnames=["\\Users\\tOpak\\Documents\\mms_project\\mms_input\\nzdusd_stf9f16fMACD_60_w41_s16.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\usdcad_stf9f16fMACD_60_w38_s17.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\audusd_stf9f16fMACD_60_w43_s27.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\eurusd_stf9f16fMACD_60_w33_s23.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\usdjpy_stf9f16f269_60_w43_s25.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\gbpusd_stf16a29l269_60_w42_s13.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\xauusd_stf9f16fMACD_60_w49_s30.xlsx"]
"""

"""
fnames=["\\Users\\tOpak\\Documents\\mms_project\\mms_input\\x12_eurusd_stf9f16fMACD_60_w33_s15.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\x12_audusd_stf9f16fMACD_60_w22_s15.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\x12_usdjpy_stf9f16f269_60_w43_s15.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\x12_nzdusd_stf9f16fMACD_60_w39_s15.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\x12_gbpusd_stf9f16f269_60_w42_s13.xlsx",
        "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\x12_usdcad_stf9f16fMACD_60_w46_s13.xlsx"]
   #     "\\Users\\tOpak\\Documents\\mms_project\\mms_input\\xauusd_stf9f16fMACD_60_w49_s30.xlsx"]

"""
fname_out=f"\\Users\\tOpak\\Documents\\mms_project\\mms_meta\\trades_{datetime.now().microsecond}.json"
trades=[]
index=0

total=0
win=0

def trade_rate(inp:list):
    ds=inp[0][0]
    de=inp[-1][0]
    dx=de-ds
    l=len(inp)/2
    return round(100*l/dx.days)

for fname in fnames:
    print(fname,"--->")
    try:
        sub_total=0
        sub_win=0
        fdat=pd.read_excel(fname)
        for i in fdat.values:
            open_d=datetime.fromisoformat(str(i[3]))
            close_d=datetime.fromisoformat(str(i[8]))
            pipes=i[11]
            dir=+1
            sub_total+=1
            sub_win+=1
            if pipes<0:
                dir=-1
                sub_win-=1
                
            trades.append([open_d,index,dir])
            index+=1
            trades.append([close_d,index,0])
            index+=1
        print(f"winrate: %{round(100*sub_win/sub_total)}")
        total+=sub_total
        win+=sub_win
    except:
        print("Cant open or Extract File")
trades.sort(key=lambda x:x[0])
#print(trades)
try:
    print(f"winrate total: _w{round(100*win/total)}_s{trade_rate(trades)}")
except:
    print("cant caculate winrate, check inputs")
print(f"Saved in {fname_out}")
with open(fname_out,'w') as f:
    json.dump(trades,f,default=str)

