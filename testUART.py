import machine
import ustruct
from time import sleep

g3=machine.Pin(18,machine.Pin.OUT)   #G
g3.value(0)
sleep(1)

b = machine.UART(2, 115200)

for t in range(3):
    sleep(1)
    while b.any():
        buf=b.readline()
        cbuf=str(buf, 'UTF-8')
        if "temp_center" in cbuf:
            print(cbuf)
