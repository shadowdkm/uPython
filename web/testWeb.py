try:
    import usocket as socket
except:
    import socket
import random
import time

CONTENT = b"""\
HTTP/1.0 200 OK

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Document</title>
    <style>
        #chart_div {
            width: 1200px;
        }
        
        body {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
</head>
<body>
    <!-- CONTAINER FOR CHART -->
    <div id="chart_div"></div>
    <script type="text/javascript" loading="lazy" src="https://www.gstatic.com/charts/loader.js"></script>
    <script>
        // load current chart package
        google.charts.load("current", {
            packages: ["corechart", "line"]
        });
        // set callback function when api loaded
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {
            // create data object with default value
            let data = google.visualization.arrayToDataTable([
                ["Year", "CPU Usage"],
                [0, 0]
            ]);
            // create options object with titles, colors, etc.
            let options = {
                title: "CPU Usage",
                hAxis: {
                    title: "Time"
                },
                vAxis: {
                    title: "Usage"
                }
            };
            // draw chart on load
            let chart = new google.visualization.LineChart(
                document.getElementById("chart_div")
            );
            chart.draw(data, options);
            // interval for adding new data every 250ms
            let index = 0;
            setInterval(function() {
                // instead of this random, you can make an ajax call for the current cpu usage or what ever data you want to display
                let random = Math.random() * 30 + 20;
                data.addRow([index, random]);
                if(data.getNumberOfRows()>20)
                {
                    data.removeRow(0);
                }
                chart.draw(data, options);
                index++;
            }, 100);
        }
    </script>
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

        if not micropython_optimize:
            # To read line-oriented protocol (like HTTP) from a socket (and
            # avoid short read problem), it must be wrapped in a stream (aka
            # file-like) object. That's how you do it in CPython:
            client_stream = client_sock.makefile("rwb")
        else:
            # .. but MicroPython socket objects support stream interface
            # directly, so calling .makefile() method is not required. If
            # you develop application which will run only on MicroPython,
            # especially on a resource-constrained embedded device, you
            # may take this shortcut to save resources.
            client_stream = client_sock

        print("Request:")
        req = client_stream.readline()
        #print(req)
        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
                break
            print(h)
        client_stream.write(CONTENT)
        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
        counter += 1
        print()


main()

