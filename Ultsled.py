from Libraries.ultrasonic import UltrasonicSensor
from Libraries.led import LED
from Libraries.servo import Servo
import time

servo = Servo(15)
led = LED(21)
ultsSensor = UltrasonicSensor(trig=17, echo=16)

while True:
    ultsSensor.update()                   # Refresh reading
    print("Distance:", ultsSensor.distCm(), "cm")
    time.sleep(0.05)                 # Main loop delay

    if ultsSensor.distCm() > 20:
        led.on()
        servo.setAngle(90)  # Move to 90°
    else:
        servo.setAngle(0)   # Move to 0°
        led.off()    