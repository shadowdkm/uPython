import machine
import time
import errno

#read temperature
vcc=machine.Pin(32,machine.Pin.OUT)
g=machine.Pin(33,machine.Pin.OUT)
g.value(0)
vcc.value(1)
i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25),freq=400000)

try:
    i2c.readfrom_mem(0x48, 0, 0)
    i2c.readfrom_mem(0x49, 0, 0)
except OSError as exc:
    print(exc.args[0])
finally:
    print("Temp sensor inited")
   
i2c.writeto(0x4A,bytearray([0x21, 0x30]))
i2c.writeto(0x4A,bytearray([0xE0, 0x00]))

while True:
    time.sleep(1)
    tempInBytes=i2c.readfrom(0x4A, 3)
    temp3=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.00267-45
    tempInBytes=i2c.readfrom(0x48, 2)
    temp1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    tempInBytes=i2c.readfrom(0x49, 2)
    temp2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
    
    print(temp1,temp2,temp3)



