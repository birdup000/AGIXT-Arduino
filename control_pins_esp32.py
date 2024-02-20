import requests
import time

ESP32_IP = '0.0.0.0'  # Replace with your ESP32's IP address

def control_pin(pin, state):
    try:
        if state == 1:
            response = requests.get(f'http://{ESP32_IP}/pin/{pin}/on')
        elif state == 0:
            response = requests.get(f'http://{ESP32_IP}/pin/{pin}/off')
        
        response.raise_for_status()  # Raise an exception for non-200 status codes
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

while True:
    user_input = input("Enter pin number and state (e.g., '2 on', '4 off') or 'q' to quit: ")
    if user_input.lower() == 'q':
        break
    elif user_input.strip():
        try:
            pin, state = user_input.strip().split()
            pin = int(pin)
            if state.lower() == 'on':
                control_pin(pin, 1)
            elif state.lower() == 'off':
                control_pin(pin, 0)
            else:
                print("Invalid input. Please enter 'on' or 'off' for state.")
        except ValueError:
            print("Invalid input format. Please enter pin number followed by state (e.g., '2 on').")
        except Exception as e:
            print("Error:", e)
