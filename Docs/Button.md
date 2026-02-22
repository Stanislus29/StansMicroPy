# Chapter 5: Button

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model of the library ```pushbutton.py```

---

## Entity Relationship

**Entity Relationship Model: ```Button```**

**Entity: Button**

**Attributes (Properties / State)**

```pin``` → machine.Pin object configured as an input with optional pull-up/down.

```last_pressed_time``` → Timestamp (ms) of last valid press for debounce handling.

```debounce_ms``` → Minimum time (ms) between valid presses.

```state``` → Current toggle state (False = OFF, True = ON).

Methods (Behaviors)

```__init__(pin_number, pull=Pin.PULL_UP, debounce_ms=200)``` → Constructor; initializes pin, state, debounce parameters.

```buttonPressed()``` → Checks button press, applies debounce, toggles state if valid.

```getState()``` → Returns current boolean toggle state.

**Relationships**

- Button ↔ Pin

    - 1 Button is connected to 1 Pin (mandatory).

- Button ↔ State

    - 1 Button maintains 1 toggle state (True/False) at a time.

- Button ↔ Debounce

    - 1 Button has 1 debounce time setting.