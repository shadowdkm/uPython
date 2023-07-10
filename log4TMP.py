import machine
import time
import errno

#read temperature
vcc=machine.Pin(32,machine.Pin.OUT)
g=machine.Pin(33,machine.Pin.OUT)
g.value(0)
vcc.value(1)
i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25),freq=100000)

time.sleep(3)

for i in range(0x48,0x4B):
    try:
        i2c.readfrom_mem(0x48, 0, 0)
    except OSError as exc:
        print(exc.args[0])
    finally:
        print("Temp sensor inited")


while True:
    time.sleep(1)
    tempInBytes=i2c.readfrom(0x4A, 2)
    temp4=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    tempInBytes=i2c.readfrom(0x4B, 2)    
    temp3=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    
    tempInBytes=i2c.readfrom(0x48, 2)
    temp1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    tempInBytes=i2c.readfrom(0x49, 2)
    temp2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    
    print(temp1,temp2,temp3,temp4)



