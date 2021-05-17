import machine

led = machine.PWM(machine.Pin(2), freq=1000)

led.duty(1)
