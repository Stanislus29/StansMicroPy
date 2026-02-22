# Computer Vision

PC-side Python scripts that use OpenCV and MediaPipe for real-time computer vision. These scripts capture webcam input, process it, and send commands to the Raspberry Pi Pico over Wi-Fi.

## Folder Structure

```css
Computer_Vision/
├── gesture_control.py   # Detect gestures via optical flow, send FORWARD/BACKWARD to Pico
├── finger_brightness_control.py      # Track finger height via MediaPipe, send brightness to Pico
├── mediapipe_hands_test.py           # Test MediaPipe hand landmark detection (local, no network)
├── MediaPipe_Installation_Guide.md   # Step-by-step MediaPipe install guide
└── COCO_Object_Detection/            # MobileNet SSD object detection (see subfolder README)
    ├── coco_object_detection.py
    ├── deploy.prototxt
    └── mobilenet_iter_73000.caffemodel
```
