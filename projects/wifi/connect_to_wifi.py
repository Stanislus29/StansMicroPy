"""Test file to connect to wifi and print the IP address."""

from stansmicropy.wifiManager import WiFiManager
from stansmicropy.led import LED

def main():
    SSID = "TS9T Stan"  # Replace with your Wi-Fi SSID
    PASSWORD = "stanislus29"  # Replace with your Wi-Fi password

    wifi_manager = WiFiManager(SSID, PASSWORD)
    print("Connected to Wi-Fi, IP address:", wifi_manager.wlan.ifconfig()[0])