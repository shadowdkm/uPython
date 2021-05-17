try:
    import usocket as socket
except:
    import socket
import random
import time
import machine

CONTENT = b"""\
HTTP/1.0 200 OK

<!DOCTYPE html>
<html>
<body>

<div id="demo">
<h1>The XMLHttpRequest Object</h1>
<button type="button" onclick="loadDoc()">Change Content</button>
</div>

<script>   
   var ajaxRequest = new XMLHttpRequest();  
   
   function ajaxLoad(ajaxURL)  
   {  
    ajaxRequest.open('GET',ajaxURL,true);  
    ajaxRequest.onreadystatechange = function()  
    {  
     if(ajaxRequest.readyState == 4 && ajaxRequest.status==200)  
     {  
      var ajaxResult = ajaxRequest.responseText;  
      var tmpArray = ajaxResult.split("|");  
      document.getElementById('temp').innerHTML = tmpArray[0];  
      document.getElementById('humi').innerHTML = tmpArray[1];  
     }  
    }  
    ajaxRequest.send();  
   }  
     
   function updateDHT()   
   {   
     ajaxLoad('getDHT');   
   }  
     
   setInterval(updateDHT, 250);  
    
  </script>  

<p>Temperature: <strong><span id='temp'>--.-</span> &deg;C</strong></p>  
<p>Humidity: <strong><span id='humi'>--.-</span> % </strong></p>
     
</body>
</html>
"""

def array2table():
    t=[]
    val=[]

    while len(val)<20:
        val.append(random.random())
        t.append(time.ticks_ms())

    dataString="['Time (ms)', 'Val'],\n"
    for i in range(20):
        dataString+="[%d, %.3f],\n"%(t[i],val[i])
        
    return dataString

def main(micropython_optimize=False):
    # setup hardware
    vcc=machine.Pin(32,machine.Pin.OUT)
    g=machine.Pin(33,machine.Pin.OUT)
    vcc.value(1)
    time.sleep(1)
    g.value(0)
    vcc.value(1)
    i2c = machine.I2C(scl=machine.Pin(26), sda=machine.Pin(25))
    vcc.value(1)
    time.sleep(1)
    i2c.writeto(0x44,bytearray([0x27, 0x21]))
    time.sleep(1)
    i2c.writeto(0x44,bytearray([0xE0, 0x00]))
    time.sleep(1)
    
    
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:80/")

    counter = 0
    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        request=client_sock.recv(1024)
        #print(req)
        request=str(request)
        update = request.find('/getDHT')
        if update == 6:
            try:
                tempBuf=i2c.readfrom(0x44,6)
                calcTemp=(int(tempBuf[0])*256+int(tempBuf[1]))*0.00267-45
                calcRH=(int(tempBuf[3])*256+int(tempBuf[4]))*0.001526
                t = random.random()
                h = random.random()
                response = str(calcTemp) + "|"+ str(calcRH)
            except:
                print("Sensor overload")
                response = "0|0"
                
            client_sock.send('HTTP/1.1 200 OK\n')
            client_sock.send('Content-Type: text/html\n')
            client_sock.send('Connection: close\n\n')
            client_sock.sendall(response)
        else:
            client_sock.send(CONTENT)
           
            
        client_sock.close()


main()

