from machine import Pin, PWM
import time

class RGBLED:
    NAMED_COLOURS = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203)
    }

    def __init__(self, redPin, greenPin, bluePin, commonAnode=False, pwm=True):
        self.commonAnode = commonAnode
        self.pwmMode = pwm

        if pwm:
            self.red = PWM(Pin(redPin))
            self.green = PWM(Pin(greenPin))
            self.blue = PWM(Pin(bluePin))
            for ch in (self.red, self.green, self.blue):
                ch.freq(1000)
        else:
            self.red = Pin(redPin, Pin.OUT)
            self.green = Pin(greenPin, Pin.OUT)
            self.blue = Pin(bluePin, Pin.OUT)

        self.currentColour = [0, 0, 0]
        self.targetColour = [0, 0, 0]
        self.fadeSpeed = 0
        self.lastUpdate = time.ticks_ms()

    def _pwmValue(self, value):
        duty = int((value / 255) * 65535)
        return 65535 - duty if self.commonAnode else duty

    def _applyColour(self, r, g, b):
        if self.pwmMode:
            self.red.duty_u16(self._pwmValue(r))
            self.green.duty_u16(self._pwmValue(g))
            self.blue.duty_u16(self._pwmValue(b))
        else:
            self.red.value(0 if (r == 0) ^ self.commonAnode else 1)
            self.green.value(0 if (g == 0) ^ self.commonAnode else 1)
            self.blue.value(0 if (b == 0) ^ self.commonAnode else 1)

    def setColour(self, r, g, b):
        """Immediately set LED colour."""
        self.currentColour = [r, g, b]
        self.targetColour = [r, g, b]
        self._applyColour(r, g, b)

    def setHex(self, hexCode):
        """Set LED colour using HEX code (#RRGGBB)."""
        hexCode = hexCode.lstrip('#')
        r = int(hexCode[0:2], 16)
        g = int(hexCode[2:4], 16)
        b = int(hexCode[4:6], 16)
        self.setColour(r, g, b)

    def setNamedColour(self, name):
        """Set LED colour using predefined name."""
        name = name.lower()
        if name in self.NAMED_COLOURS:
            self.setColour(*self.NAMED_COLOURS[name])
        else:
            raise ValueError(f"Unknown colour name: {name}")

    def fadeTo(self, r, g, b, speed=5):
        """
        Non-blocking fade to a new colour.
        Speed = how much the value changes per update (1–255).
        """
        self.targetColour = [r, g, b]
        self.fadeSpeed = max(1, min(speed, 255))

    def update(self):
        """Call this repeatedly in your main loop to handle fades."""
        now = time.ticks_ms()
        if time.ticks_diff(now, self.lastUpdate) < 20:  # ~50Hz
            return
        self.lastUpdate = now

        updated = False
        for i in range(3):
            if self.currentColour[i] < self.targetColour[i]:
                self.currentColour[i] = min(self.currentColour[i] + self.fadeSpeed, self.targetColour[i])
                updated = True
            elif self.currentColour[i] > self.targetColour[i]:
                self.currentColour[i] = max(self.currentColour[i] - self.fadeSpeed, self.targetColour[i])
                updated = True

        if updated:
            self._applyColour(*self.currentColour)

    def off(self):
        self.setColour(0, 0, 0)