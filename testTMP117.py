import machine
import time
import errno

#read temperature
vcc=machine.Pin(32,machine.Pin.OUT)
g=machine.Pin(33,machine.Pin.OUT)
g.value(0)
vcc.value(1)
i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25))

try:
    i2c.readfrom_mem(0x48, 0, 0)
except OSError as exc:
    print(exc.args[0])
finally:
    print("Temp sensor inited")
    
time.sleep(1)
tempInBytes=i2c.readfrom(0x48, 2)
print((int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125)

# put the device to sleep

