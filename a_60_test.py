fname="XAUUSD5.csv"


profit=0
loss=0
trade_cnt=0
times={
       "04:00":"short",
       "01:00":"short",

       "11:00":"short",
       "12:00":"long",
       "16:00":"long",
       "19:00":"long",
       "23:00":"long",
       "18:00":"short"
       }
date="x"
day_cnt=0
DAY_START=0
trade_days=0
with open(fname) as f:
    while True:
        line=f.readline()
        line_dat=line.split(",")
        if line=="":
            break

        if line_dat[0]!=date:
            day_cnt+=1
            date=line_dat[0]
            if day_cnt>DAY_START:
                trade_days+=1  
        if day_cnt<DAY_START:
            continue

        hour=line_dat[1]
        op=float(line_dat[2])
        cl=float(line_dat[5])
        if hour in times.keys():
            trade_cnt+=1
            if times[hour]=="long":
                if op>cl:
                    profit+=op-cl
                else:
                    loss+=cl-op
            else:
                if cl>op:
                    profit+=cl-op
                else:
                    loss+=op-cl

print("Results:----------------")
print(f"Profit = {profit//10} pipe")
print(f"loss   = {loss//10} pipe")
print(f"*total   = {(profit-loss)//10} pipe")
print(f"*count trades   = {trade_cnt} ")
print(f"*count days   = {trade_days} ")
