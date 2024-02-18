
import network
import usocket as socket
import machine

# Connect to WiFi
ssid = 'ssid_name'
password = 'password'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# Wait until connected to WiFi
while not station.isconnected():
    pass

print('Connected to WiFi')

# Define HTML response
html = """HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n
<!DOCTYPE html>
<html>
<head>
<title>ESP32 LED Control</title>
</head>
<body>
<h1>ESP32 LED Control</h1>
<p><a href="/led/on">Turn LED On</a></p>
<p><a href="/led/off">Turn LED Off</a></p>
</body>
</html>
"""

# Setup LED pin
led = machine.Pin(2, machine.Pin.OUT)

# Function to handle HTTP requests
def handle_request(client):
    request = client.recv(1024)
    request = str(request)

    if '/led/on' in request:
        led.on()
        response = 'LED turned on'
    elif '/led/off' in request:
        led.off()
        response = 'LED turned off'
    else:
        response = html

    client.send(response)
    client.close()

# Setup web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)

print('Web server started')

# Main loop
while True:
    client, addr = s.accept()
    handle_request(client)