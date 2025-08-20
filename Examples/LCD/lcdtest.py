from machine import Pin, I2C
import utime
from Libraries.LiquidCrystal import LCD

# I2C configuration
I2C_ADDR = 0x27   # Common address (check with i2c.scan())
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

# Initialize LCD
lcd = LCD(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Clear and display text
lcd.clear()
lcd.putstr("Hello World")
