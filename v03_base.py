
from datetime import datetime,time,date, timedelta
from distutils.log import error
from math import ceil
################################################################################
LOGGING=True
DEBUG=True

def printl(msg):
    if LOGGING==True:
        print(msg)

def printd(msg):
    if DEBUG==True:
        print(msg)
#################################################################################

LONG="long"
SHORT="short"
BUY="long"
SELL="short"

POSITION_SIGN={LONG:1,SHORT:-1}
NOTSET=-1
NOTSETDATE=datetime(2666,6,6,6,6,6)

LOT_SIZE=100000

################################################################################
#
################################################################################

def spreadGet(date:datetime):
    return 0.49 # all calculation in dollar unit

################################################################################3
#   Order Struts
#   0--> id
#   1--> sl
#   2--> tp
#   3--> exdate
#   4--> swap
#   5--> open price
#   6--> open date
#   7--> volume
#   8--> volume_curreny
#   9--> leverage
#  10--> margin
#  11--> kind
################################################################################
OID=0
SL=1
TP=2
EXDATE=3
SWAP=4
OP=5
OPENDATE=6
VOLUME=7
VOLUME_CURRENCY=8
LEVERAGE=9
MARGIN=10
KIND=11
################################################################################
order_id_counter=0
orders=[]


balance=0
leverage=50
margin=0

def equiy(price):
    printd(f"***********************function: equity price:{price}")
    result=0
    for order in orders:
        dif=(price-order[OP])*POSITION_SIGN[order[KIND]]*order[VOLUME_CURRENCY]#/order[LEVERAGE]
        result+=dif

        printd(f"   order->{order[OID]} kind:{order[KIND]} open:{order[OP]} volume:{order[VOLUME]} vc:{order[VOLUME_CURRENCY]} lv:{order[LEVERAGE]}")
        printd(f"   ----diff:{dif}---")
    printd(f"*******************equity:{balance+result}")
    
    return balance+result

def freeMargin(price):
    printd("******free margin------")
    return equiy(price)-margin


def orderId():
    global order_id_counter
    order_id_counter+=1
    return order_id_counter


def order(op:float,kind:str,volume:float,date:datetime,sl=NOTSET,tp=NOTSET,expire_date=NOTSETDATE):
    global margin,orders


    op=op+POSITION_SIGN[kind]*spreadGet(date)
    volume_margin=volume*LOT_SIZE/leverage
    
    printd("*******order*******")
    printd(f"    op:{op} volume:{volume} volume_margin:{volume_margin}")
    
    if volume_margin>freeMargin(op):
        return -1
    
    margin+=volume_margin
    volume_currency=LOT_SIZE*volume/op

    oid=orderId()

    order=[
        oid,
        sl,
        tp,
        expire_date,
        0,
        op,
        date,
        volume,
        volume_currency,
        leverage,
        volume_margin,
        kind
        ]
 

    orders.append(order)

    return oid


def risk2Volume(op:float,sl:float,risk:int,balance:float,date:datetime):
    
    risk=freeMargin(op)*risk/100
    vol=risk/(LOT_SIZE*(abs(op-sl)+spreadGet(date)))
    vol=round(vol,2)

    if vol<0.01:
        return -1
    return vol



def closeOrder(id:int,price:float):
    global margin,balance
    flag=False
    for i in range(len(orders)):
        if orders[i][OID]==id:
            flag=True
            break

    if flag==False:
        return -1

    order=orders.pop(i)
    op=order[OP]
    volume_currency=order[VOLUME_CURRENCY]
    volume_margin=order[MARGIN]
    kind=order[KIND]
    swap=order[SWAP]  #no use until now

    diff=volume_currency*(price-op)*POSITION_SIGN[kind]
    balance+=diff
    margin-=volume_margin
    return id


def updateOrders(hi:float,lo:float,date:datetime):
    close_id=[]
    
    for order in orders:
        exptime=order[EXDATE]
        sl=order[SL]
        tp=order[TP]
        id=order[OID]
        kind=order[KIND]

        if sl>=lo and sl<=hi:
            close_id.append([id,sl])
        elif tp>=lo and tp<=hi:
            close_id.append([id,tp])
        elif date>=exptime:
            if kind==LONG:
                close_id.append([id,lo])
            else:
                close_id.append([id,hi])

    for pack in close_id:
        id=pack[0]
        price=pack[1]
        stat=closeOrder(id,price)

#    if equiy((hi+lo)/2)<0:
#        error("U have no margin")  it fuck cpu it cant work under it

    #what are u doing if it good to call


#####################################################################
#
#
###########################################################################

time_cond=time(21,15)
time_start=time(21,20)
time_end=time(21,25)


cond=False
pos_id=-1

def tick(time:datetime,op,cl,hi,lo):
    global cond,pos_id
    
    updateOrders(hi,lo,time)
    if time.time()==time_cond:
        if op>cl:
            cond=True 
        else:
            cond=False
    elif time.time()==time_start:
        if cond==True:
            #(open_price,sl,tp,risk,kind,open_date,expire_date):
            if op>cl:
                kind=LONG
            else:
                kind=SHORT
            pos_id=order(op,kind,0.02,time)
            #pos_id=position_add(op,inf,inf,1,kind,time,EXPIRE_DATE)
            cond=False
    
    elif time.time()>=time_end:
        closeOrder(cl,pos_id)



#####################################################################
#
#   main reader
#####################################################################
fname="XAUUSD5.csv"
balance=1000

with open(fname) as f:
    while True:



        line=f.readline()
        if line=="":
            break
        info=line.split(',')
        date_st=info[0].split('.')
        time_st=info[1].split(':')
        timex=datetime(int(date_st[0]),int(date_st[1]),int(date_st[2]),int(time_st[0]),int(time_st[1]))
        
        op=float(info[2])
        hi=float(info[3])
        lo=float(info[4])
        cl=float(info[5])
        vl=float(info[6])

        ###############################################################################################

        tick(timex,op,cl,hi,lo)
        ###############################################################################################
        
###################################################################

for order in orders:
    print(order)

print(equiy(cl))