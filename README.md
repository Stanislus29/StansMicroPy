<div align="center">

<img src="https://img.shields.io/badge/StansMicroPy-Multitasking%20MicroPython%20Libraries-0B3D91?style=for-the-badge&logo=micropython&logoColor=white" alt="StansMicroPy Banner"/>

<br/>

<img src="https://img.shields.io/badge/Raspberry%20Pi-Pico%20Series-0B3D91?style=flat-square&logo=raspberrypi&logoColor=white"/>
<img src="https://img.shields.io/badge/Espressif-ESP32%20Series-0B3D91?style=flat-square&logo=espressif&logoColor=white"/>

<br/>

[![License](https://img.shields.io/badge/License-MIT-0B3D91?style=flat-square&logoColor=white)](LICENSE)
[![MicroPython](https://img.shields.io/badge/MicroPython-v1.25-0B3D91?style=flat-square&logo=micropython&logoColor=white)](https://micropython.org/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-1a73e8?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

<br/>

*Baremetal MicroPython libraries with built-in cooperative multitasking for the Raspberry Pi Pico and Espressif boards.*

</div>

---

## Overview

The purpose of this project is to develop a set of libraries that allow easy programming and prototyping of essential sensor and robotics functions, similar to the form of the Arduino IDE. The implementations here are independent of any IDE or existing framework — written in 'baremetal' form using only the `machine` modules provided by MicroPython.

*N.B: Initial development was for Raspberry Pi Pico boards, but the firmware in this repository works seamlessly with ESP32 boards. In projects or documentation where references are made to Pico boards rather than `MCU`, treat this as an oversight. The libraries work equivalently for both boards. If you may wish for such documentation issues to be addressed, kindly open a pull request*

<details>
<summary><b>🔧 Supported Components</b></summary>
<br/>

| Component | Library | Key Features |
|:---|:---|:---|
| **LED** | `led.py` | On/Off, non-blocking blink, PWM fade & brightness |
| **Servo** | `servo.py` | Angle positioning, sweep, oscillate, calibration |
| **Ultrasonic** | `ultraSonic.py` | HC-SR04 distance measurement |
| **Button** | `button.py` | Debounced input with short/long press |
| **RGB LED** | `rgbLed.py` | PWM/digital, named colours, hex, fades |
| **LCD** | `liquidCrystal.py` | I2C HD44780 via PCF8574 driver |
| **OLED** | `oled.py` | SSD1306 & SH1106 (I2C/SPI) |
| **Wi-Fi** | `wifiManager.py` | Station mode connect + TCP server |
| **Scheduler** | `scheduler.py` | Cooperative task scheduler with profiling |

</details>

---

## Multitasking Without an RTOS

In building this library, I had to tackle multitasking in a way that didn't require me to build a full RTOS. If this project has any use or advantage over similar libraries, then it's that.

The libraries for LEDs, servos, and the ultrasonic sensor are embedded with an `update()` function which performs cooperative scheduling while hiding the complexity. This allows a programmer to multitask multiple processes on a single core:

```python
"""Simultaneously blink LEDs and oscillate a servo motor."""

from stansmicropy.led import LED
from stansmicropy.servo import Servo

blinkLed = LED(16)
pwmLed = LED(17)
servo = Servo(15)

servo.oscillate(min_angle=30, max_angle=150, step=3, delay=0.03)
blinkLed.blink(delay=0.3)
pwmLed.fade(minP=5, maxP=80, step=5, delay=0.05)

while True:
    servo.update()
    blinkLed.update()
    pwmLed.update()
```

For more complex scenarios, the `Scheduler` class manages multiple task modules with priority sorting, runtime add/remove, and optional profiling:

- [schedulerDemo.py](projects/schedulerDemo.py) — Running multiple task files as simultaneous processes on the MCU
- [buttonTogglePrograms.py](projects/buttonTogglePrograms.py) — Using a physical button to switch between active programs at runtime, with OLED menu UI and mode persistence

For someone seeking to replicate modern PC OS capabilities on a cheap MCU, those demonstrations serve as a solid backbone.

---

## Computer Vision

> **Architecture:** Heavy processing (OpenCV, MediaPipe) runs on the PC → commands are sent to the MCU over Wi-Fi TCP.

The repository includes gesture control projects split into:

| Side | Location | Role |
|:---|:---|:---|
| **Client** (PC) | `projects/Computer_Vision/client_side/` | Webcam capture, hand tracking, sends commands |
| **Server** (MCU) | `projects/Computer_Vision/server_side/` | Receives commands, drives hardware |

The desktop-side `compVision.py` library wraps MediaPipe's Hand Landmarker for simplified hand detection. When transferring `stansmicropy` to the MCU, copy it **without** the `desktop` module:

```bash
mpremote cp -r src/stansmicropy :
```

---

## Getting Started

<table>
<tr>
<td width="50%">

### Prerequisites

1. Flash the appropriate firmware from onto your Pico
2. Install [Python 3.12+](https://www.python.org/) (ensure *Add to PATH* is checked)
3. Install mpremote:
   ```bash
   pip install mpremote
   ```
4. Install the **MicroPico** VSCode extension, but **disable auto-connect** — the serial port can only be accessed by one of `mpremote` or MicroPico at a time. The **MicroPico** extension helps resolve Pylance issues as micriopython only libraries like `machine` aren't available on desktop Python.

   ```
   Settings > MicroPico > Auto Connect → OFF
   ```

</td>
<td width="50%">

### Quick Start

1. Read the [Coding Guide](Docs/Coding_Guide.md)
2. Browse the [library docs](Docs/) for method references
3. Start with the [LED examples](projects/LED/) and progress from there

### For CV Projects

```bash
pip install -r requirements.txt
```

</td>
</tr>
</table>

---

## Project Structure

```
blink/
├── src/
│   ├── stansmicropy/             # ← Core MicroPython libraries
│   │   ├── led.py, servo.py, button.py, ultraSonic.py
│   │   ├── rgbLed.py, liquidCrystal.py, lcd.py, oled.py
│   │   ├── wifiManager.py, scheduler.py
│   │   └── __init__.py
│   └── desktop/                  # ← Desktop-side libraries (PC only)
│       └── compVision.py             # MediaPipe hand tracking wrapper
│
├── projects/                     # ← Example projects by component
│   ├── LED/, Servo/, Button/, LCD/, OLED/, RGBLED/, Ultrasonic/
│   ├── multi_component_projects/     # Sound sensor, multi-actuator demos
│   ├── Computer_Vision/
│   │   ├── client_side/              # PC scripts (sends commands)
│   │   └── server_side/              # MCU scripts (receives commands)
│   ├── wifi/                         # Wi-Fi connection examples
│   ├── task/                         # Task modules for the scheduler
│   ├── schedulerDemo.py
│   └── buttonTogglePrograms.py
│
├── Docs/                         # ← Guides & library documentation
│   ├── Coding_Guide.md
│   ├── LED.md, Servo.md, Button.md, Ultrasonic.md
│   ├── LCD.md, RGB.md
│   └── AI_Kit_recommendations.md
│
├── pyproject.toml
├── requirements.txt
└── LICENSE
```

---

## Conventions

- Libraries and methods use **camelCase** naming
- Each library module has corresponding documentation in `Docs/`
- Project files include docstrings and inline comments where intuition might fail

---

## Citations

This project is indebted to the open source community, particularly the contributions of:

<div align="center">

![Radomir Dopieralski](https://img.shields.io/badge/Radomir%20Dopieralski-%40deshipu-0B3D91?style=for-the-badge&logo=github&logoColor=white)
![Robert Hammelrath](https://img.shields.io/badge/Robert%20Hammelrath-%40robert--hh-0B3D91?style=for-the-badge&logo=github&logoColor=white)
![Tim Weber](https://img.shields.io/badge/Tim%20Weber-%40scy-0B3D91?style=for-the-badge&logo=github&logoColor=white)
![Adafruit Inc.](https://img.shields.io/badge/Adafruit%20Inc.-Open%20Source-0B3D91?style=for-the-badge&logo=adafruit&logoColor=white)

whose code provided the foundations for the OLED library in this repository.

and 

![Damien Hyländs](https://img.shields.io/badge/Damien%20Hyl%C3%A4nds-%40dhylands-0B3D91?style=for-the-badge&logo=github&logoColor=white)

whose code is the backbone of the LCD Library 
</div>

---

<div align="center">

**Somtochukwu Stanislus Emeka-Onwuneme** · [MIT License](LICENSE)

### Connect with me

<a href="https://twitter.com/vzyengineer">
  <img src="https://img.shields.io/badge/X-000000?style=flat&logo=&logoColor=white" />
</a><a href="https://linkedin.com/in/emekasomto3">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=&logo=linkedin&logoColor=white" />
</a>

</div>
