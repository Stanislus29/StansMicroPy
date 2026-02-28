# StansMicroPy

**Multitasking Libraries for MicroPython compatible boards**

[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Production-green.svg)]()

---

# Overview

The purpose of this project was to develop a set of libraries to allow easy programming and prototyping of essential sensor and robotics functions similar to the form of the Arduino IDE. The implementations here are independent of any IDE or existing framework. The libraries can be considered written in 'baremetal' form using only the `machine` modules provided by micropython. 

Primary Purpose: Achieving Multitasking without an RTOS**

In building this library, I had to tackle multitasking in a way that didn't require me to build a full RTOS. If this project has any use or advantage over similar libraries then it's that. 

The libraries for programming leds, servos, and the ultrasonic sensor are embedded with an `update()` function which performs scheduling while hiding the complexity. 

This 'innovation' allows a programmer to multitask multiple processes on a single core, e.g

```python
"""Simultaneously blink LEDs and oscillate a servo motor in a multi-actuator demo."""

from stansmicropy.led import LED
from stansmicropy.servo import Servo

blinkLed = LED(16)
pwmLed = LED(17)
servo = Servo(15)

servo.oscillate(min_angle=30, max_angle=150, step=3, delay=0.03)

# Blink LED on pin 16
blinkLed.blink(delay=0.3)

# PWM LED on pin 17 with fade effect
pwmLed.fade(minP=5, maxP=80, step=5, delay=0.05)

while True:
    servo.update()
    blinkLed.update()
    pwmLed.update()
```

The limits of how many programs can be 

## Folder Structure

```
blink/
├── README.md
├── requirements.txt
├── Computer_Vision/          # PC-side scripts using OpenCV and MediaPipe
│   ├── optical_flow_gesture_control.py
│   ├── finger_brightness_control.py
│   ├── mediapipe_hands_test.py
│   ├── opencv_version_check.py
│   ├── MediaPipe_Installation_Guide.md
│   └── COCO_Object_Detection/
│       ├── coco_object_detection.py
│       ├── deploy.prototxt
│       └── mobilenet_iter_73000.caffemodel
├── Pico_Code/                # Code that runs ON the Pico
│   ├── gesture_servo_server.py
│   ├── brightness_led_server.py
│   └── WiFi_Server/
│       └── wifi_tcp_server.py
├── Examples/                 # MicroPython examples by component
│   ├── Button/
│   │   └── button_toggle_led.py
│   ├── LCD/
│   │   ├── i2c_address_scan.py
│   │   ├── lcd_hello_world.py
│   │   └── lcd_two_lines.py
│   ├── LED/
│   │   ├── led_blink_baremetal.py
│   │   ├── led_on.py
│   │   ├── onboard_led_blink.py
│   │   ├── external_led_blink.py
│   │   ├── onboard_and_external_blink.py
│   │   ├── two_leds_blink_and_fade.py
│   │   └── external_led_brightness.py
│   ├── OLED/
│   │   ├── oled_init_test.py
│   │   ├── oled_temperature_display.py
│   │   └── ssd1306.py
│   ├── RGBLED/
│   │   └── rgb_color_cycle.py
│   ├── Servo/
│   │   ├── servo_move_to_angle.py
│   │   ├── servo_sweep.py
│   │   ├── servo_oscillate.py
│   │   └── servo_sweep_baremetal.py
│   ├── Ultrasonic/
│   │   ├── ultrasonic_measure_distance.py
│   │   ├── ultrasonic_led_servo.py
│   │   └── ultrasonic_led_servo_threshold.py
│   └── Integrated/
│       ├── keypad_read.py
│       ├── sound_sensor_led.py
│       ├── sound_sensor_servo.py
│       ├── ultrasonic_led_baremetal.py
│       └── leds_and_servo.py
├── Libraries/                # Reusable MicroPython libraries
│   ├── __init__.py
│   ├── led.py
│   ├── servo.py
│   ├── ultrasonic.py
│   ├── pushbutton.py
│   ├── RGBLED.py
│   ├── LiquidCrystal.py
│   ├── LCD/
│   │   └── lcdapi.py
│   └── OLED/
│       └── ssd1306.py
├── Docs/                     # Guides and documentation
│   ├── Raspberry_Pi_Pico_Coding_Guide.md
│   ├── LED.md
│   ├── Button.md
│   ├── Servo.md
│   ├── Ultrasonic.md
│   ├── LCD.md
│   ├── RGB.md
│   └── AI_Kit_recommendations.md
└── Firmware/                 # MicroPython .uf2 firmware files
    ├── RPI_PICO_W-20250415-v1.25.0.uf2
    └── RPI_PICO2_W-20250415-v1.25.0.uf2
```

---

## Quick Start

### 1. Flash the Pico
- Hold the **BOOTSEL** button, connect the Pico via USB.
- Copy the appropriate `.uf2` from `Firmware/` to the Pico drive.

### 2. Install PC dependencies
```bash
pip install -r requirements.txt
```

### 3. Upload MicroPython code
Use the [MicroPico VS Code extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) to upload `Libraries/` and `Pico_Code/` scripts to the Pico.

### 4. Run Computer Vision scripts
```bash
python Computer_Vision/Gesture1_OpenCV_pc.py
```

---

## Components Used

- Raspberry Pi Pico W / Pico 2 W
- LEDs, RGB LEDs, Servo motors, Ultrasonic sensors
- LCD (I2C), OLED (SSD1306)
- Webcam (for PC-side vision)

---

## License

Educational use. See `Docs/AI_Kit_recommendations.md` for full kit details.
