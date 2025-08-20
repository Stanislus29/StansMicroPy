# AI & Electronics Learning Kit for Kids

**Author: Somtochukwu Emeka-Onwuneme**

---

## Overview of Recommended Components


| Component                 | Purpose                              | Est. Cost (GHS) |
| ------------------------- | ------------------------------------ | --------------- | 
| Camera module             | Vision and object detection          | ₵75 – ₵120      |
| Microphone / Sound sensor | Hearing, sound detection             | ₵30 – ₵45       |
| MicroSD card module       | Storage for datasets and logs        | ₵30 – ₵45       |
| Capacitive touch sensor   | Touch interaction                    | ₵15 – ₵30       |
| Gas sensor                | Smell detection (e.g., CO, LPG)      | ₵45 – ₵75       |
| Temperature sensor        | Heat detection                       | ₵45 – ₵60       |
| OLED display (Adafruit compatible) | Visual feedback             | ₵45 – ₵60       |
| RGB LEDs                  | Status feedback (color-coded states) | ₵15 – ₵30       |
| Gyroscope / IMU           | Balance and motion sensing           | ₵75 – ₵120      |
| Wheels (x2) + chassis     | Mobile robot platform                | ₵75 – ₵105      |

**Total Kit Cost (estimate): \$30 – \$45 → ₵450 – ₵675**

---

## Possible Projects

The projects presented below are intended to provide a ground from which interested AI enthusiasts can learn the fundamentals of AI and ML, particularly how to create rule-based reasoning models and see how 'weights' which are fundamental in creating Neural Networks operate. 

The projects combine a variety of sensors available in the kit and shows the user how reasoning models can be formulated from the readings of those components.

The codes presented here are placeholders and not the actual implementation. 

1. **Fire Detection Robot** – Combines gas, temperature, and vision sensors to reason about fire presence.
2. **Intruder Detection Robot** – Uses sound and motion sensors to detect disturbances and raise alarms.
3. **Smart Fan Robot** – Combines touch and temperature sensors to mimic decision-making for comfort.
4. **Self-Balancing Robot** – Uses gyroscope/IMU to demonstrate balance like a human.
5. **Touch-Responsive Bot** – Responds to human touch with movement and visual feedback.

---

## Project 1: Fire Detection Robot (Weighted Rule-Based Reasoning)

**Concept:**

* Use **gas + temperature + camera** inputs.
* Assign weights to each sensor and calculate a “fire likelihood score.”
* If score exceeds a threshold → Fire detected.

**Implementation (MicroPython Code):**

```python
# Fire Detection Robot - MicroPython (Pico W)
# Using simplified sensor library functions for teaching purposes

from mykit import Camera, GasSensor, TempSensor, OLED, RGBLED, Motors

# --- Init sensors & outputs ---
cam = Camera(model_file="fire_model.tflite")  # pre-trained fire/smoke model
gas = GasSensor(pin=26)                       # analog pin example
temp = TempSensor(pin=27)
oled = OLED(width=128, height=64)
led = RGBLED(red=15, green=14, blue=13)
motors = Motors(left_fwd=10, left_back=11, right_fwd=12, right_back=9)

# --- Thresholds for reasoning ---
GAS_FIRE_THRESHOLD = 300      # analog units, depends on sensor
TEMP_FIRE_THRESHOLD = 55.0    # °C
VISION_FIRE_CONF = 0.7        # confidence from vision model

# --- Reasoning weights ---
W_GAS = 0.3
W_TEMP = 0.3
W_VISION = 0.4

def detect_fire():
    # --- Read sensors ---
    gas_val = gas.read_value()                # raw analog reading
    temp_val = temp.read_celsius()
    v_label, v_conf = cam.classify_frame()    # e.g., ("fire", 0.85)

    # --- Convert to confidence scores (0-1) ---
    gas_conf = 1.0 if gas_val > GAS_FIRE_THRESHOLD else gas_val / GAS_FIRE_THRESHOLD
    temp_conf = 1.0 if temp_val > TEMP_FIRE_THRESHOLD else temp_val / TEMP_FIRE_THRESHOLD
    vision_conf = v_conf if v_label == "fire" else 0.0

    # --- Weighted reasoning ---
    final_conf = (W_GAS * gas_conf) + (W_TEMP * temp_conf) + (W_VISION * vision_conf)

    # --- Decision ---
    if final_conf >= 0.75:
        return "FIRE", final_conf
    elif final_conf >= 0.4:
        return "POSSIBLE_FIRE", final_conf
    else:
        return "SAFE", final_conf

def respond_to_fire(label, conf):
    if label == "FIRE":
        led.set_color("red")
        oled.show_text(f"FIRE! Conf:{conf:.2f}")
        motors.stop()
    elif label == "POSSIBLE_FIRE":
        led.set_color("yellow")
        oled.show_text(f"Check Area ({conf:.2f})")
        motors.slow_forward()
    else:
        led.set_color("green")
        oled.show_text("Safe")
        motors.forward()

# --- Main loop ---
while True:
    label, conf = detect_fire()
    respond_to_fire(label, conf)
```

