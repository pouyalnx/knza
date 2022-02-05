from datetime import datetime,timedelta
from random import random
from random import uniform


diff=timedelta(hours=1)
start_price=1.2342
numbars=1000
numtick=60
changeprice=0.01
volume=1
infp=100000
infn=-10000
start_time=datetime(2017,1,1,0,0)


cl=start_price

outfile="XXXXX.csv"

with open(outfile,"w") as f:
    for i in range(numbars):
        op=cl
        hi=infn
        lo=infp

        for tick in range(numtick):
            cl=round(op+changeprice*uniform(-1,1),4)
            hi=max(hi,cl)
            lo=min(lo,cl)

        start_time+=diff
        date=start_time.strftime("%Y.%m.%d,%H:%M")
        line=f"{date},{op},{hi},{lo},{cl},{volume}"
        f.write(line+"\n")
