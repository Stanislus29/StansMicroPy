"""Sweep a servo from 0° to 180° in 2° steps using the Servo library."""

from stansmicropy.servo import Servo
import time

servo = Servo(pin=15)  # Connect servo signal wire to GPIO 15
servo.sweep(start_angle=0, end_angle=180, step=2, delay=0.05)

while True:
    servo.update()  # Must be called continuously