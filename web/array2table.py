import random
import time

t=[]
val=[]

while len(val)<20:
    val.append(random.random())
    t.append(time.ticks_ms())

dataString="['Time (ms)', 'Val'],"
for i in range(20):
    dataString+="[%d, %.3f],\n"%(t[i],val[i])
    
print(dataString)

    
