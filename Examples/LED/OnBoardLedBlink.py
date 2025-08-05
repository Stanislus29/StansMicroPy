from Libraries.ledclass import LED
import time

# Onboard LED (Raspberry Pi Pico built-in)
boardLed = LED("LED")

# Start blinking endlessly
boardLed.blink(delay=0.5)  # Blink every 0.5s

# Main loop
while True:
    boardLed.update()