"""TCP server on the Pico that receives FORWARD/BACKWARD commands and adjusts a servo angle."""

from stansmicropy.wifiManager import WiFiManager
from stansmicropy.servo import Servo
import time

servo = Servo(22)  # Servo on GP22

def main():
    SSID = "TS9T Stan"  # Replace with your Wi-Fi SSID
    PASSWORD = "stanislus29"  # Replace with your Wi-Fi password

    wifi_manager = WiFiManager(SSID, PASSWORD)
    print("Connected to Wi-Fi, IP address:", wifi_manager.wlan.ifconfig()[0])

    servo.oscillate(0,30)  # Start at neutral position

    status = wifi_manager.wait_for_client()

    if status is None:
        print("Failed to establish client connection.")
        return  # Exit if no client connected
    
    while True:
        command = wifi_manager.receive_command()
        print("Received command:", command)    

        if command == "FORWARD":
            servo.oscillate(0,90, step = 5, delay=0.2)  # Rotate right
        elif command == "BACKWARD":
            servo.oscillate(90,0, step = 5, delay=0.2)   # Rotate left

if __name__ == "__main__":
    main()
