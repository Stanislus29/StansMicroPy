# Chapter 1: LEDs

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents an object-oriented approach to programming Light-Emmiting Diodes (LEDs). This object-orineted approach allows for easy scalability and ease of teaching to leaners. 

The examples discussed in this document are:

1. Blinking one LED, and performing pulse width modulation on another simultaneously.
2. Blinking the onboard LED, and an external LED simultaneously. 
3. Blinking an external LED only.
4. Blinking the onboard LED only. 
5. Setting the brightness of an external LED.

--- 

## Entity Relationship 

**Entity Relationship Model: ```LED Class```**

**Entity: LED**

**Attributes (Properties / State)**

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

*The attributes are the lower level of abstraction and are embedded within the various method functions. By creating a single file [ledclass.py](C:\Users\DELL\Documents\blink\Libraries\ledclass.py) which contains the class LED, we provide a means to make easily understandable code which de-abstracts the lower level functions making it easier for learners*

**Methods (Behaviors)**

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

## INSTALLALING  

1. Open the file directory in your IDE