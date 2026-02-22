"""Turn on an LED and move a servo to 90° when ultrasonic distance exceeds 50 cm."""

from stansmicropy.ultraSonic import Ultrasonic
from stansmicropy.led import LED
from stansmicropy.servo import Servo
import time

servo = Servo(15)
led = LED(18)
ultsSensor = Ultrasonic(trig=17, echo=16)

while True:
    ultsSensor.update()                   # Refresh reading
    print("Distance:", ultsSensor.distCm(), "cm")
    time.sleep(0.05)                 # Main loop delay

    if ultsSensor.distCm() > 50:
        led.on()
        servo.setAngle(90)  # Move to 90°
    else:
        servo.setAngle(0)   # Move to 0°
        led.off()    