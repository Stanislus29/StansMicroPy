"""Blink one external LED on GPIO 21 while fading another on GPIO 22 between 20-80% brightness."""

from stansmicropy.led import LED
import time
# blinkLed = LED(21)
pwmLed = LED(22)

# Blink LED on pin 21
# blinkLed.blink(delay=0.3)

# PWM LED on pin 22 with fade effect
pwmLed.fade(minP=20, maxP=80, step=5, delay=0.05)

while True:
    # blinkLed.update()
    pwmLed.update()