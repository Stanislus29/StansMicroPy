## Chapter 6: RGBLED

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model of the library RGLED.py

---

## Entity Relationship

**Entity Relationship Model: ```RGBLED```**

**Entity: RGBLED**

**Attributes (Properties / State)**

```commonAnode``` → Boolean flag indicating whether the LED is wired as common anode (True) or common cathode (False).

```pwmMode``` → Boolean flag indicating whether PWM control is enabled (True) or using simple digital output (False).

```red``` → PWM or Pin object controlling the red channel.

```green``` → PWM or Pin object controlling the green channel.

```blue``` → PWM or Pin object controlling the blue channel.

```currentColour``` → Current RGB colour as a list [R, G, B] with each value from 0–255.

```targetColour``` → Target RGB colour for fade transitions.

```fadeSpeed``` → Integer (1–255) controlling the step size for fading to target colour.

```lastUpdate``` → Timestamp (ms) of last fade update for non-blocking control.

```NAMED_COLOURS``` → Dictionary mapping human-readable colour names to RGB tuples.

**Methods (Behaviours)**

```__init__(redPin, greenPin, bluePin, commonAnode=False, pwm=True)``` → Constructor; sets up pin objects, mode (PWM/digital), and default state.

```_pwmValue(value)``` → Converts 0–255 colour value to 0–65535 PWM duty cycle, accounting for common anode logic.

```_applyColour(r, g, b)``` → Writes the given RGB values to hardware pins.

```setColour(r, g, b)``` → Immediately sets the LED to a specific RGB value.

```setHex(hexCode)``` → Sets the LED colour using a HEX code (#RRGGBB).

```setNamedColour(name)``` → Sets the LED colour using a predefined human-readable name.

```fadeTo(r, g, b, speed=5)``` → Gradually changes the LED to a target RGB value at a given speed (non-blocking).

```update()``` → Updates the LED output for ongoing fade transitions; must be called repeatedly in main loop.

```off()``` → Turns off the LED (sets to [0, 0, 0]).

**Relationships**

- RGBLED ↔ Pin / PWM

    - 1 RGBLED controls three Pin or PWM objects (one per colour channel).

- RGBLED ↔ Colour

    - 1 RGBLED maintains currentColour and targetColour at all times.

- RGBLED ↔ Fade

    - 1 RGBLED uses fadeSpeed and update() to achieve non-blocking fades.

- RGBLED ↔ Named Colours

    - 1 RGBLED can map human-readable colour names to predefined RGB values.