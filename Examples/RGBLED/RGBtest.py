from Libraries.RGBLED import RGBLED
import time

# RGB LED on pins 16, 17, 18 (common cathode, PWM)
led = RGBLED(16, 17, 18, commonAnode=False, pwm=True)

# Start with red
led.setNamedColour("red")

while True:
    led.update()  # Keep calling in main loop

    # Cycle through colours with fades
    if led.currentColour == [255, 0, 0]:
        led.fadeTo(0, 255, 0, speed=5)  # Green
    elif led.currentColour == [0, 255, 0]:
        led.fadeTo(0, 0, 255, speed=5)  # Blue
    elif led.currentColour == [0, 0, 255]:
        led.fadeTo(255, 0, 0, speed=5)  # Red

    # Do other work here (non-blocking)