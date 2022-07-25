fname="XAUUSD240.csv"


#       |
#   X   |
#      | |
#   Y  | | 
#      | |
#       |
#    Z  |
#       |

p_cont=0
n_cont=0

level=4.5
z_cond=0.5

def isContinue(op,cl,hi,lo):
    global p_cont,n_cont
    if cl>op:
        x=abs(hi-cl)
        y=abs(op-cl)
        z=abs(lo-op)
    else:
        x=abs(hi-op)
        y=abs(op-cl)
        z=abs(lo-cl)        

    if x>level*z and z>=z_cond:
        p_cont+=1
    elif z>level*x and z>=z_cond:
        n_cont+=1


c_cnt=0
with open(fname) as f:
    while True:
        line=f.readline()
        line_dat=line.split(",")
        if line=="":
            break
        c_cnt+=1

        op=float(line_dat[2])
        cl=float(line_dat[5])
        hi=float(line_dat[3])
        lo=float(line_dat[4])
        isContinue(op,cl,hi,lo)
        

print(f"**count of all candel : {c_cnt}")
print(f"+conitune: {p_cont}")
print(f"-conitune: {n_cont}")

print(f"next is +cont {(100*p_cont)//c_cnt}")
print(f"next is -cont {(100*n_cont)//c_cnt}")
#print(level_area)
