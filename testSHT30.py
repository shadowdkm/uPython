import machine
import time

vcc=machine.Pin(32,machine.Pin.OUT)
g=machine.Pin(33,machine.Pin.OUT)
g.value(0)
vcc.value(1)
i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25))

while True:
    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
      print("No i2c device !")
    else:
      print('i2c devices found:',len(devices))     

      for device in devices:  
        print("Decimal address: ",device," | Hexa address: ",hex(device))
        
      break


vcc.value(1)
time.sleep(1)
i2c.writeto(0x44,bytearray([0x27, 0x21]))
time.sleep(1)
i2c.writeto(0x44,bytearray([0xE0, 0x00]))
time.sleep(1)

while True:  
    tempBuf=i2c.readfrom(0x44,6)
    calcTemp=(int(tempBuf[0])*256+int(tempBuf[1]))*0.00267-45
    calcRH=(int(tempBuf[3])*256+int(tempBuf[4]))*0.001526
    print("Temp %.2f, RH %.2f"%(calcTemp,calcRH))
    
    time.sleep_ms(100)
    