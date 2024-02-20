import requests
import time

ESP32_IP = '192.168.0.53'  # Replace with your ESP32's IP address

def turn_led(state):
    try:
        if state == 1:
            response = requests.get(f'http://{ESP32_IP}/led/on')
        elif state == 0:
            response = requests.get(f'http://{ESP32_IP}/led/off')
        
        response.raise_for_status()  # Raise an exception for non-200 status codes
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        
while True:
    user_input = input("Press any key to turn the LED on or off (q to quit): ")
    if user_input.lower() == 'q':
        break
    elif user_input.strip():
        state = int(user_input.strip())  # Convert user input to integer
        if state in (0, 1):
            turn_led(state)
            time.sleep(1)
        else:
            print("Invalid input. Please enter 0 to turn off or 1 to turn on.")
