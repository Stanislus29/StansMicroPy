from machine import ADC, Pin
import utime

mic = ADC(26)  # AO connected to GP26
led = Pin(17, Pin.OUT)

BASELINE = mic.read_u16()  # get initial bias

while True:
    value = mic.read_u16()
    diff = abs(value - BASELINE)

    print("Mic diff:", diff)

    if diff > 50:   # adjust threshold
        led.value(1)
    else:
        led.value(0)

    utime.sleep(0.5)
