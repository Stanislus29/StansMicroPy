"""Use Wi-Fi to receive brightness values from a client and control an LED."""

from stansmicropy.wifiManager import WiFiManager
from stansmicropy.led import LED
import time

led = LED(22)  # Onboard LED on GP2

def main():
    SSID = "TS9T Stan"  # Replace with your Wi-Fi SSID
    PASSWORD = "stanislus29"  # Replace with your Wi-Fi password

    wifi_manager = WiFiManager(SSID, PASSWORD)
    print("Connected to Wi-Fi, IP address:", wifi_manager.wlan.ifconfig()[0])

    status = wifi_manager.wait_for_client()

    if status is None:
        print("Failed to establish client connection.")
        return  # Exit if no client connected
    
    last_brightness = None

    while True:
        brightness_str = wifi_manager.receive_command()
        if brightness_str is None:
            continue

        try:
            brightness = int(brightness_str)
            brightness = max(0, min(255, brightness))  # Clamp safety
        except ValueError:
            continue

        # print("Received brightness:", brightness)

        # First iteration setup
        if last_brightness is None:
            last_brightness = brightness
            continue

        # Convert both to percent
        last_percent = int((last_brightness / 255) * 100)
        new_percent = int((brightness / 255) * 100)

        if brightness > last_brightness:
            # Fade UP
            print(f"Fading UP from {last_percent}% to {new_percent}%")
            led.fade(minP=last_percent, maxP=new_percent, step=10, delay=1)

        elif brightness < last_brightness:
            # Fade DOWN
            print(f"Fading DOWN from {last_percent}% to {new_percent}%")
            led.fade(minP=new_percent, maxP=last_percent, step=10, delay=1)

        # Update last value AFTER fade
        last_brightness = brightness


if __name__ == "__main__":
    main()