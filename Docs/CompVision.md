# Chapter 10: Computer Vision

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model of the library ```compVision.py```

*Note: This library runs on the desktop (PC), not on the MCU. It is part of the ```desktop``` package in ```src/desktop/``` and depends on OpenCV, MediaPipe, and NumPy.*

---

## Entity Relationship

### Entity Relationship Model: ```HandLandmarker```

**Entity: HandLandmarker**

**Attributes (Properties / State)**

```_landmarker``` → MediaPipe ```HandLandmarker``` object created via the Tasks API. Configured for ```VIDEO``` running mode.

```_timestamp_ms``` → Integer tracking the current frame timestamp in milliseconds. Incremented by 33ms (~30 FPS) on each ```detect()``` call.

**Module-Level Constants**

```_MODEL_PATH``` → Path to the ```hand_landmarker.task``` model file, stored alongside the library.

```_MODEL_URL``` → URL to download the model from Google's MediaPipe model repository if it doesn't exist locally.

```HAND_CONNECTIONS``` → List of (start, end) index tuples defining the line connections between hand landmarks for drawing (thumb, index, middle, ring, pinky, palm).

```LANDMARK``` → Dictionary mapping human-readable landmark names to their integer indices: ```"wrist"``` → 0, ```"thumb_tip"``` → 4, ```"index_tip"``` → 8, ```"middle_tip"``` → 12, ```"ring_tip"``` → 16, ```"pinky_tip"``` → 20.

**Methods (Behaviours)**

```__init__(num_hands=2, min_detection_confidence=0.5, min_presence_confidence=0.5, min_tracking_confidence=0.5)``` → Constructor; ensures the model file is downloaded, then creates a MediaPipe HandLandmarker with the specified confidence thresholds and hand count.

```detect(bgr_frame)``` → Takes a BGR numpy array (e.g. from ```cv2.VideoCapture```), converts to RGB, wraps in a MediaPipe Image, and runs hand landmark detection. Returns a ```HandLandmarkerResult``` with ```.hand_landmarks``` and ```.handedness``` lists.

```draw(image, results)``` → Draws all detected hand landmarks and connections onto the BGR frame in place. Green circles for landmarks, white lines for connections.

```get_landmark(results, landmark_name, hand_index=0)``` → Static method. Returns the (x, y, z) normalised coordinates of a named landmark (e.g. ```"index_tip"```) or integer index (0–20) from the detection results. Returns ```None``` if no hand was detected.

```close()``` → Releases MediaPipe resources.

```_draw_single_hand(image, hand_landmarks)``` → Static method. Internal helper that draws landmarks and connections for one hand.

---

### Entity Relationship Model: ```GestureControl```

**Entity: GestureControl**

**Attributes (Properties / State)**

```cap``` → ```cv2.VideoCapture``` object for the webcam (camera index 0).

```_tracker``` → Internal ```HandLandmarker``` instance configured for single-hand tracking.

```_prev_wrist_y``` → The normalised Y-coordinate of the wrist from the previous frame (0.0 = top, 1.0 = bottom). Used to calculate vertical movement delta. ```None``` when no hand was previously detected.

```_threshold``` → Minimum normalised Y-delta required to trigger a gesture (default 0.015 ≈ 1.5% of frame height).

**Methods (Behaviours)**

```__init__(movement_threshold=0.015)``` → Constructor; opens the webcam, creates a single-hand ```HandLandmarker```, and initialises the movement tracking state.

```detect(frame)``` → Analyses a single BGR frame and returns a command string: ```"FORWARD"``` (hand moved up), ```"BACKWARD"``` (hand moved down), or ```None``` (no hand detected or movement below threshold).

```draw(frame, results=None)``` → Draws hand landmarks on the frame. If results is ```None```, runs detection first.

```close()``` → Releases the camera, MediaPipe resources, and OpenCV windows.

---

### Module-Level Function

```main()``` → Test function. Opens the webcam, runs ```HandLandmarker``` detection on each frame, draws landmarks, and displays the feed. Press 'q' to quit. Useful for verifying the setup.

---

## Relationships

- HandLandmarker ↔ MediaPipe
    - 1 HandLandmarker wraps 1 MediaPipe ```HandLandmarker``` (Tasks API) configured in ```VIDEO``` mode.

- HandLandmarker ↔ Model File
    - Requires ```hand_landmarker.task``` in the same directory. Auto-downloads from Google's servers on first use via ```_ensure_model()```.

- GestureControl ↔ HandLandmarker
    - 1 GestureControl uses 1 HandLandmarker internally for hand tracking.

- GestureControl ↔ Camera
    - 1 GestureControl opens 1 ```cv2.VideoCapture``` for webcam input.

- Desktop ↔ MCU
    - The ```compVision.py``` library runs on the PC. Gesture commands (```"FORWARD"```, ```"BACKWARD"```) are sent to the MCU over Wi-Fi TCP via the client-side scripts in ```projects/Computer_Vision/client_side/```. The MCU receives them using ```WiFiManager.receive_command()```.

- Dependencies
    - ```cv2``` (OpenCV), ```mediapipe```, ```numpy```, ```urllib.request```, ```pathlib```.
