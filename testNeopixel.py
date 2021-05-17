import machine, neopixel
import random
import time
np = neopixel.NeoPixel(machine.Pin(4), 8)

np[0] = (10, 0, 0) # set to red, full brightness
np[1] = (0, 10, 0) # set to green, half brightness
np[2] = (0, 0, 10)  # set to blue, quarter brightness

np.write()

for i in range(100):
    for led in range(5):
        np[led]=(random.getrandbits(4),random.getrandbits(4),random.getrandbits(4))
    np.write()
    time.sleep(0.01)
    
np[0] = (0, 0, 0) # set to red, full brightness
np[1] = (0, 0, 0) # set to green, half brightness
np[2] = (0, 0, 0)  # set to blue, quarter brightness

np.write()