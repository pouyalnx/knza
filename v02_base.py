####################################################################
#       green eye queen dimond
#       rulse)
#       base of all money unit is USD
#       base of in trade calculation is pipet
#      *base of all caluacltion in usd dollar max float lenght is 5 digit
#       unit size is lot each lot equal 100000 USD
#       each pipet === 0.1pipe
#       volume unit is lot
####################################################################
from datetime import datetime,time,date
from locale import currency

EXPIRE_DATE=datetime(2369,9,3,6,39)
XAUUSD="XAUUSD"

PIPE_POS={XAUUSD:100}
ACCURACY=2
#####################################################################
#
#####################################################################

def swap_get(date,size):
    return -49*size

######################################################################
#
######################################################################

LOT_SIZE=100000
def usd2lot(usd):
    return usd/LOT_SIZE

def lot2usd(lot):
    return lot*LOT_SIZE

####################################################################
#      just short and long
####################################################################
LONG="long"
SHORT="short"
BUY="long"
SELL="short"


POSITON_SIGN={LONG:1,SHORT:-1}

def reverse_position(pos):
    if pos==LONG:
        return SHORT
    else:
        return LONG

def spread_get(date):
    return 0.48



####################################################################
#   according risk management give our position size
#   notic unti is lot
# risk level number between 0-100 
# free margin so import tant
# -1 return mean unable to handle this position
####################################################################

def volume_get(open,sl,free_margin,risk_level,date,kind):
    op=abs(open-sl)+2*spread_get(date)
    base=free_margin*(risk_level/100)*LOT_SIZE*abs(op)
    return round(base,2)  #fix this for working with europe usd and other currency


#####################################################################
#   each postion is
#   [op,sl,tp,expire_date,kind,open_date,volume]
#    0  1  2  3             4     5        6
positions=[]
position_id_counter=0

balance=0
def balance_get():
    return balance

def equity_get(price,pair,date):
    global positions
    
    equity=balance_get()

    for position in positions:
        
        op=position[0]
        kind=position[4]
        volume=position[6]

        currency_volume=lot2usd(volume)/op
        position_equity=currency_volume*(price-spread_get(date,reverse_position(kind)))
        equity+= round(position_equity,ACCURACY)

    return equity



def position_add(open_price,sl,tp,risk,kind,open_date,expire_date):
    
    volume=volume_get(open_price,sl,0,1)

    if kind==LONG:
        op=open_price+spread_get(open_date,volume,kind)
    else:
        op=open_price-spread_get(open_date,volume,kind)

    positions.append([op,sl,tp,expire_date,kind,open_date,volume])


def position_update(high,low,time):
    pass

def position_close(price,id):
    pass

#####################################################################
#
#
###########################################################################

time_cond=time(13,0)
time_start=time(14,0)
time_end=time(15,0)
cond=False
pos_id=-1

def tick(time:datetime,op,cl,hi,lo):
    global cond,pos_id
    
    position_update(hi,lo,time)

    if time.time==time_cond:
        if op>cl:
            cond=True 
        else:
            cond=False
    elif time.time==time_start:
        if cond==True:
            pos_id=position_add(op-spread_get(),op+spread_get,EXPIRE_DATE,time,op)
            cond=False
    elif time.time==time_end:
        position_close(op,pos_id)




#####################################################################
#
#   main reader
#####################################################################
fname="XAUUSD60.csv"

with open(fname) as f:
    while True:
        line=f.readline()
        if line=="":
            break
        info=line.split(',')
        date_st=info[0].split('.')
        time_st=info[1].split(':')
        time=datetime(int(date_st[0]),int(date_st[1]),int(date_st[2]),int(time_st[0]),int(time_st[1]))
        
        op=float(info[2])
        hi=float(info[3])
        lo=float(info[4])
        cl=float(info[5])
        vl=float(info[6])

        ###############################################################################################


        ###############################################################################################