tempInBytes=i2c.readfrom(0x4A, 2)
temp4=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
tempInBytes=i2c.readfrom(0x4B, 2)    
temp3=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125

tempInBytes=i2c.readfrom(0x48, 2)
temp1=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125
tempInBytes=i2c.readfrom(0x49, 2)
temp2=(int(tempInBytes[0])*256+int(tempInBytes[1]))*0.0078125

print("%d, %d, %d, %d, Ambient, %.2f,  device peri, %.2f, device central, %.2f, TE Body, %.2f,"%(-1, time.time(), pwmBody.duty(),pwmExt.duty(),temp1,temp3,temp4,temp2))

