"""Continuously read and print distance (cm) from an HC-SR04 ultrasonic sensor."""

from stansmicropy.ultraSonic import Ultrasonic
import time

ultsSensor = Ultrasonic(trig=17, echo=16)

while True:
    ultsSensor.update()                   # Refresh reading
    print("Distance:", ultsSensor.distCm(), "cm")
    time.sleep(0.05)                 # Main loop delay