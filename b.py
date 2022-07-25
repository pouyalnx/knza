fname="XAUUSD5.csv"
data=[]
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
        hg=float(line_dat[3])
        lo=float(line_dat[4])

        rate=max(abs((hg-op+0.000001)/(lo-op+0.000001)),abs((lo-op+0.000001)/(hg-op+0.000001)))
        data.append([hour,rate,abs(hg-op+0.000001),abs(lo-op+0.000001)])

        
        cnt+=1
        if cnt==cnt_level:
            cnt=0
            print(f"{cnt_level} of data has been read")

data.sort()
print(data)
x="sax"
result="data2_first_v2.csv"
with open(result,"w") as f:
    for date in data:
        if date[0]!=x:
            pt="%.2f,v+%.2f,v-%.2f"%(date[1],date[2],date[3])
            resp=f"{date[0]}, {pt}"
            f.write(resp+"\n")
            x=date[0]
       # print(resp)
