import network, socket, machine, utime
from machine import Pin, PWM

# --- Connect to Wi-Fi ---
SSID = "TS9T Stan"
PASSWORD = "stan29ccco"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    utime.sleep(1)
print("Connected:", wlan.ifconfig())

# --- Setup servo on GP15 ---
servo = PWM(Pin(15))
servo.freq(50)

# Function to set angle
def set_angle(angle):
    duty = int((angle / 180 * 2000) + 500)   # 500-2500us
    servo.duty_u16(int(duty * 65535 / 20000))

angle = 90  # start at center
set_angle(angle)

# --- Start TCP server ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 12345))
server.listen(1)
print("Waiting for connection...")
conn, addr = server.accept()
print("Connected by", addr)

# --- Receive commands and move servo ---
while True:
    data = conn.recv(1024).decode('utf-8').strip()
    if data:
        print("Received:", data)
        if data == "FORWARD":
            angle = min(180, angle + 10)  # rotate right
        elif data == "BACKWARD":
            angle = max(0, angle - 10)    # rotate left
        set_angle(angle)