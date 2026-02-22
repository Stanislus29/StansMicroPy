# Pico Code

MicroPython scripts that run **on** the Raspberry Pi Pico. These set up the Pico as a Wi-Fi server to receive commands from PC-side computer vision scripts.

## Folder Structure

```css
Pico_Code/
├── gesture_servo_server.py    # TCP server: receive FORWARD/BACKWARD, control a servo
├── brightness_led_server.py   # UDP server: receive brightness (0–255), control LED via PWM
└── WiFi_Server/
    └── wifi_tcp_server.py     # Generic Wi-Fi TCP server template
```
