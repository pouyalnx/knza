fname="XAUUSD60.csv"


#       |
#   X   |
#      | |
#   Y  | | 
#      | |
#       |
#    Z  |
#       |

def isPower(op,cl,lo,hi):
    df=0.50
    if op>cl:
        x=abs(hi-op)
        y=abs(op-cl)
        z=abs(lo-cl)
        if y>x+z and y>df:
            return True
    else:
        x=abs(hi-cl)
        y=abs(op-cl)
        z=abs(lo-op)
        if y>x+z and y>df:
            return True
    return False


def isGoodProfit(op,cl,lo,hi):
    dl=0.1
    du=0.2
    if op>cl:
        x=abs(hi-op)
        y=abs(op-cl)
        z=abs(lo-cl)
        if y>x+z and y>df:
            return True
    else:
        x=abs(hi-cl)
        y=abs(op-cl)
        z=abs(lo-op)
        if y>x+z and y>df:
            return True
    return False

p_cnt=0
p_p_cnt=0
p_n_cnt=0

n_cnt=0
n_n_cnt=0
n_p_cnt=0

back_stat=False
back_dir=0

with open(fname) as f:
    while True:
        line=f.readline()
        line_dat=line.split(",")
        if line=="":
            break


        op=float(line_dat[2])
        cl=float(line_dat[5])
        hi=float(line_dat[3])
        lo=float(line_dat[4])
        stat=isPower(op,cl,lo,hi)

        dur=cl-op
        if dur<0 and stat:
            n_cnt+=1
        else:
            p_cnt+=1

        if back_stat==True and stat==True:
            if dur<0:
                if back_dir<0:
                    n_n_cnt+=1
                else:
                    p_n_cnt+=1
            else:
                if back_dir<0:
                    n_p_cnt+=1
                else:
                    p_p_cnt+=1
                    
        back_stat=stat
        back_dir=dur
           
        

        
print(f"Results for file: {fname}----------------")
#print(f"three after each other positive_candels   = {pos_pos_pos_cnt} ")
#print(f"three after each other negative_candels   = {neg_neg_neg_cnt} ")
chance_neg="%.2f"%(n_cnt/(p_cnt+n_cnt))
chance_pos="%.2f"%(p_cnt/(p_cnt+n_cnt))



print(f"P(positve moment)   = {chance_pos} ")
print(f"P(negative moment)   = {chance_neg} ")


#print(f"*four positive candel ofter each other = {pos_pos_pos_then_pos}")
#print(f"*four negative candel ofter each other = {neg_neg_neg_then_neg}")


px="%.2f"%(p_p_cnt/p_cnt)
py="%.2f"%(n_n_cnt/n_cnt)
print(f"P(positive moment and next positive moment) = {px}")
print(f"P(negative moment and next negative momnet) = {py}")


px="%.2f"%(p_n_cnt/p_cnt)
py="%.2f"%(n_p_cnt/n_cnt)
print(f"P(positive moment and next negative moment) = {px}")
print(f"P(negative moment and next positive momnet) = {py}")

#pz="%.2f"%((pos_pos_pos_then_pos+neg_neg_neg_then_neg)/(pos_pos_pos_cnt+neg_neg_neg_cnt))
#print(f"P(currnt candel similar three back candel) = {pz}")


#pz="%.2f"%((pos_pos_pos_then_neg+neg_neg_neg_then_pos)/(pos_pos_pos_cnt+neg_neg_neg_cnt))
#print(f"P(currnt candel diffrent three back candel) = {pz}")






