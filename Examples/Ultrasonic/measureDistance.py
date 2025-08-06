from Libraries.ultrasonic import UltrasonicSensor
import time

ultsSensor = UltrasonicSensor(trig=17, echo=16)

while True:
    ultsSensor.update()                   # Refresh reading
    print("Distance:", ultsSensor.distCm(), "cm")
    time.sleep(0.05)                 # Main loop delay