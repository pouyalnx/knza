fname="XAUUSD240.csv"


#       |
#   X   |
#      | |
#   Y  | | 
#      | |
#       |
#    Z  |
#       |

MAXCHANGE=25
N_candel=6
candel_buffer=[]
MIN_AREA=5


def isLevel():
    hi=-100000
    lo=1000000
    for candel in candel_buffer:
        hc=candel[0]
        lc=candel[1]
        hi=max(hc,hi)
        lo=min(lc,lo)
        dif=hi-lo
        if dif>MAXCHANGE:
            return (0,hi,lo)
    return (1,hi,lo)


level_seq=[0]
#we should add level area
level_area=[]
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

        candel_buffer.append([max(op,cl),min(op,cl)])

        if len(candel_buffer)>N_candel:
            candel_buffer.pop(0)
            stat=isLevel()
            if level_seq[-1]!=stat[0]:
                level_seq.append(stat[0])
                if stat[0]==1:
                    flag=True
                    hx=stat[1]
                    lx=stat[2]
                    for i in range(len(level_area)):
                        hz=level_area[i][0]
                        lz=level_area[i][1]

                        if hx>=hz and lx<=lz:
                            level_area[i][0]=hx
                            level_area[i][1]=lx
                            flag=False
                            break
                        if hz>=hx and lz<=lx:
                            flag=False
                            break
                        
                        if hx>=hz and lx>=lz and lx<=hz:
                            level_area[i][0]=hx
                            flag=False
                            break
                        
                        if lx<=lz and hx>=lz and hx<=hz:
                            level_area[i][1]=lx
                            flag=False
                            break

                        if abs(lx-hz)<MIN_AREA or abs(lz-hx)<MIN_AREA:
                            level_area[i][0]=max(hx,hz)
                            level_area[i][1]=min(lx,lz)
                            flag=False
                            break
                if flag:
                    level_area.append([hx,lx])
print(f"***number of in range candels: {N_candel} ****")
print(f"***area price diffrence: {MAXCHANGE} USD***")

print(f"num of candels: {c_cnt} or {c_cnt//6} days")
print(f"num of levels touch for in range candel : {sum(level_seq)}")
print(f"num of unique levels  : {len(level_area)}")

#print(level_area)
