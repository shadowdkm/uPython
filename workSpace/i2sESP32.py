from machine import IIS

iis = IIS(IIS.RECORDER)
iis.init()
iis.set_sampwidth(24)
iis.set_framerate(16000)
iis.record(' /sd/2.wav',5)
