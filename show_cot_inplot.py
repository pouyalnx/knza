from cProfile import label
from pydoc import locate
import matplotlib.pyplot as plt

x=[202101,202102,202103,202104,202105,202106,202107,202108,202109,202110,202111,202112,202201,202202]
short=[206,198,174,173,159,166,160,184,189,172,178,181,172,171]
long=[49,51,51,50,51,49,52,60,57,56,50,50,49,58]

plt.plot(x,short,'r-',label="short")
plt.plot(x,long,'b-',label="long")
plt.legend(loc='upper left')
 
# add the header
plt.title('COT of Banks')
 
# display the chart
plt.show()