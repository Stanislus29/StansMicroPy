from machine import Pin
import utime

# Keypad setup
rows = [Pin(i, Pin.OUT) for i in (6, 7, 8, 9)]   # GP2 to GP5
cols = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in (5, 4, 3, 2)]  # GP6 to GP9

keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

def scan_keypad():
    for row_num, row_pin in enumerate(rows):
        row_pin.high()
        for col_num, col_pin in enumerate(cols):
            if col_pin.value():
                utime.sleep_ms(20)  # debounce delay
                if col_pin.value():  # confirm still pressed
                    row_pin.low()
                    return keys[row_num][col_num]
        row_pin.low()
    return None

# Main loop
print("Ready. Press a key...")

while True:
    key = scan_keypad()
    if key:
        print("Key pressed:", key)
        utime.sleep(0.3)
