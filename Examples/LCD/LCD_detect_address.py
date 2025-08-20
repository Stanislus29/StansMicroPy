from machine import Pin, I2C

# Configure I2C pins (adjust pins if using different GPIO)
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)  # GP5 = SCL, GP4 = SDA

print("Scanning I2C bus...")
devices = i2c.scan()

if not devices:
    print("No I2C devices found. Check wiring and power.")
else:
    print("I2C devices found:")
    for device in devices:
        print("Decimal address:", device, " | Hex address:", hex(device))
