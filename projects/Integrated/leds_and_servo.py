"""Simultaneously blink LEDs and oscillate a servo motor in a multi-actuator demo."""

from stansmicropy.led import LED
from stansmicropy.servo import Servo
import time
blinkLed = LED(21)
pwmLed = LED(22)
servo = Servo(15)

servo.oscillate(min_angle=30, max_angle=150, step=3, delay=0.03)

# Blink LED on pin 21
blinkLed.blink(delay=0.3)

# PWM LED on pin 22 with fade effect
pwmLed.fade(minP=20, maxP=80, step=5, delay=0.05)

while True:
    servo.update()
    blinkLed.update()
    pwmLed.update()