# RASPBERRY PI PICO CODING GUIDE 

**Author: Somtochukwu Stanislus Emeka-Onwuneme**

---

This guide provides an approach for engineers to install the relevant firmware on the Pico board, as well as an explanation into the object-oriented methodologies which we will be using to make learning easier for our leaners. 

It covers the following: 
1. How to install Micropython and flash the firmware onto the board 
2. Programming approach, creating libraries 
3. Uploading libraries using mpremote

---

## How To Install MicroPython 

1. Install the .uf2 firmware files. The files for the MicroPython firmware for the **Pico W** and the **Pico 2W** can be found here: [PicoFirmware](C:\Users\DELL\Documents\blink\Pico_MicroPython_Firmware). Install the required firmware for your board.

2. Plug in the device holding the ```BOOTSEL``` button, it should appear like a drive. Drag and drop the .uf2 file into the drive, wait a while for the firmware to install, the drive should disappear from your screen. This confirms that the firmware has been flashed. 

## Using VsCode 

Whilst Thonny IDE is the mainstream choice for programming the Pico and is suitable for learners, I believe VsCode offers a lot more particularly in it's ability to easily connect with your github repo. It should be the preferred choice for engineers. To use the Pico on VsCode, install the folllowing dependencies:

1. Install Python. At the time this doc was written, my version of choice is Python 3.13.5. Install from here: [Python3.13.5_download](https://www.python.org/downloads/release/python-3135/). 

N.B: Ensure that during installation you click **'Add Python to Path'**

2. Install the MicroPico extension 

3. Install mpremote (REPL and file management)

```bash 
pip install mpremote
```

With the firmware and other dependencies installed, restart VsCode, and plug in your board. Press ```Ctrl + Shift + P```, and type ```MicroPico: Connect```, this should automatically connect the Pico to VsCode if other dependencies are installed correctly. 

## Object-Oriented Approach 

The Object-Oriented approach is chosen as it allows for easy scalability, and ease of teaching to learners. The approach involves the creation of libraries which handle the lower-level abstraction work, while the programmer operates at a higher level of abstraction, calling only the methods. 

For example, we create a folder called ```Libraries``` which contains the libraries to program components like LEDs, Keypads, Servo motors, Ultasonic Sensors. The creation of this folder allows us to simplify coding by installing the lower level work in these libraries, this making our code more custom, and easier to understand.

**N.B:** Ensure you have a folder named ```_init.py_```, this causes Python to treat Libraries as a package. Crucial when running from VsCode directly.

For example, for an LED which can exhibit the following behaviours:

1. Turning on or off
2. Blinking 
3. PWM 

We create a library called ```led.py``` which can handle the lower level functions like calculating delay times, and duty cycles, and concern ourselves with only the method calls. 

The library ```led.py```, holds the following attributes of the class ```LED```:

```pin``` → GPIO pin (string or integer)

```pwm``` → PWM object (or None if not used)

```mode``` → Current operation mode (None, 'blink', 'fade')

```last_update``` → Timestamp for last state change

```state``` → Current digital state (0 = OFF, 1 = ON)

```blink_delay``` → Time (ms) between blinks

```blink_times``` → Number of blinks (None = infinite)

```blink_count``` → Blinks completed

```fade_min``` → Minimum brightness (%)

```fade_max```→ Maximum brightness (%)

```fade_step``` → Increment/decrement per update

```fade_delay``` → Time (ms) between brightness changes

```brightness``` → Current brightness (%)

```direction``` → Direction of fade (1 = increase, -1 = decrease)

*The attributes are the lower level of abstraction and are embedded within the various method functions. By creating a single file [led.py](Libraries/led.py) which contains the class LED, we provide a means to make easily understandable code which de-abstracts the lower level functions making it easier for learners*

and offers the following methods:

```on()``` → Turn LED fully ON (digital mode).

```off()``` → Turn LED fully OFF (digital mode).

```enablePwm()``` → Initialize PWM for brightness control.

```setBrightness(percent)``` → Set brightness level (0–100%) via PWM.

```blink(delay, times)``` → Start non-blocking blink animation.

```fade(minP, maxP, step, delay)``` → Start non-blocking fade animation.

```update()``` → Refresh LED state (called in main loop).

*This higher-level of abstraction allows for coding ease and easy scalability*

**Relationships**

- LED ↔ Pin
    - 1 LED controls 1 Pin (mandatory).

- LED ↔ PWM
    - 1 LED may use 1 PWM (optional, only for brightness/fade).

- LED ↔ Mode
    - 1 LED has 1 mode at a time (blink, fade, or None).

The focus on creating a library allows us to write custom code based on the methods.

For example: Code to turn on an external LED

```python
from machine import Pin 
from Libraries.led import LED

ExtLed = LED(21)
ExtLed.on()
```

This is easier to understand and scale than conventional codes. Conventional code for this would be: 

```python
from machine import Pin 

ExtLed = Pin (21, Pin.OUT)
ExtLed.value(1)
```

The code to turn on an LED perhaps isn't an ideal example. Let's look at applying Pulse Width Modulation to fade an LED.

Using our Object-Oriented Approach
```python 
from Libraries.led import LED
import time

pwmLed = LED(22)

pwmLed.fade(minP=20, maxP=80, step=5, delay=0.05)

while True:
    pwmLed.update()
```

Comparing to the functional code (non-OOL):

```python 
from machine import Pin, PWM
import time

# Setup PWM on pin 21
pwm = PWM(Pin(21))
pwm.freq(1000)  # 1kHz frequency

# Helper to set brightness (0-100%)
def set_brightness(pwm, percent):
    duty = int((percent / 100) * 65535)  # convert to 16-bit duty
    pwm.duty_u16(duty)

# Helper to fade
def fade(minP, maxP, step, delay):
    if start < end:
        rng = range(minP, maxP + 1, step)
    else:
        rng = range(minP, maxP - 1, -step)
    for level in rng:
        set_brightness(pwm, level)
        time.sleep(delay)

# Fade loop
while True:
    fade(20, 80, 5, 0.05)  # fade up
    fade(80, 20, 5, 0.05)  # fade down
```

We see that the Object-Oriented approach allows us to avoid the overhead of lower-level abstraction, and provides scalable and modular code

## Updating Pico's lib folder 

Ensure mpremote was installed from earlier, then run this in bash. 

```bash
mpremote connect auto mkdir :/lib
mpremote connect auto cp -r Libraries :/lib
```

This adds all updates to your Libraries into the ```lib``` directory in Pico's file management system 

## Uploading Examples to Pico 

You can push the Examples (if required) to the Pico board 

```bash
mpremote connect auto mkdir :/Examples
mpremote connect auto cp -r Examples :/Examples
```
**N.B:** ```-r``` copies the entire folder recursively 
```mpremote connect auto mkdir :/Examples``` creates a folder named "Examples" on the Pico if it doesn't exist already

Or if you want to only update or upload a single example 
```bash
mpremote connect auto mkdir :/Examples
mpremote connect auto cp Examples/LED/OnBoardLedBlink.py :/Examples
```

Verify 
```bash 
mpremote connect auto ls :/Examples
```

You should see 
```bash 
ls :/Examples
         244 OnBoardLedBlink.py
```        

## Deleting Files from the Pico

A generic file on the Pico board ```e.g ledclass.py``` can be deleted via the following command in the bash. Assuming the directotry is ```lib/Libraries/ledclass.py

```bash 
mpremote connect auto rm :/lib/Libraries/ledclass.py
```

If you want to delete an entire directory, you must first delete all the files within it, and then use this command: 

```bash 
mpremote connect auto rmdir :/lib/Libraries
```


---

© STEMAIDE Africa 2025 - Internal Technical Report
