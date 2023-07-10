import machine
import time
import errno
from machine import Pin, PWM

stableTimeInSeconds=10
alwaysPrint=True
waitingForCoolingDown=True
bodyInitPWM=50
tBpdy=[]
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
    if len(array)==stableTimeInSeconds and max(array)-min(array)<0.1:
        return True
    else:        
        #print(len(array),max(array),min(array))
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

bodyPWM=bodyInitPWM
extPWM=0

pwmBody = PWM(Pin(2), freq=20000, duty=10)
pwmBody.duty(bodyPWM)

pwmExt = PWM(Pin(0), freq=20000, duty=10)
pwmExt.duty(extPWM)

while True:
    LED.value(1-LED.value())
    time.sleep(1)
    try:
        tempInBytes=i2c.readfrom(0x4A, 2)
        temp4=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        tempInBytes=i2c.readfrom(0x4B, 2)    
        temp3=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        
        tempInBytes=i2c.readfrom(0x48, 2)
        temp1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        tempInBytes=i2c.readfrom(0x49, 2)
        temp2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    except OSError as exc:
        #print(exc)
        continue
    
    if temp3<1 or temp4<1:
        vcc.value(0)
        time.sleep(1)
        vcc.value(1)        
        time.sleep(3)
        continue
    
    if waitingForCoolingDown:
        if temp1<27 and temp2<27 and temp3<27 and temp4<27:
            waitingForCoolingDown=False               
            pwmBody.duty(bodyPWM)
            pwmExt.duty(extPWM)
        else:
            pwmBody.duty(0)
            pwmExt.duty(0)
            print("%d, %d, %d, %d, Ambient, %.2f,  device peri, %.2f, device central, %.2f, TE Body, %.2f,"%(-1, time.time(), pwmBody.duty(),pwmExt.duty(),temp1,temp3,temp4,temp2))
            continue
    
    if readingIsValid(temp4,temp3,temp2,temp1):
        temperatureStable=isArrayValStable(tDev,temp4) and isArrayValStable(tDevP,temp3)
    else:
        temperatureStable=False
        tDev=[]
        tDevP=[]
        
    #Ambient TE Body device peri device central

    if temperatureStable or alwaysPrint:
        print("%d, %d, %d, %d, Ambient, %.2f,  device peri, %.2f, device central, %.2f, TE Body, %.2f,"%(temperatureStable, time.time(), pwmBody.duty(),pwmExt.duty(),temp1,temp3,temp4,temp2))
    
    if temperatureStable:
        bodyPWM=bodyPWM+50 #should be 20
        pwmBody.duty(bodyPWM)
        time.sleep(0.5)
        tDev=[]
        tDevP=[]       
        
    if bodyPWM>=250: #should be >=300, mapping to 45 degree  or temp4>45
        bodyPWM=bodyInitPWM    
        extPWM+=50
        waitingForCoolingDown=True
        
        time.sleep(0.5)
        
    if extPWM>300 : #or temp3>45
        break
        
pwmBody.duty(0)
pwmExt.duty(0)



