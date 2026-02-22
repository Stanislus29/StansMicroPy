# Stansberry - Repository with Raspberry Pi Pico Libraries 

**Author:** Somtochukwu Stanislus Emeka-Onwuneme

---

## Folder Structure

```
blink/
├── README.md
├── requirements.txt
├── Computer_Vision/          # PC-side scripts using OpenCV and MediaPipe
│   ├── optical_flow_gesture_control.py
│   ├── finger_brightness_control.py
│   ├── mediapipe_hands_test.py
│   ├── opencv_version_check.py
│   ├── MediaPipe_Installation_Guide.md
│   └── COCO_Object_Detection/
│       ├── coco_object_detection.py
│       ├── deploy.prototxt
│       └── mobilenet_iter_73000.caffemodel
├── Pico_Code/                # Code that runs ON the Pico
│   ├── gesture_servo_server.py
│   ├── brightness_led_server.py
│   └── WiFi_Server/
│       └── wifi_tcp_server.py
├── Examples/                 # MicroPython examples by component
│   ├── Button/
│   │   └── button_toggle_led.py
│   ├── LCD/
│   │   ├── i2c_address_scan.py
│   │   ├── lcd_hello_world.py
│   │   └── lcd_two_lines.py
│   ├── LED/
│   │   ├── led_blink_baremetal.py
│   │   ├── led_on.py
│   │   ├── onboard_led_blink.py
│   │   ├── external_led_blink.py
│   │   ├── onboard_and_external_blink.py
│   │   ├── two_leds_blink_and_fade.py
│   │   └── external_led_brightness.py
│   ├── OLED/
│   │   ├── oled_init_test.py
│   │   ├── oled_temperature_display.py
│   │   └── ssd1306.py
│   ├── RGBLED/
│   │   └── rgb_color_cycle.py
│   ├── Servo/
│   │   ├── servo_move_to_angle.py
│   │   ├── servo_sweep.py
│   │   ├── servo_oscillate.py
│   │   └── servo_sweep_baremetal.py
│   ├── Ultrasonic/
│   │   ├── ultrasonic_measure_distance.py
│   │   ├── ultrasonic_led_servo.py
│   │   └── ultrasonic_led_servo_threshold.py
│   └── Integrated/
│       ├── keypad_read.py
│       ├── sound_sensor_led.py
│       ├── sound_sensor_servo.py
│       ├── ultrasonic_led_baremetal.py
│       └── leds_and_servo.py
├── Libraries/                # Reusable MicroPython libraries
│   ├── __init__.py
│   ├── led.py
│   ├── servo.py
│   ├── ultrasonic.py
│   ├── pushbutton.py
│   ├── RGBLED.py
│   ├── LiquidCrystal.py
│   ├── LCD/
│   │   └── lcdapi.py
│   └── OLED/
│       └── ssd1306.py
├── Docs/                     # Guides and documentation
│   ├── Raspberry_Pi_Pico_Coding_Guide.md
│   ├── LED.md
│   ├── Button.md
│   ├── Servo.md
│   ├── Ultrasonic.md
│   ├── LCD.md
│   ├── RGB.md
│   └── AI_Kit_recommendations.md
└── Firmware/                 # MicroPython .uf2 firmware files
    ├── RPI_PICO_W-20250415-v1.25.0.uf2
    └── RPI_PICO2_W-20250415-v1.25.0.uf2
```

---

## Quick Start

### 1. Flash the Pico
- Hold the **BOOTSEL** button, connect the Pico via USB.
- Copy the appropriate `.uf2` from `Firmware/` to the Pico drive.

### 2. Install PC dependencies
```bash
pip install -r requirements.txt
```

### 3. Upload MicroPython code
Use the [MicroPico VS Code extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) to upload `Libraries/` and `Pico_Code/` scripts to the Pico.

### 4. Run Computer Vision scripts
```bash
python Computer_Vision/Gesture1_OpenCV_pc.py
```

---

## Components Used

- Raspberry Pi Pico W / Pico 2 W
- LEDs, RGB LEDs, Servo motors, Ultrasonic sensors
- LCD (I2C), OLED (SSD1306)
- Webcam (for PC-side vision)

---

## License

Educational use. See `Docs/AI_Kit_recommendations.md` for full kit details.
