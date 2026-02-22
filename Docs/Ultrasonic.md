# Chapter 3: Ultrasonic Sensor 

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model  of the library ```ultrasonic.py```

--- 

## Entity Relationship 

**Entity Relationship Model: ```UltrasonicSensor```**

**Entity: UltrasonicSensor**

**Attributes: (Properties / State)**

```trig``` → Pin object used to send the ultrasonic pulse

```echo``` → Pin object used to receive the echo response

```max_time``` → Maximum echo timeout (in microseconds), derived from max_cm

```_distance``` → Last successfully measured distance in centimeters

```_last_read``` → Timestamp of the last distance update (used for non-blocking logic)

```_interval``` → Time interval (ms) between auto-refresh distance readings

**Methods (Behaviours)**

```__init__(trig, echo, max_cm=400)``` → Initialize the trigger and echo pins, and configure max range

```_pulse()``` → Send a 10 µs pulse on the trigger pin (private helper)

```_readDistance()``` → Perform a single ultrasonic read and return distance (private helper)

```update()``` → Non-blocking refresh of the sensor’s distance measurement (call repeatedly in loop)

```distCm()``` → Return the last measured distance in centimeters

```distMm()``` → Return the last measured distance in millimeters

```avg(count=3, gap=50)``` → Take multiple measurements and return their average (blocking)

```near(threshold)``` → Return True if the last reading is closer than or equal to threshold (cm)

```setInterval(ms)``` → Set the update interval (in milliseconds) for non-blocking updates

**Relationships**

- Uses Pin and time_pulse_us from MicroPython’s machine module

- Depends on time module for millisecond tracking and delays

- Designed to be integrated with actuators (e.g. LED, Servo) in interactive systems