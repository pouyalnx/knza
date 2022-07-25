from cmath import log
import matplotlib.pyplot as plt
import json
from datetime import datetime
from operator import le
fname="\\Users\\tOpak\\Documents\\mms_project\\mms_meta\\trades_662103.json"
with open(fname) as f:
    trades=json.load(f)
for trade in trades:
    trade[0]=datetime.fromisoformat(trade[0])

def winrate(trade:list):
    total=0
    w=0
    for trade in trades:
        index=trade[1]
        if index%2==0:
            total+=1
            if trade[2]>0:
                w+=1
    return round(100*w/total)
    
      
#########################################################################################
def trader(trades:list,bal=1000,risk=1,Reward2risk=2,verbose=True):
    L=len(trades)
    equ=[bal]
    l=0
    if verbose:
        print(f"trader start>> balance:{bal}$  risk:%{risk} Reward2risk={Reward2risk}")
        
    for trade in trades:
        l+=1
        index=trade[1]
        if index%2==1:
            bal+=trade[2]
            equ.append(bal)
            if verbose:
                print(f"<Order {index} end: balance:{bal}$")
            
        else:
            index_twin=index+1
            proff=-bal*risk/100
            if trade[2]>0:
                proff=bal*Reward2risk*risk/100

            for i in range(l,L):
                if trades[i][1]==index_twin:
                    trades[i][2]=proff
                    break
            if verbose:
                print(f">Order {index_twin} added")
    if verbose:
        print(f"Finish trades: balance:{bal}")
    return (bal,equ)


def trade_rate(inp:list):
    ds=inp[0][0]
    de=inp[-1][0]
    dx=de-ds
    l=len(inp)/2
    return round(100*l/dx.days)
    

#######################################################################  
def cycle_trader(inp,bal=1000,repeat=5,risk=1,Reward2risk=2):
    dx=[]
    for i in range(repeat):
        bal,cx=trader(inp,bal,risk,Reward2risk,False)
        dx+=cx
    return bal,dx
########################################################################
########################################################################
#user play area
Rr=2
r=2

########################################################################
bal,dx=cycle_trader(trades,bal=1000,repeat=8,
                    risk=r,
                    Reward2risk=Rr)
ix=[i for i in range(len(dx))]
plt.plot(ix,dx)
plt.show()


#######################################################################
r_start=0.2
r_end=30
steps=800
rx=[]
ry=[]
for i in range(0,steps):
    risk=r_start+(r_end-r_start)*i/steps
    rx.append(risk)
    bal,_=cycle_trader(trades,bal=1000,repeat=20,risk=risk,Reward2risk=Rr)
    ry.append(bal)

plt.plot(rx,ry)
plt.title(f"best risk for Rr:{Rr}")
plt.show()

mx=max(ry)
risk_mx=rx[ry.index(mx)]

############################################################################
#standard output format
bal,_=cycle_trader(trades,bal=1000,repeat=1,
                    risk=r,
                    Reward2risk=Rr)
bal2,_=cycle_trader(trades,bal=1000,repeat=2,
                    risk=r,
                    Reward2risk=Rr)
bal4,_=cycle_trader(trades,bal=1000,repeat=4,
                    risk=r,
                    Reward2risk=Rr)
bal8,_=cycle_trader(trades,bal=1000,repeat=8,
                    risk=r,
                    Reward2risk=Rr)


balx,_=cycle_trader(trades,bal=1000,repeat=1,
                    risk=risk_mx,
                    Reward2risk=Rr)
bal4x,_=cycle_trader(trades,bal=1000,repeat=4,
                    risk=risk_mx,
                    Reward2risk=Rr)
bal8x,_=cycle_trader(trades,bal=1000,repeat=8,
                    risk=risk_mx,
                    Reward2risk=Rr)

print(f"{winrate(trades)}%,{r}%,{Rr},{trade_rate(trades)}%")
print(f"${round(bal)},${round(bal2)},${round(bal4)},${round(bal8)}")
print(f"{round(risk_mx,1)}%,${round(balx)},${round(bal4x)},${round(bal8x)}")