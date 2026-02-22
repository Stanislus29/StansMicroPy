"""Move a servo to 90° then to 0° using the Servo library."""

from stansmicropy.servo import Servo
import time

servo = Servo(pin=15)  # Connect servo signal wire to GPIO 15

servo.setAngle(90)  # Move to 90°
time.sleep(1)
servo.setAngle(0)   # Move to 0°