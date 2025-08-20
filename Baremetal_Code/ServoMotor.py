from machine import Pin, PWM
import utime

# Configure PWM on GP15
servo = PWM(Pin(15))
servo.freq(50)  # 50 Hz for standard servos

# Helper function to set angle (0-180)
def set_angle(angle):
    # Convert angle to duty cycle (approx 0.5ms - 2.5ms pulse)
    duty = int((angle / 180 * 2000) + 500)  # 500-2500 µs
    servo.duty_u16(int(duty * 65535 / 20000))  # Scale to 16-bit

# Sweep demo
while True:
    for angle in range(0, 181, 10):
        set_angle(angle)
        utime.sleep(0.05)
    for angle in range(180, -1, -10):
        set_angle(angle)
        utime.sleep(0.05)
