"""Track index finger height via MediaPipe Hands and send brightness values (0–255) to a Pico over UDP."""

import cv2
import mediapipe as mp
import socket
import urllib.request
from pathlib import Path

# --- Configuration ---
PICO_IP = "PICO-IP"    # Replace with Pico's IP
PICO_PORT = 5005

# --- Download hand landmarker model if not present ---
MODEL_PATH = Path(__file__).resolve().parent / "hand_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
)

if not MODEL_PATH.exists():
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(MODEL_URL, str(MODEL_PATH))
    print("Download complete.")

# Setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize MediaPipe Hand Landmarker (Tasks API)
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7,
)

landmarker = HandLandmarker.create_from_options(options)

# Hand landmark connections for drawing
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),          # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),          # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12),     # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16),   # Ring finger
    (13, 17), (17, 18), (18, 19), (19, 20),  # Pinky
    (0, 17),                                  # Palm
]


def draw_hand_landmarks(image, hand_landmarks):
    """Draw hand landmarks and connections on the image."""
    h, w, _ = image.shape
    points = []
    for lm in hand_landmarks:
        px, py = int(lm.x * w), int(lm.y * h)
        points.append((px, py))
        cv2.circle(image, (px, py), 5, (0, 255, 0), -1)
    for start, end in HAND_CONNECTIONS:
        cv2.line(image, points[start], points[end], (255, 255, 255), 2)


# Open webcam
cap = cv2.VideoCapture(0)
frame_timestamp_ms = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)  # Mirror view
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert to MediaPipe Image and detect landmarks
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    results = landmarker.detect_for_video(mp_image, frame_timestamp_ms)
    frame_timestamp_ms += 33  # ~30 FPS

    brightness = 0  # Default brightness

    if results.hand_landmarks:
        for hand_landmarks in results.hand_landmarks:
            # Use Y position of index finger tip (landmark 8) for brightness
            index_tip_y = hand_landmarks[8].y
            brightness = int((1 - index_tip_y) * 255)  # Map 0-1 to 255

            draw_hand_landmarks(image, hand_landmarks)

    # Send brightness value over UDP
    message = str(brightness).encode()
    sock.sendto(message, (PICO_IP, PICO_PORT))

    # Display
    cv2.putText(image, f'Brightness: {brightness}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Gesture Control', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

landmarker.close()
cap.release()
cv2.destroyAllWindows()