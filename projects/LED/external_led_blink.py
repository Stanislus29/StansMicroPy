"""Blink an external LED on GPIO 21 at 0.2-second intervals using the LED library."""

from stansmicropy.led import LED
import time

# External LED connected to GPIO 21
extLed = LED(21)

# Blink external LED endlessly
extLed.blink(delay=0.2)  # Faster blink

while True:
    extLed.update()