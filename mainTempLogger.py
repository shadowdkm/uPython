import machine
import time
import errno



#constants for exam temp stable
tempToleranceOver10s=0.1
minSecondInMode=300
minSecondAfterStable=300
timeResolution=1

#vals for exam temp stable
secondsInNewSetting=0
secondsAfterStable=0
B1s=[0]*20
B2s=[0]*20
E1s=[0]*20
E2s=[0]*20

def initI2C():
    for i in range(0x48,0x4A):
        try:
            tmpBody.readfrom_mem(i, 0, 0)
        except OSError as exc:
            print("tmpBody ERROR:", exc.args[0])
        finally:
            print("Body Temp sensor inited 0x%x"%i)
            
    for i in range(0x48,0x4A):
        try:
            tmpEnv.readfrom_mem(i, 0, 0)
        except OSError as exc:
            print("tmpEnv ERROR:", exc.args[0])
        finally:
            print("Env Temp sensor inited 0x%x"%i)
            
def TMPisStable(secondsInNewSetting):
    B1=0.0
    B2=0.0
    E1=0.0
    E2=0.0
    try:
        tempInBytes=tmpBody.readfrom(0x48, 2)
        B1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        #print("B1 %.2f"%B1)
    except OSError as exc:
        print("ERROR:", exc)
        
    try:
        tempInBytes=tmpBody.readfrom(0x49, 2)
        B2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        #print("B2 %.2f"%B2)
    except OSError as exc:
        print("ERROR:", exc)
        
    try:
        tempInBytes=tmpEnv.readfrom(0x48, 2)
        E1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        #print("E1 %.2f"%E1)
    except OSError as exc:
        print("ERROR:", exc)
        
    try:
        tempInBytes=tmpEnv.readfrom(0x49, 2)
        E2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
        #print("E2 %.2f"%E2)
    except OSError as exc:
        print("ERROR:", exc)
    
    print("[%ds]\tBody:\t%.2f\t%.2f\tEnv:\t%.2f\t%.2f"%(secondsInNewSetting,B1,B2,E1,E2))
    
    B1s.pop(0)
    B1s.append(B1)
    B2s.pop(0)
    B2s.append(B2)
    E1s.pop(0)
    E1s.append(E1)
    E2s.pop(0)
    E2s.append(E2)
    
    global secondsAfterStable
    if secondsInNewSetting>minSecondInMode and\
    max(B1s)-min(B1s)<tempToleranceOver10s and\
    max(B2s)-min(B2s)<tempToleranceOver10s and\
    max(E1s)-min(E1s)<tempToleranceOver10s and\
    max(E2s)-min(E2s)<tempToleranceOver10s:
        secondsAfterStable+=timeResolution
        if secondsAfterStable>minSecondAfterStable:
            return True
        else:
            return False    
    else:
        return False

    
def readDevice():
    while b.any():
        buf=b.readline()
        cbuf=str(buf, 'UTF-8')
        if "temp_center" in cbuf:
            print(cbuf)

#read temperature
vcc=machine.Pin(32,machine.Pin.OUT) #R
vcc2=machine.Pin(5,machine.Pin.OUT) #R
g=machine.Pin(33,machine.Pin.OUT)   #G
g2=machine.Pin(27,machine.Pin.OUT)   #G
g3=machine.Pin(18,machine.Pin.OUT)   #G
g3.value(0)
g2.value(0)
g.value(0)
vcc.value(0)
vcc2.value(0)
time.sleep(1)
vcc.value(1)
vcc2.value(1)
time.sleep(1)
tmpBody = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25),freq=100000)   #SCL B, SDA Y
tmpEnv = machine.I2C(scl=machine.Pin(14), sda=machine.Pin(15),freq=100000)    #SCL B, SDA Y
b = machine.UART(2, 115200)
if 'pwmBody' not in locals():
    pwmBody = machine.PWM(machine.Pin(2), freq=1000, duty=512)
    pwmEnv = machine.PWM(machine.Pin(4), freq=1000, duty=512)
pwmBody.duty(0)
pwmEnv.duty(0)

initI2C()
time.sleep(1)



#set PWM target Vals
pwmBodyCandidates=[0,100,250,400, 600, 800, 0]
pwmEnvCandidates=[0,100,250,400, 600, 800, 0]

for pwmBodyVal in pwmBodyCandidates:
    pwmBody.duty(pwmBodyVal)
    for pwmEnvVal in pwmBodyCandidates:
        vcc.value(0)
        vcc2.value(0)
        time.sleep(1)
        vcc.value(1)
        vcc2.value(1)
        time.sleep(1)

        pwmEnv.duty(pwmEnvVal)
        secondsInNewSetting=0
        secondsAfterStable=0
        
        time.sleep(1)
        readDevice()
        while not TMPisStable(secondsInNewSetting):
            readDevice()
            secondsInNewSetting+=timeResolution
            time.sleep(timeResolution)
    
