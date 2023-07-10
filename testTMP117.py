import machine
import time
import errno

#read temperature
vcc=machine.Pin(32,machine.Pin.OUT) #R
g=machine.Pin(33,machine.Pin.OUT)   #G
g2=machine.Pin(27,machine.Pin.OUT)   #G
g2.value(0)
g.value(0)
vcc.value(1)
time.sleep(1)
i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25))   #SCL B, SDA Y
#i2c = machine.I2C(scl=machine.Pin(14), sda=machine.Pin(12))   #SCL B, SDA Y

for i in range(0x48,0x4C):
    try:
        i2c.readfrom_mem(i, 0, 0)
    except OSError as exc:
        print("ERROR:", exc.args[0])
    finally:
        print("Temp sensor inited 0x%x"%i)

for i in range(0x48,0x4C):
    try:
        tempInBytes=i2c.readfrom(i, 2)
        print((int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125)
    except OSError as exc:
        print("ERROR:", exc)
  
