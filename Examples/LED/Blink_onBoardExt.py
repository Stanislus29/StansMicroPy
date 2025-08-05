from Libraries.ledclass import LED
import time

boardLed = LED("LED")   # Onboard LED
extLed = LED(21)        # External LED

# Start blink animations
boardLed.blink(delay=0.3)
extLed.blink(delay=1.0)

while True:
    boardLed.update()
    extLed.update()