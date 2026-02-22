"""Blink the onboard LED on/off every 0.5 seconds using bare machine.Pin (no library)."""

from machine import Pin
import time

led = Pin("LED", Pin.OUT)  # uppercase
while True:
    led.toggle()
    time.sleep(0.5)