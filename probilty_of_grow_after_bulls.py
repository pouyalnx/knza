from datetime import datetime
from doctest import FAIL_FAST
from turtle import position
from xmlrpc.client import TRANSPORT_ERROR
#####################################################################
def getSpread():
    return 0.49

#candel=[op,cl,hi,lo]
OP=0
CL=1
HI=2
LO=3
ZW=0.0001

def isInc(candel):
    if candel[CL]>candel[OP]:
        return True
    return False

def posClose(candel):
    l1=candel[HI]-candel[LO]+ZW
    l2=candel[HI]-candel[CL]
    if (l2/l1)<(1/3):
        return 1
    elif (l2/l1)>(2/3):
        return 3
    return 2
    
def isHighBull(candel1,candel2):
    if isInc(candel1)==False:
        return False
    if isInc(candel2)==False:
        return False
    if posClose(candel2)!=1:
        return False
    if candel1[HI]>candel2[CL]:
        return False
    return True
#####################################################################
loss=0
profit=0
SL=0
TP=1
Ox=2
SL_DIST=5
TP_DIST=50

orders=[]


def updateOrders(lo,hi):
    global loss,profit
    killed=[]
    for i in range(len(orders)):
        if orders[i][SL]>lo:
            loss+=orders[i][SL]-orders[i][Ox]
            killed.append(i)
        elif orders[i][TP]<hi:
            profit+=orders[i][TP]-orders[i][Ox]
            killed.append(i)
    for i in reversed(killed):
        orders.pop(i)
        
#####################################################################
fname="XAUUSD240.csv"
cnt=0
bullhigh=0
last=[1000,0,0,0]
date_flag=False

with open(fname) as f:
    while True:
        cnt+=1
        line=f.readline()
        if line=="":
            break
        info=line.split(',')
        date_st=info[0].split('.')
        time_st=info[1].split(':')
        timex=datetime(int(date_st[0]),int(date_st[1]),int(date_st[2]),int(time_st[0]),int(time_st[1]))
        if date_flag==False:
            print(timex)
            date_flag=True        
        op=float(info[2])
        hi=float(info[3])
        lo=float(info[4])
        cl=float(info[5])
        vl=float(info[6])
        candel=[op,cl,hi,lo]
        updateOrders(lo,hi)
        ###############################################################################################
        if isHighBull(last,candel):
            bullhigh+=1
            orders.append([candel[OP]-SL_DIST-getSpread(),candel[OP]+TP_DIST-getSpread(),candel[OP]+getSpread()])
        #tick(timex,op,cl,hi,lo)
        ###############################################################################################
        last=candel    
#######################################################################################################
print(f"Prob of next is HighBear={round(bullhigh/cnt,2)}")
print(f"profit:{round(profit,2)}")
print(f"loss:{round(loss,2)}")
print(f"result:{round(profit+loss,2)}")    
