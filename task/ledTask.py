from stansmicropy.led import LED
import time

PRIORITY = 1

led = LED(17)  # Use GPIO17 for the LED

def init():
    led.fade(minP=10, maxP=90, step=5, delay=0.1)  # Start fading the LED

def step():
    led.update()  # Update the LED state (handle fading)