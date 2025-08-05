from machine import Pin, PWM
import time

class LED:
    def __init__(self, pin_id):
        # Setup pin (digital output)
        self.pin = Pin(pin_id, Pin.OUT)
        self.pwm = None          # Will hold PWM object when needed

        # Mode control (None, 'blink', or 'fade')
        self.mode = None

        # Timing control
        self.last_update = time.ticks_ms()  # Track last state change

        # Blink settings
        self.blink_delay = 500   # ms between on/off
        self.blink_times = None  # Number of blinks (None = endless)
        self.blink_count = 0     # Count blinks done
        self.state = 0           # 0 = off, 1 = on

        # Fade settings
        self.fade_min = 0
        self.fade_max = 100
        self.fade_step = 5
        self.fade_delay = 50     # ms between brightness updates
        self.brightness = 0      # Current brightness (0-100%)
        self.direction = 1       # 1 = increasing, -1 = decreasing

    # -----------------------
    # BASIC CONTROL
    # -----------------------

    def on(self):
        """Turn LED fully ON (no animations)."""
        self.mode = None
        self.pin.value(1)

    def off(self):
        """Turn LED fully OFF (no animations)."""
        self.mode = None
        self.pin.value(0)

    def enablePwm(self):
        """Attach PWM to this pin (if not already)."""
        if self.pwm is None:
            self.pwm = PWM(self.pin)
            self.pwm.freq(1000)  # 1kHz frequency (smooth for LEDs)

    def setBrightness(self, percent):
        """
        Set LED brightness (0-100%).
        Enables PWM automatically if not already active.
        """
        self.enablePwm()
        duty = int(65535 * (percent / 100))
        self.pwm.duty_u16(duty)

    # -----------------------
    # NON-BLOCKING ANIMATIONS
    # -----------------------

    def blink(self, delay=0.5, times=None):
        """
        Start blinking LED without blocking main program.
        delay: seconds per ON or OFF
        times: number of full blinks (None = endless)
        """
        self.mode = 'blink'
        self.blink_delay = int(delay * 1000)  # convert to ms
        self.blink_times = times
        self.blink_count = 0
        self.state = 0  # Start OFF

    def fade(self, minP=20, maxP=80, step=5, delay=0.05):
        """
        Start fading LED brightness between two values.
        minP, maxP: brightness range (0-100%)
        step: how much to change per update
        delay: time between brightness changes
        """
        self.mode = 'fade'
        self.fade_min = minP
        self.fade_max = maxP
        self.fade_step = step
        self.fade_delay = int(delay * 1000)  # convert to ms
        self.brightness = minP
        self.direction = 1  # start increasing
        self.enablePwm()
        self.setBrightness(minP)

    def update(self):
        """
        Must be called repeatedly in the main loop.
        Checks if it's time to change LED state.
        """
        now = time.ticks_ms()

        # --- Handle Blinking ---
        if self.mode == 'blink':
            if time.ticks_diff(now, self.last_update) >= self.blink_delay:
                self.last_update = now
                # Toggle LED
                self.state = not self.state
                self.pin.value(self.state)

                # Count completed blinks (2 toggles = 1 blink)
                if self.blink_times is not None:
                    self.blink_count += 0.5
                    if self.blink_count >= self.blink_times:
                        self.mode = None  # stop blinking

        # --- Handle Fading ---
        elif self.mode == 'fade':
            if time.ticks_diff(now, self.last_update) >= self.fade_delay:
                self.last_update = now

                # Update brightness value
                self.brightness += self.fade_step * self.direction

                # Reverse direction at limits
                if self.brightness >= self.fade_max:
                    self.brightness = self.fade_max
                    self.direction = -1
                elif self.brightness <= self.fade_min:
                    self.brightness = self.fade_min
                    self.direction = 1

                # Apply brightness
                self.setBrightness(self.brightness)