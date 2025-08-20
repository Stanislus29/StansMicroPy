from machine import Pin, time_pulse_us
import time

# --- Pin setup ---
TRIG_PIN = 12      # GPIO12 for trigger
ECHO_PIN = 13      # GPIO13 for echo
LED_PIN = 21      # GPIO21 for LED

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
led = Pin(LED_PIN, Pin.OUT)

# --- Function to measure distance ---
def get_distance_cm():
    # Send a 10µs pulse to trigger
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Measure echo pulse width
    pulse_time = time_pulse_us(echo, 1, 30000)  # timeout 30ms
    if pulse_time < 0:
        return None  # no echo detected

    # Distance in cm: speed of sound ~ 343m/s => 29.1 µs per cm (round trip)
    distance = (pulse_time / 2) / 29.1
    return distance

# --- Main loop ---
THRESHOLD_CM = 10  # Turn on LED if object closer than 10 cm

while True:
    dist = get_distance_cm()
    if dist is not None:
        print("Distance:", dist, "cm")
        if dist < THRESHOLD_CM:
            led.value(1)  # Turn LED ON
        else:
            led.value(0)  # Turn LED OFF
    else:
        print("No echo")
        led.value(0)
    
    time.sleep(0.2)