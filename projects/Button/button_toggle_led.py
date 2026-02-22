"""Toggle an LED on/off each time a push button is pressed (with debouncing)."""

#Connect 1 pin to GPIO and the other to GND

import time
from stansmicropy.button import Button
from stansmicropy.led import LED

button = Button(16)          # Button on GPIO16
led = LED("LED")               # Onboard LED

print("Press the button to toggle the LED.")

while True:
    button.buttonPressed()
        
    # Use the boolean to control something
    if button.getState():
        led.on()
    else:
        led.off()

    time.sleep(0.01)