import machine
v5=machine.Pin(16,machine.Pin.OUT)
v12=machine.Pin(17,machine.Pin.OUT)


for i in range(0, 100):
    time.sleep(0.3)
    print(i)
    
    if i%4==0:
        v5.value(0)
    elif i%4==1:
        v12.value(0)
    elif i%4==2:
        v5.value(1)
    elif i%4==3:
        v12.value(1)
        
        