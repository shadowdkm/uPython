
import utime
import struct

from machine import I2C, Pin

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

l=i2c.scan()

print(i2c.readfrom_mem(0x69, 0x75, 1)) #who am i
print(i2c.readfrom_mem(0x69, 0x00, 3))
print(i2c.readfrom_mem(0x69, 0x0D, 3))

i2c.writeto_mem(0x69, 0x1A, b'\x00, \x00, \x00, \x00, \x0A') #cfg Acc Samlping rate
i2c.writeto_mem(0x69, 0x6C, b'\x07') #turn on Acc, turn off Gyr

i2c.writeto_mem(0x69, 0x37, b'\x02') #connect to Mag
l=i2c.scan()

i2c.writeto_mem(0x0C, 0x0A, b'\x11') #enable Mag single read
print(i2c.readfrom_mem(0x0C, 0x10, 3)) #Mag Adj Val

for i in range(36000):
  reading=i2c.readfrom_mem(0x0C, 0x00, 10)
  i2c.writeto_mem(0x0C, 0x0A, b'\x11') #enable Mag single read
  mag=struct.unpack('hhh',reading[3:9])
  
  reading=i2c.readfrom_mem(0x69, 0x3B, 6)
  acc=struct.unpack('>hhh',reading)
  print(acc,mag)
  utime.sleep(0.1)

