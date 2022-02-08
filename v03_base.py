from datetime import datetime,time,date
from math import ceil
################################################################################

LONG="long"
SHORT="short"
BUY="long"
SELL="short"

POSITION_SIGN={LONG:1,SHORT:-1}
NOTSET=-1
NOTSETDATE=datetime(2666)

LOT_SIZE=100000
def usd2lot(usd):
    return usd/LOT_SIZE

def lot2usd(lot):
    return lot*LOT_SIZE

################################################################################
#
################################################################################


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
leverage=20
margin=0

def equiy(price):
    result=0
    for order in orders:
        dif=(price-order[SL])*POSITION_SIGN[order[KIND]]*LOT_SIZE
        value=dif/leverage
        result+=value
    return balance-result

def freeMargin():
    return equiy()-margin


def orderId():
    global order_id_counter
    order_id_counter+=1
    return order_id_counter


def order(op:float,kind:str,volume:float,date:datetime,sl=NOTSET,tp=NOTSET,expire_date=NOTSETDATE):
    global margin,orders

    op=op+POSITION_SIGN[kind]*spreadGet(date)
    volume_margin=lot2usd(volume)/leverage
    
    if volume_margin>freeMargin():
        return -1
    
    margin+=volume_margin
    volume_currency=lot2usd(volume)/op

    oid=orderId()

    order=[
        oid,
        sl,
        tp,
        expire_date,
        0,
        op,
        volume,
        volume_currency,
        LEVERAGE,
        volume_margin,
        kind
        ]
    
    orders.append(order)

    return oid




def risk2Volume(op:float,sl:float,risk:int,balance:float,date:datetime):
    risk=balance*risk/100*LOT_SIZE
    vol=LOT_SIZE*(abs(op-sl)+2*spreadGet(date))
    

    if vol<0.008:
        return -1
    elif vol>0.01:
        return vol
    else:
        return 0.01






