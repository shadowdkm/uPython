import machine
import time
import errno
from machine import Pin, PWM

stableTimeInSeconds=5
alwaysPrint=True
waitingForCoolingDown=True
bodyInitPWM=50
tBody=[]
tDev=[]
tDevP=[]
tExt=[]

def trend(array, newVal):
    if len(array)>=stableTimeInSeconds:
        array.pop(0)
    array.append(newVal)
    if len(array)<5:
        return 0
    
    
    if len(array)>= 3 and array[2]-array[0]>0:
        return 1
    elif len(array)>= 3 and array[2]-array[0]<0:
        return -1
    else:        
        return False

def readingIsValid(DevCenter,DevPeri,Body,Ambient):
    if Body>DevCenter and DevCenter>DevPeri and DevPeri>Ambient:
        return True
    elif Body<=DevCenter and DevCenter<=DevPeri and DevPeri<=Ambient:
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

bodyPWM=40
extPWM=30

pwmBody = PWM(Pin(2), freq=20000, duty=1)
pwmBody.duty(bodyPWM)

pwmExt = PWM(Pin(0), freq=20000, duty=1)
pwmExt.duty(extPWM)

targetBodyTemp=33.5
targetAmbTemp=33

timetoAdjustPWM=10
while True:
    
    LED.value(1-LED.value())
    time.sleep(1)
    try:
        tempInBytes=i2c.readfrom(0x4A, 2)
        temp4=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        tempInBytes=i2c.readfrom(0x4B, 2)    
        temp3=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        
        tempInBytes=i2c.readfrom(0x48, 2)
        temp2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125 #Amb
        tempInBytes=i2c.readfrom(0x49, 2)
        temp1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125 #Body
    except OSError as exc:
        #print(exc)
        continue
    
    
    if timetoAdjustPWM>0:
        timetoAdjustPWM=timetoAdjustPWM-1
    else:
        timetoAdjustPWM=5
        
        '''if temp1<targetAmbTemp-0.1:
            extPWM=extPWM+1
            pwmExt.duty(extPWM)
        elif temp1>targetAmbTemp+0.1 and extPWM>0:
            extPWM=extPWM-1
            pwmExt.duty(extPWM)
            
        #print(temp2,targetBodyTemp)
        if temp2<targetBodyTemp-0.1 and bodyPWM>0:
            bodyPWM=bodyPWM+1
            pwmBody.duty(bodyPWM)
        elif temp2>targetBodyTemp+0.1:
            bodyPWM=bodyPWM-1
            pwmBody.duty(bodyPWM)'''
            
    if temp1<1 or temp2<1 or temp3<1 or temp4<1:
        vcc.value(0)
        time.sleep(1)
        vcc.value(1)        
        time.sleep(3)
        continue
            
        
    print("%d, %d, %d, %d, Ambient, %.2f,  device peri, %.2f, device central, %.2f, TE Body, %.2f,"%(timetoAdjustPWM, time.time(), pwmBody.duty(),pwmExt.duty(),temp1,temp3,temp4,temp2))
        
    