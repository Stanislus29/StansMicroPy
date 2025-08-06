from Libraries.servo import Servo
import time

servo = Servo(15)

servo.setAngle(90)  # Move to 90°
time.sleep(1)
servo.setAngle(0)   # Move to 0°