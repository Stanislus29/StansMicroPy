"""Oscillate a servo continuously between 30° and 150° using the Servo library."""

from stansmicropy.servo import Servo
import time

servo = Servo(pin=15)  # Connect servo signal wire to GPIO 15

servo.oscillate(min_angle=30, max_angle=150, step=3, delay=0.03)

while True:
    servo.update()