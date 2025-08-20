from machine import Pin, PWM, ADC
import utime

mic = ADC(26)  # AO connected to GP26

# Configure PWM on GP15
servo = PWM(Pin(15))
servo.freq(50)  # 50 Hz for standard servos

BASELINE = mic.read_u16()  # get initial bias

# Helper function to set angle (0-180)
def set_angle(angle):
    # Convert angle to duty cycle (approx 0.5ms - 2.5ms pulse)
    duty = int((angle / 180 * 2000) + 500)  # 500-2500 µs
    servo.duty_u16(int(duty * 65535 / 20000))  # Scale to 16-bit
    
# Sweep demo
while True:
    value = mic.read_u16()
    diff = abs(value - BASELINE)

    print("Mic diff:", diff)

    if diff > 200:   # adjust threshold
        for angle in range(0, 181, 10):
            set_angle(angle)
            utime.sleep(0.05)

