from Libraries.ledclass import LED
import time

# External LED on GPIO 21
extLed = LED(21)

# Set fixed brightness (e.g., 50%)
extLed.setBrightness(50)

while True:
    # LED stays at 50% brightness
    pass