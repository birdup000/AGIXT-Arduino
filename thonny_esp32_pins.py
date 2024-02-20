import network
import usocket as socket
import machine

# Connect to WiFi
ssid = 'your_wifi_ssid'
password = 'your_wifi_password'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# Wait until connected to WiFi
while not station.isconnected():
    pass

print('Connected to WiFi')

# Define HTML response
html_template = """HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n
<!DOCTYPE html>
<html>
<head>
<title>ESP32 Pin Control</title>
</head>
<body>
<h1>ESP32 Pin Control</h1>
%s
</body>
</html>
"""

# Function to generate HTML for controlling individual pins
def generate_control_html(pin):
    return f"<p><a href='/pin/{pin}/on'>Turn Pin {pin} On</a></p>\n<p><a href='/pin/{pin}/off'>Turn Pin {pin} Off</a></p>\n"

# Setup web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)

print('Web server started')

# Main loop
while True:
    client, addr = s.accept()
    request = client.recv(1024).decode('utf-8')
    if request:
        request_parts = request.split(' ')
        if len(request_parts) > 1:
            method = request_parts[0]
            path = request_parts[1]
            if method == 'GET':
                if path == '/':
                    # Display control options for all pins
                    pin_controls = ''.join([generate_control_html(pin) for pin in range(40)])  # Considering GPIO0 to GPIO39
                    response = html_template % pin_controls
                elif path.startswith('/pin/'):
                    # Control individual pins
                    parts = path.split('/')
                    if len(parts) == 4:
                        pin = int(parts[2])
                        action = parts[3]
                        if action == 'on':
                            machine.Pin(pin, machine.Pin.OUT).on()
                            response = f'Pin {pin} turned on'
                        elif action == 'off':
                            machine.Pin(pin, machine.Pin.OUT).off()
                            response = f'Pin {pin} turned off'
                        else:
                            response = 'Invalid action'
                    else:
                        response = 'Invalid request'
                else:
                    response = '404 Not Found'
            else:
                response = '405 Method Not Allowed'
        else:
            response = '400 Bad Request'
    else:
        response = '500 Internal Server Error'

    client.send(response)
    client.close()
