from datetime import datetime,time,date
################################################################################

LONG="long"
SHORT="short"
BUY="long"
SELL="short"

POSITION_SIGN={LONG:1,SHORT:-1}


################################################################################
#
################################################################################
balance=0


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
#   9--> 
#  10-->
################################################################################
order_id_counter=0
orders=[]

def orderIdGet():
    global order_id_counter
    order_id_counter+=1
    return order_id_counter


def order(op:float,kind:str,volume:float,date:datetime):
    op=op+POSITION_SIGN[kind]*spreadGet(date)











