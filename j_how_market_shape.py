fname="XAUUSD240.csv"

op=-1
cl=-1
hi=-9999999999
lo=99999999999


with open(fname) as f:
    while True:
        line=f.readline()
        line_dat=line.split(",")
        if line=="":
            break
   
        opc=float(line_dat[2])
        clc=float(line_dat[5])
        hic=float(line_dat[3])
        loc=float(line_dat[4])
        if op==-1:
            op=opc
        cl=clc
        hi=max(hi,hic)
        lo=min(lo,loc)
        

print(op)
print(lo)
print(hi)
print(cl)

if cl>op:
    kind="high"
    x=hi-cl
    y=cl-op
    z=op-lo
    s=x+y+z
else:
    kind="low"
    x=hi-op
    y=op-cl
    z=cl-op
    s=x+y+z    

print(f"type:{kind}")
print(f"x={100*x/s}")
print(f"y={100*y/s}")
print(f"z={100*z/s}")
print(f"x+y+z={s}")
