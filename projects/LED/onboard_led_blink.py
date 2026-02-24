"""Blink the Pico's onboard LED at 0.5-second intervals using the LED library."""

from stansmicropy.led import LED
import time
boardLed = LED(2)

# Start blinking endlessly
boardLed.blink(delay=0.5)  # Blink every 0.5s

# Main loop
while True:
    boardLed.update()