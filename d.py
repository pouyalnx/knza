fname="XAUUSD240.csv"


pos_pos_cnt=0
pos_pos_then_pos=0
pos_pos_then_neg=0

neg_neg_cnt=0
neg_neg_then_pos=0
neg_neg_then_neg=0

lst1=0
lst2=0

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

            if lst1>0 and lst2>0:
                pos_pos_then_pos+=1
                pos_pos_cnt+=1
            elif lst1<0 and lst2<0:
                neg_neg_cnt+=1
                neg_neg_then_pos+=1
        else:
            if lst1>0 and lst2>0:
                pos_pos_then_neg+=1
                pos_pos_cnt+=1
            elif lst1<0 and lst2<0:
                neg_neg_cnt+=1
                neg_neg_then_neg+=1

        lst2=lst1
        lst1=cur
        

        
print(f"Results for file: {fname}----------------")
print(f"two after each other positive_candels   = {pos_pos_cnt} ")
print(f"two after each other negative_candels   = {neg_neg_cnt} ")
chance_neg="%.2f"%(neg_neg_cnt/(pos_pos_cnt+neg_neg_cnt))
chance_pos="%.2f"%(pos_pos_cnt/(pos_pos_cnt+neg_neg_cnt))


print(f"P(positive_positive)   = {chance_pos} ")
print(f"P(negative_negative)   = {chance_neg} ")


print(f"*three positive candel ofter each other = {pos_pos_then_pos}")
print(f"*three negative candel ofter each other = {neg_neg_then_neg}")


px="%.2f"%(pos_pos_then_pos/pos_pos_cnt)
py="%.2f"%(neg_neg_then_neg/neg_neg_cnt)
print(f"P(currnt and back candel positve and next will be positvie) = {px}")
print(f"P(currnt and back candel negative and next will be negative) = {py}")


px="%.2f"%(pos_pos_then_neg/pos_pos_cnt)
py="%.2f"%(neg_neg_then_pos/neg_neg_cnt)
print(f"P(currnt and back  candel positve and next will be negatie) = {px}")
print(f"P(currnt and back  candel negative and next will be positvie) = {py}")

pz="%.2f"%((pos_pos_then_pos+neg_neg_then_neg)/(pos_pos_cnt+neg_neg_cnt))
print(f"P(currnt candel similar two back candel) = {pz}")


pz="%.2f"%((pos_pos_then_neg+neg_neg_then_pos)/(pos_pos_cnt+neg_neg_cnt))
print(f"P(currnt candel diffrent two back candel) = {pz}")






