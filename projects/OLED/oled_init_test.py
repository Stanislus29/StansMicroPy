from machine import Pin, I2C
from stansmicropy.oled import SH1106_I2C
import time 

WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=100000)

display = SH1106_I2C(128, 64, i2c, addr=0x3C)

display.invert(0)
display.text('Testing 1', 0, 0, 1)
# time.sleep(1)
display.show()