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

def isDecnt(candel):
    if candel[OP]>candel[CL]:
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
    
def isHighBear(candel1,candel2):
    if isDecnt(candel1)==False:
        return False
    if isDecnt(candel2)==False:
        return False
    if posClose(candel2)!=3:
        return False
    if candel1[LO]<candel2[CL]:
        return False
    return True
#####################################################################
loss=0
profit=0
SL=0
TP=1
Ox=2
SL_DIST=20
TP_DIST=60

orders=[]


def updateOrders(lo,hi):
    global loss,profit
    killed=[]
    for i in range(len(orders)):
        if orders[i][SL]<lo:
            loss+=orders[i][Ox]-orders[i][SL]
            killed.append(i)
        elif orders[i][TP]>hi:
            profit+=orders[i][Ox]-orders[i][TP]
            killed.append(i)
    for i in reversed(killed):
        orders.pop(i)
#####################################################################


SL_TP=[[1,2],
       [2,4],
       [4,8],
       [4,10],
       [5,10],
       [10,20],
       [20,40],
       [40,80]]
fnames=["XAUUSD5.csv"]#,"EURUSD5.csv"]#,"XAUUSD240.csv","EURUSD240.csv"]


for fname in fnames:
    
    for sltp in SL_TP:
        SL_DIST=sltp[0]
        TP_DIST=sltp[1]
        cnt=0
        bearhigh=0
        last=[1000,0,0,0]
        date_flag=False
        loss=0
        
        profit=0
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
                    st_date=timex
                    date_flag=True        
                op=float(info[2])
                hi=float(info[3])
                lo=float(info[4])
                cl=float(info[5])
                vl=float(info[6])
                candel=[op,cl,hi,lo]
                updateOrders(lo,hi)
                ###############################################################################################
                if isHighBear(last,candel):
                    bearhigh+=1
                    orders.append([candel[OP]+SL_DIST-getSpread(),candel[OP]-TP_DIST-getSpread(),candel[OP]+getSpread()])
                #tick(timex,op,cl,hi,lo)
                ###############################################################################################
                last=candel    

        #######################################################################################################
        #print(f"Prob of next is HighBear={round(bearhigh/cnt,2)}")
        #print(f"profit:{round(profit,2)}")
        #print(f"loss:{round(loss,2)}")
        #print(f"result:{round(profit+loss,2)}")    

        print(f"({st_date} - {timex}),{fname} ,p(HighBear)={round(bearhigh/cnt,2)} ,tp={TP_DIST}$ ,sl={SL_DIST}$ ,profit={round(profit,2)} ,loss={round(loss,2)} ,sum={round(profit+loss,2)}")