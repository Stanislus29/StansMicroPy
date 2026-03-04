"""Motor library with directional control, speed, and acceleration methods."""

from machine import Pin, PWM
import time


class Motor:
    """
    A Motor control class for Raspberry Pi Pico using an H-bridge driver.
    Supports forward, backward, left, right, accelerate, and decelerate.
    """

    def __init__(self, enablePin, in1, in2, in3, in4, freq=1000):
        """
        Initialize the motor controller.

        Args:
            enablePin (int): GPIO pin number for PWM speed control (enable pin).
            in1 (int): GPIO pin for left motor forward.
            in2 (int): GPIO pin for left motor backward.
            in3 (int): GPIO pin for right motor forward.
            in4 (int): GPIO pin for right motor backward.
            freq (int): PWM frequency in Hz, typically 1000Hz for DC motors.
        """
        self.pwm = PWM(Pin(enablePin))
        self.pwm.freq(freq)

        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.in3 = Pin(in3, Pin.OUT)
        self.in4 = Pin(in4, Pin.OUT)

        # Speed state
        self.currentSpeed = 0
        self.targetSpeed = 0
        self.maxSpeed = 65535

        # Non-blocking ramp state
        self.ramping = False
        self.rampStep = 0
        self.delay = 0
        self.lastUpdate = time.ticks_ms()

    # ------------------- Core Helper -------------------

    def _applySpeed(self, speed):
        """
        Apply speed via PWM duty cycle.
        """
        speed = max(0, min(self.maxSpeed, int(speed)))
        self.currentSpeed = speed
        self.pwm.duty_u16(speed)

    # ------------------- Public Methods -------------------

    def setSpeed(self, speed):
        """
        Set motor speed directly.

        Args:
            speed (int): Speed value from 0 (stopped) to 65535 (full speed).
        """
        self._applySpeed(speed)

    def forward(self, speed=40000):
        """
        Drive both motors forward.

        Args:
            speed (int): Speed value from 0 to 65535.
        """
        self.in1.value(1)
        self.in2.value(0)
        self.in3.value(1)
        self.in4.value(0)
        self._applySpeed(speed)

    def backward(self, speed=40000):
        """
        Drive both motors backward.

        Args:
            speed (int): Speed value from 0 to 65535.
        """
        self.in1.value(0)
        self.in2.value(1)
        self.in3.value(0)
        self.in4.value(1)
        self._applySpeed(speed)

    def left(self, speed=40000):
        """
        Turn left by driving right motor forward and stopping left motor.

        Args:
            speed (int): Speed value from 0 to 65535.
        """
        self.in1.value(0)
        self.in2.value(0)
        self.in3.value(1)
        self.in4.value(0)
        self._applySpeed(speed)

    def right(self, speed=40000):
        """
        Turn right by driving left motor forward and stopping right motor.

        Args:
            speed (int): Speed value from 0 to 65535.
        """
        self.in1.value(1)
        self.in2.value(0)
        self.in3.value(0)
        self.in4.value(0)
        self._applySpeed(speed)

    def accelerate(self, step=5000):
        """
        Increase current speed by step amount.

        Args:
            step (int): Amount to increase speed by.
        """
        self._applySpeed(self.currentSpeed + step)

    def decelerate(self, step=5000):
        """
        Decrease current speed by step amount.

        Args:
            step (int): Amount to decrease speed by.
        """
        self._applySpeed(self.currentSpeed - step)

    def stop(self):
        """
        Stop all motors.
        """
        self.in1.value(0)
        self.in2.value(0)
        self.in3.value(0)
        self.in4.value(0)
        self._applySpeed(0)

    def rampTo(self, targetSpeed, step=1000, delay=0.02):
        """
        Start a non-blocking speed ramp toward targetSpeed.

        Args:
            targetSpeed (int): Desired speed (0 to 65535).
            step (int): Speed increment per update tick.
            delay (float): Time between steps (seconds).
        """
        self.targetSpeed = max(0, min(self.maxSpeed, int(targetSpeed)))
        self.rampStep = step
        self.delay = int(delay * 1000)  # store as ms
        self.ramping = True
        self.lastUpdate = time.ticks_ms()

    def stopRamp(self):
        """
        Stop ramping and hold current speed.
        """
        self.ramping = False

    def release(self):
        """
        Disable PWM signal.
        """
        self.pwm.deinit()

    # ------------------- Non-blocking Update -------------------

    def update(self):
        """
        Must be called in a loop for non-blocking speed ramping.
        Gradually adjusts currentSpeed toward targetSpeed.
        """
        if not self.ramping:
            return

        now = time.ticks_ms()

        # Respect delay timing
        if time.ticks_diff(now, self.lastUpdate) < self.delay:
            return

        self.lastUpdate = now

        # Ramp speed toward target
        if self.currentSpeed < self.targetSpeed:
            self.currentSpeed += self.rampStep
            if self.currentSpeed > self.targetSpeed:
                self.currentSpeed = self.targetSpeed
        elif self.currentSpeed > self.targetSpeed:
            self.currentSpeed -= self.rampStep
            if self.currentSpeed < self.targetSpeed:
                self.currentSpeed = self.targetSpeed

        self._applySpeed(self.currentSpeed)

        # Stop ramping once target is reached
        if self.currentSpeed == self.targetSpeed:
            self.ramping = False

