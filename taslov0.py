from cmath import pi
from email.mime import image
import MetaTrader5 as mt5
import datetime
import json
from collections import namedtuple

Trade=namedtuple('Trade','type open close comment symbol date_open date_close')
trades_stack={}

print("connecting...  ",end="")
if not mt5.initialize():
    print(f"!unable to connect mt5t... {mt5.last_error()}")
    exit()
else:
    print("connected!\n\n")


account_info=mt5.account_info()
print("*************************************")
print("login:   ",account_info.login)
print("server:  ",account_info.server)
print("name:    ",account_info.name)
print(f"balance: ${account_info.balance}")
print(f"margin:  ${account_info.margin}")
print("#####################################")


cnt_active_order=mt5.orders_total()
cnt_open_pos=mt5.positions_total()
print(f"count active orders: {cnt_active_order}")
print(f"count open positions: {cnt_open_pos}")

print("#####################################")
print("<<<history analyse>>>")
date_end=datetime.datetime.now()
date_start=datetime.datetime(2000,1,1)

print("numbers of orders: ",mt5.history_orders_total(date_start,date_end))
print("numbers of deals: ",mt5.history_deals_total(date_start,date_end))

orders=mt5.history_orders_get(date_start,date_end)

for order in orders:
    pid=order.position_id
    if pid in trades_stack:
        trades_stack[pid]=trades_stack[pid]._replace(close=order.price_open, date_close=order.time_done)
    else:
        trades_stack[pid]=Trade(order.type,order.price_open,0,order.comment,order.symbol,order.time_done,0,)



import time
def sec2iso(sec:int):
    stc=time.gmtime(sec)
    sts=time.strftime("%Y-%m-%d %H:%M:%S",stc)
    return datetime.datetime.fromisoformat(sts)


trades_seq=[]
index=0
win=0
total=0

for pid in trades_stack:
    total+=1
    trade:Trade=trades_stack[pid]
    if trade.date_close==0 or trade.date_open==0:
        continue
    
    open_d=sec2iso(trade.date_open)
    close_d=sec2iso(trade.date_close)
    if trade.type==0:#Buy
        if trade.close>trade.open:
            dir=1
            win+=1
        else:
            dir=-1
    elif trade.type==1:#Sell
        if trade.close<trade.open:
            dir=1
            win+=1
        else:
            dir=-1

    trades_seq.append([open_d,index,dir])
    index+=1
    trades_seq.append([close_d,index,0])
    index+=1    
    
trades_seq.sort(key=lambda x:x[0])


print("\n\nkill connections... ",end="")
mt5.shutdown()
print("killed!.\n\n\n")



def trade_rate(inp:list):
    ds=inp[0][0]
    de=inp[-1][0]
    dx=de-ds
    l=len(inp)/2
    return round(100*l/dx.days)


fname_out=f"\\Users\\tOpak\\Documents\\mms_project\\mms_meta\\trades_{datetime.datetime.now().microsecond}.json"

print("Quality of trades: ",end="")
try:
    print(f"w:{round(100*win/total)} s:{trade_rate(trades_seq)}")
except:
    print("cant caculate Quality, check inputs")

print("Saving log... ",end=" ")
print(f"Saved in {fname_out}")
with open(fname_out,'w') as f:
    json.dump(trades_seq,f,default=str)
    
    


print("\n\n\n---taslover2022620 poyalx")
print("---mt5",mt5.__version__,mt5.__author__)