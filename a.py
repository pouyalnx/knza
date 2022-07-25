fname="XAUUSD60.csv"
data={}
cnt_level=1000
cnt=0
with open(fname) as f:
    while True:
        line=f.readline()
        line_dat=line.split(",")
        if line=="":
            break

        hour=line_dat[1]
        op=float(line_dat[2])
        cl=float(line_dat[5])
        if not(hour in data):
            data[hour]=[0,0]

        if op>cl:
            data[hour][1]+=1
        else:
            data[hour][0]+=1

        cnt+=1
        if cnt==cnt_level:
            cnt=0
            print(f"{cnt_level} of data has been read")

print(data)
result="data60.csv"
with open(result,"w") as f:
    for date,dat in data.items():
        pt="%.2f"%((dat[0]+1)/(dat[1]+dat[0]))
        ptq="%.2f"%((dat[1]+1)/(dat[1]+dat[0]))
        resp=f"{date}, +:{dat[0]}, -:{dat[1]}, p(+):{pt}, p(-):{ptq}"
        f.write(resp+"\n")
        print(resp)
