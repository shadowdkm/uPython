import machine
import time

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


time.sleep(1)
i2c.writeto(0x58,bytearray([0x36, 0x82]))
tempBuf=i2c.readfrom(0x58,10)
print(tempBuf)


i2c.writeto(0x58,bytearray([0x20, 0x1e,0x89,0x73,0xCA,0x8A,0xAE,0xAF]))
time.sleep_ms(100)

i2c.writeto(0x58,bytearray([0x20, 0x15]))
tempBuf=i2c.readfrom(0x58,10)
print("Baseline",tempBuf)

i2c.writeto(0x58,bytearray([0x20, 0x03]))
time.sleep_ms(300)
    
while True:
    


    i2c.writeto(0x58,bytearray([0x20, 0x08]))
    time.sleep_ms(300)
    tempBuf=i2c.readfrom(0x58,6)
    print(int(tempBuf[0])*256+int(tempBuf[1]),int(tempBuf[3])*256+int(tempBuf[4]))
    
    
    time.sleep_ms(100)
        
