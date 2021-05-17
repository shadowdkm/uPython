from machine import I2S
from machine import Pin
import struct
from time import sleep
import math
import binascii

bck_pin = Pin(14)  # Bit clock output
ws_pin = Pin(13)   # Word clock output
sdin_pin = Pin(12) # Serial data input


audio_in = I2S(I2S.NUM0,                                 # create I2S peripheral to read audio
               bck=bck_pin, ws=ws_pin, sdin=sdin_pin,    # sample data from an INMP441
               standard=I2S.PHILIPS, mode=I2S.MASTER_RX, # microphone module 
               dataformat=I2S.B32,                       
               channelformat=I2S.ONLY_LEFT,
               samplerate=16000, 
               dmacount=16,dmalen=256)
               
samples = bytearray(2048)                                # bytearray to receive audio samples


for p in range(1000):
    num_bytes_read = audio_in.readinto(samples)              # read audio samples from microphone
                                                             # note:  blocks until sample array is full
                                                             # - see optional timeout argument
                                                             # to configure maximum blocking duration
    #print(samples)
    sumv=0
    for i in range(1027,num_bytes_read-4,4):
#         print(binascii.hexlify(bytearray(samples[i:i+4])))
#         sleep(0.01)
        v=struct.unpack(">l",samples[i:i+4])[0]/256
        v=(v+2**23)%2**24-2**23
        sumv+=abs(v)
        n=math.ceil(math.log(sumv,10))
        
    print(sumv)
