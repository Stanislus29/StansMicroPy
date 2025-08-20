from machine import I2C, Pin
from Libraries.LiquidCrystal import LCD  # Assuming your class is saved here

# Setup I2C (update pins and I2C ID if needed)
i2c = I2C(0, scl=Pin(17), sda=Pin(16))  # Use correct GPIOs for your board

# Initialize LCD (adjust I2C address and dimensions)
lcd = LCD(i2c, 0x27, num_lines=2, num_columns=16)

# Write to first line
lcd.move_to(0, 0)
lcd.putstr("Hello, World!")

# Write to second line
lcd.move_to(0, 1)
lcd.putstr("Line 2 here")
