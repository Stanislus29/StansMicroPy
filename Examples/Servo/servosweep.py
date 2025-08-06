from Libraries.servo import Servo
import time

servo = Servo(15)
servo.sweep(0, 180, step=2, delay=0.02)

while True:
    servo.update()  # Must be called continuously