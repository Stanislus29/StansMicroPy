from Libraries.servo import Servo
import time

servo = Servo(15)

servo.oscillate(min_angle=30, max_angle=150, step=3, delay=0.03)

while True:
    servo.update()