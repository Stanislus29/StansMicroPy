"""Simultaneously blink LEDs and oscillate a servo motor in a multi-actuator demo."""

from stansmicropy.led import LED
from stansmicropy.servo import Servo

blinkLed = LED(16)
pwmLed = LED(17)
servo = Servo(15)

servo.oscillate(min_angle=30, max_angle=150, step=3, delay=0.03)

# Blink LED on pin 16
blinkLed.blink(delay=0.3)

# PWM LED on pin 17 with fade effect
pwmLed.fade(minP=5, maxP=80, step=5, delay=0.05)

while True:
    servo.update()
    blinkLed.update()
    pwmLed.update()