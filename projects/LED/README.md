# LED Examples

Examples for controlling LEDs with the Raspberry Pi Pico, from basic blinking to PWM brightness control.

## Folder Structure

```css
LED/
├── led_blink_baremetal.py          # Blink LED using bare machine.Pin (no library)
├── led_on.py                       # Turn onboard LED on permanently (bare machine.Pin)
├── onboard_led_blink.py            # Blink the Pico's onboard LED (LED library)
├── external_led_blink.py           # Blink an external LED on GPIO 21 (LED library)
├── onboard_and_external_blink.py   # Blink onboard + external LEDs simultaneously
├── two_leds_blink_and_fade.py      # Blink one LED while fading another with PWM
└── external_led_brightness.py      # Set external LED to 50% brightness via PWM
```
