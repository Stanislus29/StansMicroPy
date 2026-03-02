"""Run OpenCV on PC to detect hand movements and send commands to MCU over Wi-Fi to control an LED."""

from stansmicropy.wifiManager import WiFiManager
from stansmicropy.led import LED
import time

led = LED(2)  # Onboard LED on GP2

def main():
    SSID = "TS9T Stan"  # Replace with your Wi-Fi SSID
    PASSWORD = "stanislus29"  # Replace with your Wi-Fi password

    wifi_manager = WiFiManager(SSID, PASSWORD)
    print("Connected to Wi-Fi, IP address:", wifi_manager.wlan.ifconfig()[0])

    status = wifi_manager.wait_for_client()

    if status is None:
        print("Failed to establish client connection.")
        return  # Exit if no client connected

    while True:
        command = wifi_manager.receive_command()
        print("Received command:", command)    

        if command == "FORWARD":
            led.on()
        elif command == "BACKWARD":
            led.off()

        # time.sleep(0.5)  # Simulate processing time, adjust as needed
        
if __name__ == "__main__":
    main()    