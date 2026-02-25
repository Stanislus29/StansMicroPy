"""Read the esp32's internal temperature sensor and display the value on an SSD1306 OLED."""

from machine import ADC, I2C, Pin
from stansmicropy.oled import SH1106_I2C
import time

# On ESP32, the internal temperature sensor is connected to ADC1, channel 0
# However, in MicroPython, we use the internal hall sensor function or esp32-specific API
import esp32

WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=100000)

display = SH1106_I2C(128, 64, i2c, addr=0x3C)

display.invert(0)
    
while True:
    # Read the internal temperature (approximate)
    temp = esp32.raw_temperature()
    print("ESP32 internal temperature: {:.2f} °C".format(temp))

    display.fill(0)
    display.text("Temp: {:.2f}C".format(temp), 0, 14, 1)
    display.show()
    time.sleep(1)