import network
import socket
from machine import Pin, PWM
import time

# --- Wi-Fi Config ---
SSID = "TS9T Stan"
PASSWORD = "stan29ccco"

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(0.5)
print("Connected, IP:", wlan.ifconfig()[0])

# Setup LED PWM (GPIO 15 example)
led = PWM(Pin(15))
led.freq(1000)

# Setup UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((wlan.ifconfig()[0], 5005))

print("Listening for brightness values...")

while True:
    data, addr = sock.recvfrom(1024)
    try:
        brightness = int(data.decode())
        brightness = max(0, min(255, brightness))  # Clamp 0-255
        led.duty_u16(brightness * 257)  # Convert 8-bit to 16-bit PWM
        print("Brightness set to:", brightness)
    except:
        pass