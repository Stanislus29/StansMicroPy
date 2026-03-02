# Coding Guide

**Author: Somtochukwu Stanislus Emeka-Onwuneme**

---

This guide is a thorough walkthrough for getting set up with the StansMicroPy library. It covers installing firmware, setting up your development environment, understanding how the libraries are structured and named, and using `mpremote` to manage files and programs on your board.

**This guide covers:**

1. [Installing MicroPython firmware](#1-installing-micropython-firmware)
2. [Setting up your development environment](#2-setting-up-your-development-environment)
3. [Understanding `mpremote`](#3-understanding-mpremote)
4. [The library architecture](#4-the-library-architecture)
5. [Naming conventions](#5-naming-conventions)
6. [Learning path — from docs to projects](#6-learning-path)

---

## 1. Installing MicroPython Firmware

MicroPython regularly updates their firmware, so rather than bundling it in this repo, download the latest version directly from the official source.

### Raspberry Pi Pico / Pico W / Pico 2W

**Download:** 

1. [Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO_W/)
2. [Raspberry Pi Pico 2W](https://micropython.org/download/RPI_PICO2_W/)

Select the correct board variant (Pico W, Pico 2W, etc.) and download the latest `.uf2` file.

**Flashing the firmware:**

1. Unplug the Pico from your computer
2. Hold the **BOOTSEL** button and plug the USB cable back in
3. The Pico will appear as a removable drive (like a USB stick)
4. Drag and drop the `.uf2` file into the drive
5. The drive will disappear — this confirms the firmware has been flashed

That's it. The Pico is now running MicroPython.

### Espressif Boards (ESP32, ESP32-S3, etc.)

**Download:** [micropython.org/download — Espressif](https://micropython.org/download/ESP32_GENERIC/)

The flashing process for Espressif boards is different from the Pico. Espressif boards use a serial flash tool rather than drag-and-drop. MicroPython provides detailed installation instructions on the download page for each board, including the `esptool.py` commands required. Follow those board-specific instructions carefully.

In general, the process looks like:

```bash
pip install esptool

# Erase existing firmware
esptool.py --port COM3 erase_flash

# Flash the new firmware (.bin file)
esptool.py --port COM3 --baud 460800 write_flash -z 0x1000 <firmware_file>.bin
```

> **Note:** The flash address (`0x0` vs `0x1000`) and baud rate vary by board. Always check the specific instructions on MicroPython's download page for your board. FOr certain boards eliminate `--baud 460800` and write at regular speed. 

---

## 2. Setting Up Your Development Environment

Whilst Thonny IDE is the mainstream choice for programming MicroPython boards and is suitable for learners, I believe VSCode offers a lot more — particularly in its ability to connect with your GitHub repo and manage more complex project structures. It should be the preferred choice for engineers.

### Prerequisites

1. **Python 3.12+** — Install from [python.org](https://www.python.org/downloads/). Ensure you check **"Add Python to PATH"** during installation.

2. **mpremote** — The primary tool for managing your board:
   ```bash
   pip install mpremote
   ```

3. **MicroPico extension** — Install from the VSCode extensions marketplace. This gives you a REPL, syntax highlighting, and resolves Pylance warnings for MicroPython-only modules like `machine` that don't exist on desktop Python.

   > **Important:** Disable MicroPico's auto-connect feature. The serial port can only be accessed by **one** of `mpremote` or MicroPico at a time. If both try to connect, you'll get port conflicts.
   >
   > ```
   > Settings > MicroPico > Auto Connect → OFF
   > ```

4. **For Computer Vision projects only:**
   ```bash
   pip install -r requirements.txt
   ```

### Verifying Your Setup

With the firmware installed and dependencies in place, restart VSCode and plug in your board. Since we use mpremote as opposed to MicroPico REPL, run:

```bash
mpremote connect auto
```

This should activte the MicroPython REPL. Press `Ctrl + ]` to exit. 


#### Errors 

1. In case where you get an error like:

```bash 
unable to access MicroPico REPL
```

Just unplug your board and ply back in and run the connect command. That should rectify the issue. 

2. You could also get a situation where an error like this appears 
```bash
unable to connect to port
```
Kindly confirm that your board is connected to a working port and that MicroPico REPL does not run auto-connect. 

3. If the above do not rectify this, run `Win + X > Device Manager` and find the exact port your device is connected to. Then run:
```bash 
mpremote connect PORT_NAME
```

where `PORT_NAME` is of the type COM3, COM5, COM9 etc.

---

## 3. Understanding `mpremote`

`mpremote` is arguably the most important tool in this workflow. It handles file transfers, running programs, and managing the board's filesystem — all from your terminal.

### Why `mpremote` matters

If you've worked with Arduino (`.ino`) boards, you're used to a workflow where you compile and flash a single program to the board. There's no filesystem — the board runs whatever was last uploaded, and that's it.

With MicroPython and `mpremote`, your board has an **actual filesystem**. You can store multiple programs, libraries, config files, and data on the board simultaneously. This changes the game entirely:

- You're not limited to a single `main.py`
- You can structure your `main.py` as an operating system — using buttons, conditionals, or terminal arguments to start or kill a process
- You can hot-swap programs at runtime without reflashing anything

I demonstrated this with two projects in `projects/`:

- [schedulerDemo.py](../projects/schedulerDemo.py) — Running two task files as simultaneous processes on the MCU
- [buttonTogglePrograms.py](../projects/buttonTogglePrograms.py) — Using a physical button to switch between active programs, killing one and starting another — with OLED menu UI and mode persistence via JSON

For someone seeking to replicate modern PC OS capabilities on a cheap MCU, those demonstrations serve as a solid backbone.

### File Management

**Copying the library package to the board:**

```bash
mpremote cp -r src/stansmicropy :
```

This copies the entire `stansmicropy` package to the root of the board's filesystem. The `:` refers to the board's root directory.

> **Note for CV projects:** When transferring to the MCU, copy `stansmicropy` without the `desktop` module. The `desktop` module contains OpenCV/MediaPipe wrappers that are for PC-side operations only.

**Copying a single project file:**

```bash
mpremote cp projects/LED/external_led_blink.py :main.py
```

This copies the file to the board and names it `main.py`, which the board will auto-run on boot.

**Creating directories on the board:**

```bash
mpremote mkdir :projects
```

**Copying a folder recursively:**

```bash
mpremote cp -r projects/LED :LED
```

> **Note:** The `-r` flag copies the entire folder and its contents recursively.

**Listing files on the board:**

```bash
mpremote ls :
```

You'll see something like:

```
ls :
         128 stansmicropy/
         244 main.py
```

### Running Programs

**Run a script directly without copying it to the board:**

```bash
mpremote run projects/LED/onboard_led_blink.py
```

This is useful for testing — the file executes on the board from your PC without being stored on the board's filesystem.

**Run a script already stored on the board:**

```bash
mpremote exec "import main"
```

### Deleting Files

**Delete a single file:**

```bash
mpremote rm :main.py
```

**Delete a directory** (must be empty first):

```bash
mpremote rm :stansmicropy/led.py
mpremote rm :stansmicropy/servo.py
# ... remove all files first
mpremote rmdir :stansmicropy
```

### Quick Reference

| Command | Description |
|:---|:---|
| `mpremote connect auto` | Open a REPL session |
| `mpremote ls :` | List files on the board root |
| `mpremote ls :stansmicropy/` | List files in a subdirectory |
| `mpremote cp file.py :` | Copy a file to the board root |
| `mpremote cp -r folder :folder` | Copy a folder recursively |
| `mpremote cp :main.py .` | Copy a file **from** the board to your PC |
| `mpremote run script.py` | Run a local script on the board (without saving) |
| `mpremote rm :file.py` | Delete a file from the board |
| `mpremote mkdir :dirname` | Create a directory on the board |
| `mpremote rmdir :dirname` | Remove an empty directory from the board |
| `mpremote reset` | Soft-reset the board |

---

## 4. The Library Architecture

### Object-Oriented Approach

The libraries are built using an Object-Oriented approach. This allows for easy scalability and makes teaching substantially easier. The approach involves creating library classes that handle the lower-level abstraction work, while the programmer operates at a higher level — calling only the methods.

The library package `stansmicropy` lives in `src/stansmicropy/` and contains classes for every supported component. The `__init__.py` exposes them all, so you can import directly:

```python
from stansmicropy.led import LED
from stansmicropy.servo import Servo
from stansmicropy.ultraSonic import Ultrasonic
```

**N.B:** The `__init__.py` file is what causes Python to treat `stansmicropy` as a package. Without it, imports will fail.

### Why This Matters — A Concrete Example

Let's say you want to fade an LED using PWM. Here's what the code looks like with the library:

```python
from stansmicropy.led import LED

pwmLed = LED(22)
pwmLed.fade(minP=20, maxP=80, step=5, delay=0.05)

while True:
    pwmLed.update()
```

Compare this to the raw MicroPython equivalent:

```python
from machine import Pin, PWM
import time

pwm = PWM(Pin(22))
pwm.freq(1000)

def set_brightness(pwm, percent):
    duty = int((percent / 100) * 65535)
    pwm.duty_u16(duty)

brightness = 20
direction = 1

while True:
    set_brightness(pwm, brightness)
    brightness += direction * 5
    if brightness >= 80:
        direction = -1
    elif brightness <= 20:
        direction = 1
    time.sleep(0.05)
```

The library version hides the duty cycle maths, the direction tracking, and the PWM initialisation. You describe _what_ you want (fade between 20% and 80%) and the library handles _how_.

More importantly, the library version is **non-blocking**. The `update()` pattern means you can run multiple components simultaneously without any one of them hogging the processor — which brings us to the core advantage of this library.

### The `update()` Pattern

Every time-dependent library (LED, Servo, Ultrasonic, RGBLED) follows the same cooperative pattern:

1. **Configure** the behaviour — `blink()`, `fade()`, `oscillate()`, `sweep()`, etc.
2. **Call `update()`** repeatedly in your main loop

```python
from stansmicropy.led import LED
from stansmicropy.servo import Servo

led = LED(16)
servo = Servo(15)

led.blink(delay=0.3)
servo.oscillate(min_angle=30, max_angle=150, step=3, delay=0.03)

while True:
    led.update()
    servo.update()
```

Both components run concurrently on a single core, no threads, no RTOS.

---

## 5. Naming Conventions

Consistency matters. The codebase follows these conventions:

### Files

| Type | Convention | Examples |
|:---|:---|:---|
| Library modules | **camelCase** | `led.py`, `rgbLed.py`, `ultraSonic.py`, `liquidCrystal.py`, `wifiManager.py` |
| Project scripts | **snake_case** | `onboard_led_blink.py`, `servo_sweep.py`, `ultrasonic_measure_distance.py` |
| Documentation | **PascalCase / descriptive** | `LED.md`, `Servo.md`, `Raspberry_Pi_Pico_Coding_Guide.md` |

### Classes

All classes use **PascalCase**:

```python
LED, Servo, Ultrasonic, Button, RGBLED, LCD, Scheduler, WiFiManager
```

### Methods

Methods use **camelCase**:

```python
led.setBrightness(50)
led.enablePwm()
servo.setAngle(90)
servo.stopOscillation()
rgb.setColour(255, 0, 0)
rgb.setNamedColour("cyan")
rgb.fadeTo(0, 255, 128, speed=5)
```

### Variables

Instance variables follow **camelCase**:

```python
blinkLed = LED(16)
pwmLed = LED(17)
extLed = LED(21)
boardLed = LED(2)
```

### General Rule

If you're writing a **library method** or **variable name**, use camelCase. If you're naming a **project file**, use snake_case. If you're naming a **class**, use PascalCase.

---

## 6. Learning Path

### Step 1: Read the Documentation

Each library module has a corresponding doc in `Docs/`. These are structured as entity-relationship models — they lay out every attribute and method the class offers, along with descriptions and relationships.

| Doc | Component | What You'll Learn |
|:---|:---|:---|
| [LED.md](LED.md) | LEDs | `on()`, `off()`, `blink()`, `fade()`, `setBrightness()`, `update()` |
| [Servo.md](Servo.md) | Servo Motors | `setAngle()`, `sweep()`, `oscillate()`, `calibrate()`, `release()`, `update()` |
| [Button.md](Button.md) | Push Buttons | `buttonPressed()`, `getState()`, debounce handling |
| [Ultrasonic.md](Ultrasonic.md) | HC-SR04 Sensor | `distCm()`, `distMm()`, `near()`, `avg()`, `update()` |
| [LCD.md](LCD.md) | I2C LCD Display | `clear()`, `move_to()`, `putstr()`, `backlight_on()`, `custom_char()` |
| [RGB.md](RGB.md) | RGB LEDs | `setColour()`, `setHex()`, `setNamedColour()`, `fadeTo()`, `update()` |

Start by reading the LED and Servo docs — they're the most commonly used and demonstrate the `update()` pattern clearly.

### Step 2: Work Through the Projects

The `projects/` folder is organised by component, with progressively complex examples:

**Start here — LEDs:**

| Project | What It Does |
|:---|:---|
| [led_on.py](../projects/LED/led_on.py) | Turn on an external LED — the "Hello World" |
| [onboard_led_blink.py](../projects/LED/onboard_led_blink.py) | Blink the Pico's onboard LED |
| [external_led_blink.py](../projects/LED/external_led_blink.py) | Blink an external LED on a GPIO pin |
| [external_led_brightness.py](../projects/LED/external_led_brightness.py) | PWM brightness control |
| [two_leds_blink_and_fade.py](../projects/LED/two_leds_blink_and_fade.py) | Two LEDs running different animations simultaneously |

**Then move to Servos:**

| Project | What It Does |
|:---|:---|
| [servo_move_to_angle.py](../projects/Servo/servo_move_to_angle.py) | Move a servo to a specific angle |
| [servo_sweep.py](../projects/Servo/servo_sweep.py) | Sweep from 0° to 180° |
| [servo_oscillate.py](../projects/Servo/servo_oscillate.py) | Continuous back-and-forth oscillation |

**Then multi-component projects:**

| Project | What It Does |
|:---|:---|
| [leds_and_servo.py](../projects/multi_component_projects/leds_and_servo.py) | LEDs + Servo running together |
| [sound_sensor_led.py](../projects/multi_component_projects/sound_sensor_led.py) | Sound sensor triggering an LED |
| [sound_sensor_servo.py](../projects/multi_component_projects/sound_sensor_servo.py) | Sound sensor driving a servo |
| [ultrasonic_led_baremetal.py](../projects/multi_component_projects/ultrasonic_led_baremetal.py) | Ultrasonic sensor controlling an LED |

**Then the advanced stuff:**

| Project | What It Does |
|:---|:---|
| [schedulerDemo.py](../projects/schedulerDemo.py) | Running multiple task modules as simultaneous processes |
| [buttonTogglePrograms.py](../projects/buttonTogglePrograms.py) | Button-driven program switching with OLED menu, persistence, watchdog |
| [Computer Vision projects](../projects/Computer_Vision/) | Gesture control over Wi-Fi (PC → Pico) |

### Step 3: Build Your Own

At this point you've seen the pattern:

1. Import from `stansmicropy`
2. Instantiate the component with its GPIO pin
3. Call the behaviour method (`blink()`, `sweep()`, `fadeTo()`, etc.)
4. Call `update()` in your `while True` loop

The libraries handle the rest. Build something.