---

## Project 2: Intruder Detection Robot (Weighted Rule-Based Reasoning)

**Concept:**

* Use **sound sensor + PIR motion sensor**.
* Each sensor contributes to a “risk score.”
* Risk score thresholds determine if it’s **safe, disturbance, or intruder alert**.

**Implementation (MicroPython Code):**

```python
from machine import ADC, Pin
import time

# Sensors
sound_sensor = ADC(26)
pir = Pin(27, Pin.IN)

# RGB LEDs
led_red = Pin(15, Pin.OUT)
led_green = Pin(14, Pin.OUT)
led_blue = Pin(13, Pin.OUT)

# Weights
w_motion = 0.6
w_sound = 0.4

while True:
    sound_val = sound_sensor.read_u16() / 65535
    motion_val = pir.value()

    score = (w_motion * motion_val) + (w_sound * sound_val)

    if score > 0.8:
        print("🚨 Intruder Detected!")
        led_red.value(1)
        led_green.value(0)
        led_blue.value(0)
    elif score > 0.4:
        print("⚠️ Possible Disturbance")
        led_red.value(1)
        led_green.value(1)
        led_blue.value(0)
    else:
        print("✅ Safe")
        led_red.value(0)
        led_green.value(1)
        led_blue.value(0)

    time.sleep(0.5)
```

---

## Project 3: Smart Fan Robot (Weighted Rule-Based Reasoning)

**Concept:**

* Combine **touch input + temperature sensor**.
* Decision score determines whether fan should turn on.

**Implementation (MicroPython Code):**

```python
from machine import ADC, Pin, PWM
import time

# Sensors
touch = Pin(16, Pin.IN)
temp_sensor = ADC(26)

# Servo motor
servo = PWM(Pin(17))
servo.freq(50)

# Weights
w_touch = 0.5
w_temp = 0.5

threshold = 0.7

def move_servo(angle):
    duty = int((angle / 180 * 5000) + 1000)
    servo.duty_u16(duty)

while True:
    touched = touch.value()
    temp_val = temp_sensor.read_u16() / 65535  # normalized 0–1

    score = (w_touch * touched) + (w_temp * temp_val)

    if score > threshold:
        print("Fan ON")
        move_servo(90)
    else:
        print("Fan OFF")
        move_servo(0)

    time.sleep(0.5)
```

---

## Conclusion

* These projects introduce **multi-sensory reasoning** (touch, sight, sound, heat, smell).
* They teach **rule-based logic** before transitioning to AI/TinyML.
* They show how **weights influence decision-making**, mimicking simple neural nets.
* Projects are **hands-on, modular, and affordable**.

---

© STEMAIDE Africa 2025 - Internal Technical Report
