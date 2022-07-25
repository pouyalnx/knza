fname="XAUUSD60.csv"


pos_cnt=0
pos_then_pos=0
pos_then_neg=0

neg_cnt=0
neg_then_pos=0
neg_then_neg=0

lst=0

with open(fname) as f:
    while True:
        line=f.readline()
        line_dat=line.split(",")
        if line=="":
            break


        op=float(line_dat[2])
        cl=float(line_dat[5])
        if op>cl:
            cur=1
        else:
            cur=-1

            
        if cur>0:
            pos_cnt+=1
            if lst>0:
                pos_then_pos+=1
            else:
                neg_then_pos+=1
        else:
            neg_cnt+=1
            if lst>0:
                pos_then_neg+=1
            else:
                neg_then_neg+=1
        lst=cur

        
print(f"Results for file: {fname}----------------")
print(f"positive_candels   = {pos_cnt} ")
print(f"negative_candels   = {neg_cnt} ")
chance_neg="%.2f"%(neg_cnt/(pos_cnt+neg_cnt))
chance_pos="%.2f"%(pos_cnt/(pos_cnt+neg_cnt))


print(f"P(positive)   = {chance_pos} ")
print(f"P(negative)   = {chance_neg} ")


print(f"*two positive candel ofter each other = {pos_then_pos}")
print(f"*two negative candel ofter each other = {neg_then_neg}")


px="%.2f"%(pos_then_pos/pos_cnt)
py="%.2f"%(neg_then_neg/neg_cnt)
print(f"P(currnt candel positve and next will be positvie) = {px}")
print(f"P(currnt candel negative and next will be negative) = {py}")


px="%.2f"%(pos_then_neg/pos_cnt)
py="%.2f"%(neg_then_pos/neg_cnt)
print(f"P(currnt candel positve and next will be negatie) = {px}")
print(f"P(currnt candel negative and next will be positvie) = {py}")

pz="%.2f"%((pos_then_pos+neg_then_neg)/(pos_cnt+neg_cnt))
print(f"P(currnt candel similar back candel) = {pz}")


pz="%.2f"%((pos_then_neg+neg_then_pos)/(pos_cnt+neg_cnt))
print(f"P(currnt candel diffrent back candel) = {pz}")






