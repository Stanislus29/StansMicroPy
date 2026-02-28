from stansmicropy.scheduler import Scheduler
from stansmicropy.oled import SH1106_I2C
from machine import I2C, Pin
import time
import gc

# Import task modules
import  task.servoTask as servo_task
import  task.ledTask as led_task

# Register tasks here
tasks = [servo_task, led_task]

sched = Scheduler(tasks)

sched.initialize()

# =========================
# OLED SETUP
# =========================
WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl=Pin(19), sda=Pin(18), freq=100000)
display = SH1106_I2C(128, 64, i2c, addr=0x3C)
display.invert(0)

menu_offset = 0
target_offset = 0

def draw_menu():
    display.fill(0)

    # Highlight current mode
    y_position = 12 - menu_offset

    display.fill_rect(0, y_position-2, 128, 12, 1)
    display.text(tasks[0].__name__, 2, y_position, 0)

    display.fill_rect(0, y_position+12-2, 128, 12, 1)
    display.text(tasks[1].__name__, 2, y_position+12, 0)

    y_position += 14

    display.text("RAM: {}k".format(gc.mem_free() // 1024), 32, 50, 1)

    display.show()

# Non-blocking loop
while True:
    sched.step()
    sched.print_stats()
    # other logic: button handling, OLED updates, watchdog

    draw_menu()
    time.sleep_ms(1)

# Or use blocking loop for demo
# sched.run_forever()