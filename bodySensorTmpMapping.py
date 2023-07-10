import machine
import time
import errno

def initI2C():
    for i in range(0x48,0x4A):
        try:
            tmpBody.readfrom_mem(i, 0, 0)
        except OSError as exc:
            print("ERROR:", exc.args[0])
        finally:
            print("Body Temp sensor inited 0x%x"%i)
            
    for i in range(0x48,0x4A):
        try:
            tmpEnv.readfrom_mem(i, 0, 0)
        except OSError as exc:
            print("ERROR:", exc.args[0])
        finally:
            print("Env Temp sensor inited 0x%x"%i)
            
def readTMP():
    try:
        tempInBytes=tmpBody.readfrom(0x48, 2)
        B1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    except OSError as exc:
        print("ERROR:", exc)
        
    try:
        tempInBytes=tmpBody.readfrom(0x49, 2)
        B2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    except OSError as exc:
        print("ERROR:", exc)
        
    try:
        tempInBytes=tmpEnv.readfrom(0x48, 2)
        E1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    except OSError as exc:
        print("ERROR:", exc)
        
    try:
        tempInBytes=tmpEnv.readfrom(0x49, 2)
        E2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    except OSError as exc:
        print("ERROR:", exc)
        
    print("Body:\t%.2f\t%.2f\tEnv:\t%.2f\t%.2f"%(B1,B2,E1,E2))

#read temperature
vcc=machine.Pin(32,machine.Pin.OUT) #R
vcc2=machine.Pin(5,machine.Pin.OUT) #R
g=machine.Pin(33,machine.Pin.OUT)   #G
g2=machine.Pin(27,machine.Pin.OUT)   #G
g3=machine.Pin(18,machine.Pin.OUT)   #G
g3.value(0)
g2.value(0)
g.value(0)
vcc.value(1)
vcc2.value(1)
time.sleep(1)
tmpBody = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25))   #SCL B, SDA Y
tmpEnv = machine.I2C(scl=machine.Pin(14), sda=machine.Pin(12))   #SCL B, SDA Y

initI2C()
time.sleep(1)
  
for i in range(1,10):
    readTMP()
    time.sleep(1)