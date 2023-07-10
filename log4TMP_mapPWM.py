import machine
import time
import errno
from machine import Pin, PWM

# Ambient, 25.84,  device peri, 25.93, device central, 25.87, TE Body, 26.00,

offsetT1=0.86
offsetT3=0.96
offsetT4=0.91
offsetT2=1.09

stableTimeInSeconds=10
alwaysPrint=True
waitingForCoolingDown=True
bodyInitPWM=50
tBody=[]
tDev=[]
tDevP=[]
tExt=[]

def isArrayValStable(array, newVal):
    if len(array)>=stableTimeInSeconds:
        array.pop(0)
    array.append(newVal)
    if len(array)<5:
        return False
    
    avg=sum(array)/len(array)
    if len(array)==stableTimeInSeconds and max(array)-min(array)<0.05:
        return True
    else:        
        #print(len(array),max(array),min(array))
        return False

def readingIsValid(DevCenter,DevPeri,Body,Ambient):
    if Body>DevCenter-0.1 and DevCenter>DevPeri-0.1 and DevPeri>Ambient-0.1:
        return True
    elif Body<=DevCenter+0.1 and DevCenter<=DevPeri+0.1 and DevPeri<=Ambient+0.1:
        return True
    else:        
        return False
    


   
   
#read temperature
LED=machine.Pin(22,machine.Pin.OUT)
vcc=machine.Pin(32,machine.Pin.OUT)
g=machine.Pin(33,machine.Pin.OUT)
g.value(0)
vcc.value(0)
time.sleep(1)
vcc.value(1)
i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25),freq=100000)

time.sleep(3)

for i in range(0x48,0x4C):
    try:
        i2c.readfrom_mem(i, 0, 0)
    except OSError as exc:
        print(exc.args[0])
    finally:
        print("Temp sensor inited 0x%x"%i)

bodyPWM=70
extPWM=65

pwmBody = PWM(Pin(2), freq=20000, duty=1)
pwmBody.duty(bodyPWM)

pwmExt = PWM(Pin(0), freq=20000, duty=1)
pwmExt.duty(extPWM)

pbs=[1,2,1,1,2,3,4,3,2,1,1,2,3,4,5,6,5,4,3,2,1]
pes=[1,1,2,3,2,1,1,2,3,4,5,4,3,2,1,1,2,3,4,5,6]

index=0
while True:
    LED.value(1-LED.value())
    time.sleep(1)
    try:
        tempInBytes=i2c.readfrom(0x4A, 2)
        temp4=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125-offsetT4
        tempInBytes=i2c.readfrom(0x4B, 2)    
        temp3=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125-offsetT3
        
        tempInBytes=i2c.readfrom(0x48, 2)
        temp2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125-offsetT2
        tempInBytes=i2c.readfrom(0x49, 2)
        temp1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125-offsetT1
    except OSError as exc:
        #print(exc)
        continue
    
    if temp3<1 or temp4<1 or temp1<1 or temp2<1:
        vcc.value(0)
        time.sleep(1)
        vcc.value(1)        
        time.sleep(3)
        continue
    
    
    temperatureStable=isArrayValStable(tDev,temp4) and isArrayValStable(tDevP,temp3) and isArrayValStable(tBody,temp1)and isArrayValStable(tExt,temp2)
        
    #Ambient TE Body device peri device central

    if temperatureStable or alwaysPrint:
        print("%d, %0.2f, %d, %d, Ambient, %.2f,  device peri, %.2f, device central, %.2f, TE Body, %.2f,"
              %(temperatureStable, time.time()/60, pwmBody.duty(),pwmExt.duty(),temp1,temp3,temp4,temp2))
    
    if temperatureStable:
        index=index+1
        #if index>=len(pbs):
        #    break
        
        #bodyPWM=pbs[index]*50
        #extPWM=pes[index]*50
        #pwmBody.duty(bodyPWM)
        #pwmExt.duty(extPWM)
        time.sleep(0.5)
        tDev=[]
        tDevP=[]
        
      
        
pwmBody.duty(0)
pwmExt.duty(0)



