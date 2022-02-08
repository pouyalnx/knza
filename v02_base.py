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
from cmath import inf
from datetime import datetime,time,date

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
    return 0.01
    #return round(base,2)  #fix this for working with europe usd and other currency


#####################################################################
#   each postion is
#   [op,sl,tp,expire_date,kind,open_date,volume,pid]
#    0  1  2  3             4     5        6     7
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
    
    global position_id_counter,balance
    volume=volume_get(open_price,sl,balance,risk,open_date,kind)

    if kind==LONG:
        op=open_price+spread_get(open_date)
    else:
        op=open_price-spread_get(open_date)

    balance-=volume*op
    position_id_counter+=1
    positions.append([op,sl,tp,expire_date,kind,open_date,volume,position_id_counter])

    return position_id_counter

 #   print(f"**{position_id_counter}**order open sl:{sl} tp:{tp} op:{op} kind:{kind} volume:{volume} date:{open_date} expdate:{expire_date}")




def position_close(price,id,time):
    flag=False
    global balance


    for i in range(len(positions)):
        if positions[i][7]==id:
            flag=True
            break
    
    if flag:
        position=positions.pop(i)
        op=position[0] #spread should be calculated before
        volume=position[6]
        kind=position[4]
        if kind==LONG:
            pr=price-spread_get(time)
        else:
            pr=price+spread_get(time)
            
        vx=volume*LOT_SIZE/op
        tot=vx*price
        tot=round(tot,ACCURACY)
        
        balance+=tot

def position_update(high,low,price,time):
    global balance
    pop_id=[]
    for position in positions:
        #[op,sl,tp,expire_date,kind,open_date,volume,position_id_counter]
        # 0  1  2  3            4     5          6     7
        tp=position[2]
        sl=position[1]
        kind=position[4]
        pid=position[7]
        pos_exp=position[3]

        if tp>=low and tp<=high:           
            pop_id.append([pid,tp])
        elif sl>=low and sl<=high:
            pop_id.append([pid,sl]) 

        elif time > pos_exp:
            pop_id.append([pid,price])

    for pos in pop_id:
        id=pos[0]
        pr=pos[1] 
        position_close(id,pr,time)   

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
    
    #position_update(hi,lo,op,time)
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
            pos_id=position_add(op,inf,inf,1,kind,time,EXPIRE_DATE)
            cond=False
    
    elif time.time()==time_end:
        position_close(op,pos_id,time)




#####################################################################
#
#   main reader
#####################################################################
fname="XAUUSD60.csv"
balance=500


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
print(balance)
print(position_id_counter)