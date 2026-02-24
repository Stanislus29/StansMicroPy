# Libraries

Reusable MicroPython libraries for common components. Import these into your Pico scripts to simplify hardware control.

## Folder Structure

```
Libraries/
├── __init__.py          # Package initializer
├── led.py               # LED control (on, off, blink, fade, brightness via PWM)
├── servo.py             # Servo motor (angle, sweep, oscillate, calibration)
├── ultrasonic.py        # HC-SR04 ultrasonic distance sensor
├── pushbutton.py        # Push button with debouncing
├── RGBLED.py            # RGB LED (PWM/digital, named colours, hex, fades)
├── LiquidCrystal.py     # I2C LCD display driver (HD44780 via PCF8574)
├── LCD/
│   └── lcdapi.py        # Low-level LCD API base class
└── OLED/
    └── ssd1306.py       # SSD1306 OLED driver (I2C/SPI)
```
