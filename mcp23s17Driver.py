from machine import Pin, SoftSPI
from machine import Pin
from time import sleep, sleep_ms

buf = bytearray(3)      # create a buffer

pcs = Pin(18, Pin.OUT)    # create output pin on GPIO0
pcs.on()
sleep_ms(1)
# construct a SoftSPI bus on the given pins
# polarity is the idle state of SCK
# phase=0 means sample on the first edge of SCK, phase=1 means the second
spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(4), miso=Pin(2))

spi.init(baudrate=500000) # set the baudrate


buf = bytearray(3)     # create a buffer

def spiWrite(addr, reg, val):
    buffer3 = bytearray(3)
    pcs.off()
    sleep_ms(3)
    spi.write_readinto(bytearray([addr, reg, val]), buffer3) # write to MOSI and read from MISO into the buffer
    pcs.on()
    sleep_ms(10)
    return buffer3
   
   
for addr in range(0x41,0x4F,2):
    print("----------0x%02x-----------"%addr)
    for reg in range(0x00,0x1A,1):
        buf=spiWrite(addr,reg,0x00)
        print("0x%02x: 0x%02x -> 0x%02x"%(addr,reg,buf[2]))
 
    
for addr in range(0x40,0x4F,2):
    spiWrite(addr,0x00,0x11)
    spiWrite(addr,0x01,0x00) 
    spiWrite(addr,0x13,0x00)
    spiWrite(addr,0x05,0x2A)
    spiWrite(addr,0x0A,0x2A)

sleep(3)
for addr in range(0x40,0x4F,2):
    spiWrite(addr,0x13,0xFF)