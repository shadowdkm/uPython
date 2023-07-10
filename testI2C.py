import machine
vcc=machine.Pin(32,machine.Pin.OUT)
g=machine.Pin(33,machine.Pin.OUT)
g.value(0)
vcc.value(1)
i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25), freq=100000)













while True:
    print('Scan i2c bus...')
    devices = i2c.scan()

    if len(devices) == 0:
      print("No i2c device !")
    else:
      print('i2c devices found:',len(devices))

      for device in devices:  
        print("Decimal address: ",device," | Hexa address: ",hex(device))
