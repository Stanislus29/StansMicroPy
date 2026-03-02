"""Use a button to toggle between programs and show on an OLED"""

import time
import json
import gc
from machine import Pin, I2C, WDT
from stansmicropy.oled import SH1106_I2C
from stansmicropy.scheduler import Scheduler

# =========================
# OLED SETUP
# =========================
WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl=Pin(19), sda=Pin(18), freq=100000)
display = SH1106_I2C(128, 64, i2c, addr=0x3C)
display.invert(0)

# =========================
# WATCHDOG
# =========================
wdt = WDT(timeout=3000)  # 3 second timeout

# =========================
# IMPORT PROGRAMS
# =========================
import task.servoTask as servo_task
import task.ledTask as led_task

programs = [servo_task, led_task]

# =========================
# PERSISTENCE
# =========================
CONFIG_FILE = "mode.json"

def load_mode():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("mode", 0)
    except:
        return 0

def save_mode(index):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"mode": index}, f)

current_index = load_mode()
current_program = programs[current_index]

# =========================
# BUTTON SETUP
# =========================
button = Pin(23, Pin.IN, Pin.PULL_UP)

press_start = 0
long_press_time = 800
last_state = 1

# =========================
# SCHEDULER
# =========================
scheduler = Scheduler()

# =========================
# UI ANIMATION
# =========================
menu_offset = 0
target_offset = 0

# def animate_menu():
#     global menu_offset
#     if menu_offset < target_offset:
#         menu_offset += 4
#     elif menu_offset > target_offset:
#         menu_offset -= 4

def draw_menu():
    display.fill(0)

    # Highlight current mode
    y_position = 12 - menu_offset
    for i, prog in enumerate(programs):
        if i == current_index:
            display.fill_rect(0, y_position-2, 128, 12, 1)
            display.text(prog.__name__, 2, y_position, 0)
        else:
            display.text(prog.__name__, 2, y_position, 1)

        y_position += 14

    display.text("RAM: {}k".format(gc.mem_free() // 1024), 32, 50, 1)

    display.show()

# =========================
# SWITCH LOGIC
# =========================
def switch_program(new_index):
    global current_program, current_index, target_offset

    if hasattr(current_program, "cleanup"):
        current_program.cleanup()

    current_index = new_index % len(programs)
    current_program = programs[current_index]
    save_mode(current_index)

    scheduler.tasks.clear()
    scheduler.add_task(current_program)

    if hasattr(current_program, "init"):
        current_program.init()

    target_offset = current_index * 14

# =========================
# INIT FIRST PROGRAM
# =========================
scheduler.add_task(current_program)
if hasattr(current_program, "init"):
    current_program.init()

# =========================
# PROFILER
# =========================
last_profile = time.ticks_ms()
loop_counter = 0
fps = 0

# =========================
# MAIN LOOP
# =========================
while True:
    now = time.ticks_ms()
    state = button.value()

    # Button pressed
    if state == 0 and last_state == 1:
        press_start = now

    # Button released
    if state == 1 and last_state == 0:
        duration = time.ticks_diff(now, press_start)

        if duration > long_press_time:
            switch_program(current_index - 1)
        else:
            switch_program(current_index + 1)

    last_state = state

    # Cooperative scheduler
    scheduler.step()
    scheduler.print_stats

    # UI animation
    # animate_menu()
    draw_menu()

    # Profiling
    loop_counter += 1
    if time.ticks_diff(now, last_profile) > 1000:
        fps = loop_counter
        loop_counter = 0
        last_profile = now

    # Feed watchdog
    wdt.feed()

    time.sleep_ms(10)