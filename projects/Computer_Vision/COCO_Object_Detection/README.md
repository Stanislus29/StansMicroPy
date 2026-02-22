# COCO Object Detection

Real-time object detection using a pre-trained MobileNet SSD model (trained on the COCO dataset). Detects objects from a webcam feed and sends detected labels to the Raspberry Pi Pico over Wi-Fi.

## Folder Structure

```css
COCO_Object_Detection/
├── coco_object_detection.py          # Run webcam detection, draw boxes, send labels to Pico
├── deploy.prototxt                   # Model architecture definition (Caffe format)
└── mobilenet_iter_73000.caffemodel   # Pre-trained MobileNet SSD weights
```

## Supported Classes

background, aeroplane, bicycle, bird, boat, bottle, bus, car, cat, chair, cow, diningtable, dog, horse, motorbike, person, pottedplant, sheep, sofa, train, tvmonitor
