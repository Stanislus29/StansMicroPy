from machine import Pin, time_pulse_us
import time

class UltrasonicSensor:
    """
    Non-blocking Ultrasonic Sensor class for Raspberry Pi Pico (HC-SR04 style).
    Designed for short method calls and continuous updates.
    """

    def __init__(self, trig, echo, max_cm=400):
        """
        Initialize ultrasonic sensor pins.
        
        Args:
            trig (int): GPIO pin number for Trigger.
            echo (int): GPIO pin number for Echo.
            max_cm (int): Max measurable distance (default 400 cm).
        """
        self.trig = Pin(trig, Pin.OUT)
        self.echo = Pin(echo, Pin.IN)
        self.max_time = int((max_cm / 340) * 2 * 1_000_000)  # Max echo timeout (µs)

        # Internal state for non-blocking update
        self._distance = 0
        self._last_read = time.ticks_ms()
        self._interval = 100  # default 100ms between updates

    # ------------------- Private Helpers -------------------

    def _pulse(self):
        """
        Send a 10µs trigger pulse.
        """
        self.trig.low()
        time.sleep_us(2)
        self.trig.high()
        time.sleep_us(10)
        self.trig.low()

    def _readDistance(self):
        """
        Perform a single measurement and return distance in cm.
        """
        self._pulse()

        # Measure echo pulse duration (blocking call but short)
        duration = time_pulse_us(self.echo, 1, self.max_time)

        # Convert to cm: distance = (time * speed_of_sound) / 2
        # speed_of_sound ~ 0.034 cm/us
        if duration > 0:
            return (duration * 0.0343) / 2
        else:
            return -1  # Indicate no echo

    # ------------------- Public Methods -------------------

    def update(self):
        """
        Non-blocking periodic distance measurement.
        Call this in your main loop to refresh `_distance`.
        """
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_read) >= self._interval:
            self._last_read = now
            dist = self._readDistance()
            if dist >= 0:
                self._distance = dist  # Update cached distance

    def distCm(self):
        """
        Return last measured distance in cm.
        """
        return self._distance

    def distMm(self):
        """
        Return last measured distance in mm.
        """
        return self._distance * 10

    def avg(self, count=3, gap=50):
        """
        Take multiple readings and return average (blocking, for calibration).
        
        Args:
            count (int): number of samples
            gap (int): delay in ms between samples
        """
        readings = []
        for _ in range(count):
            readings.append(self._readDistance())
            time.sleep_ms(gap)
        return sum(readings) / len(readings)

    def near(self, threshold):
        """
        Check if object is closer than threshold (cm).
        """
        return self._distance > 0 and self._distance <= threshold

    def setInterval(self, ms):
        """
        Set refresh interval for non-blocking updates.
        """
        self._interval = ms