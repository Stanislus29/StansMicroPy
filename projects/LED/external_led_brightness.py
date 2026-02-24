"""Set an external LED on GPIO 21 to 50% brightness using PWM."""

from stansmicropy.led import LED
import time

# External LED on GPIO 21
extLed = LED(22)

# Set fixed brightness (e.g., 50%)
extLed.setBrightness(50)

while True:
    # LED stays at 50% brightness
    pass