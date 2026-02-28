from stansmicropy.servo import Servo
import time

servo = Servo(15)  # Use GPIO15 for the servo

PRIORITY = 2

def init():
    servo.oscillate(min_angle=0, max_angle=180, step=5, delay=0.1)  # Start oscillating the servo

def step():
    servo.update()  # Update the servo state (handle oscillation)