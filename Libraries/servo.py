from machine import Pin, PWM
import time

class Servo:
    """
    A non-blocking Servo control class for Raspberry Pi Pico.
    Supports direct angle control, sweeps, and continuous oscillation.
    """

    def __init__(self, pin, min_us=500, max_us=2500, freq=50):
        """
        Initialize the servo.

        Args:
            pin (int): GPIO pin number connected to servo.
            min_us (int): Minimum pulse width (microseconds) corresponding to 0°.
            max_us (int): Maximum pulse width (microseconds) corresponding to 180°.
            freq (int): PWM frequency, typically 50Hz for hobby servos.
        """
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)

        # Calibration parameters
        self.min_us = min_us
        self.max_us = max_us

        # Internal state for non-blocking movement
        self.current_angle = 0
        self.target_angle = 0
        self.step = 0
        self.delay = 0
        self.last_update = time.ticks_ms()

        # Oscillation state
        self.oscillating = False
        self.osc_min = 0
        self.osc_max = 0
        self.osc_speed = 1
        self.osc_direction = 1

    # ------------------- Core Helper -------------------

    def _angleToDuty(self, angle):
        """
        Convert angle to duty cycle (16-bit value for Pico).
        """
        us = self.min_us + (self.max_us - self.min_us) * angle / 180
        duty_u16 = int((us / 20000) * 65535)  # 20ms period = 50Hz
        return duty_u16

    def _applyAngle(self, angle):
        """
        Apply a given angle immediately to servo.
        """
        self.pwm.duty_u16(self._angleToDuty(angle))

    # ------------------- Public Methods -------------------

    def setAngle(self, angle):
        """
        Immediately move servo to specific angle.
        """
        self.current_angle = angle
        self._applyAngle(angle)

    def sweep(self, start_angle, end_angle, step=1, delay=0.02):
        """
        Start a non-blocking sweep from start_angle to end_angle.

        Args:
            start_angle (int): Starting angle in degrees.
            end_angle (int): Ending angle in degrees.
            step (int): Step size in degrees per update.
            delay (float): Time between steps (seconds).
        """
        self.current_angle = start_angle
        self.target_angle = end_angle
        self.step = step
        self.delay = int(delay * 1000)  # store as ms
        self.last_update = time.ticks_ms()

        self._applyAngle(self.current_angle)

    def oscillate(self, min_angle, max_angle, step=1, delay=0.02):
        """
        Start continuous oscillation between min_angle and max_angle.

        Args:
            min_angle (int): Lower bound angle.
            max_angle (int): Upper bound angle.
            step (int): Step size per update.
            delay (float): Time between steps (seconds).
        """
        self.oscillating = True
        self.osc_min = min_angle
        self.osc_max = max_angle
        self.osc_speed = step
        self.delay = int(delay * 1000)  # ms delay
        self.current_angle = min_angle
        self.osc_direction = 1
        self._applyAngle(self.current_angle)

    def stopOscillation(self):
        """
        Stop oscillation and hold current position.
        """
        self.oscillating = False

    def calibrate(self, min_us=None, max_us=None):
        """
        Update calibration parameters dynamically.
        """
        if min_us:
            self.min_us = min_us
        if max_us:
            self.max_us = max_us

    def release(self):
        """
        Disable PWM signal, allowing servo to relax.
        """
        self.pwm.deinit()

    # ------------------- Non-blocking Update -------------------

    def update(self):
        """
        Must be called in a loop for non-blocking motion.
        Handles sweep and oscillation movement.
        """
        now = time.ticks_ms()

        # Respect delay timing
        if time.ticks_diff(now, self.last_update) < self.delay:
            return

        self.last_update = now

        # Handle oscillation
        if self.oscillating:
            self.current_angle += self.osc_speed * self.osc_direction

            # Reverse direction at bounds
            if self.current_angle >= self.osc_max:
                self.current_angle = self.osc_max
                self.osc_direction = -1
            elif self.current_angle <= self.osc_min:
                self.current_angle = self.osc_min
                self.osc_direction = 1

            self._applyAngle(self.current_angle)
            return

        # Handle single sweep
        if self.current_angle < self.target_angle:
            self.current_angle += self.step
            if self.current_angle > self.target_angle:
                self.current_angle = self.target_angle
        elif self.current_angle > self.target_angle:
            self.current_angle -= self.step
            if self.current_angle < self.target_angle:
                self.current_angle = self.target_angle

        self._applyAngle(self.current_angle)