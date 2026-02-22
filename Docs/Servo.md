# Chapter 2: Servo Motors

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model  of the library ```servo.py```

--- 

## Entity Relationship 

**Entity Relationship Model: ```servo```**

**Entity: Servo**

**Attributes: (Properties / State)**

```pwm``` – PWM object controlling servo pin

```min_us / max_us``` – Pulse width calibration (µs) for 0°–180°

```current_angle``` – Current angle position

```target_angle``` – Target angle for sweep

```step, delay, last_update``` – Non-blocking motion control

```oscillating, osc_min, osc_max, osc_speed, osc_direction```– For oscillation state

**Methods (Behaviours)**

```setAngle()``` – Move servo immediately

```sweep(start_angle, end_angle, step, delay)``` – Non-blocking sweep from start to target angle

```oscillate(min_angle, max_angle, step, delay)``` – Continuous oscillation

```stopOscillation()``` – Stop oscillation

```calibrate(min_us, max_us)``` – Adjust pulse width limits dynamically

```release()``` – Stop PWM output

```update()``` – Update servo position for sweeps/oscillation (must call repeatedly)

**Relationships**

Uses ```PWM``` and ```Pin``` from MicroPython’s machine module.