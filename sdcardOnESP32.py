

from machine import Pin, SPI
import machine, sdcard, os
# construct an SPI bus on the given pins
# polarity is the idle state of SCK
# phase=0 means sample on the first edge of SCK, phase=1 means the second
spi = SPI(-1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

sd = sdcard.SDCard(spi, machine.Pin(5))
print("Sd working")
os.mount(sd,"/SDCard")

f = open('/SDCard/data.txt', 'a+')
f.write('some data')
f.close()

