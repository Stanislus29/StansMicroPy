import network
import socket

# --- Wi-Fi credentials ---
SSID = "Your WIFI name"
PASSWORD = "Your WIFI password"

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print("Connected to Wi-Fi:", wlan.ifconfig())
# wlan.ifconfig()[0] gives Pico IP address

# --- Create TCP server ---
s = socket.socket()
s.bind(('0.0.0.0', 12345))
s.listen(1)
print("Listening for connection...")

conn, addr = s.accept()
print("Connected by", addr)

# --- Handle incoming data ---
while True:
    data = conn.recv(1024)
    if not data:
        break
    message = data.decode('utf-8').strip()
    print("Received:", message)
    # Here you could control OLED, LED, etc.