from machine import Pin
import time

class Button:
    def __init__(self, pin_number, pull=Pin.PULL_UP, debounce_ms=200):
        self.pin = Pin(pin_number, Pin.IN, pull)
        self.last_pressed_time = 0
        self.debounce_ms = debounce_ms
        self.state = False  # This is the boolean you can use to control things

    def buttonPressed(self):
        current_time = time.ticks_ms()

        # If button is pressed (active low)
        if self.pin.value() == 0:
            if time.ticks_diff(current_time, self.last_pressed_time) > self.debounce_ms:
                self.last_pressed_time = current_time

                # Toggle internal state
                self.state = not self.state
                print(f"Button pressed! State is now: {self.state}")

    def getState(self):
        return self.state
    
#Basic test function    
if __name__ == "__main__":
    button = Button(pin_number=16)          # Button on GPIO16
    led = Pin("LED", Pin.OUT)               # Onboard LED

    print("Press the button to toggle the LED.")

    while True:
        button.buttonPressed()
        
        # Use the boolean to control something
        if button.getState():
            led.on()
        else:
            led.off()

        time.sleep(0.01)