from machine import Pin, PWM

pwmBody = PWM(Pin(0), freq=20000, duty=512)

#given 12V 3A Max on the pwoer supply
# PWM 500/1024 already produces full load.

pwmBody.duty(100)
