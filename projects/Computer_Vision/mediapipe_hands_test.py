"""Test MediaPipe Hand Landmarker by detecting hand landmarks on a webcam feed and drawing them on screen."""

# Import Models
import cv2
import mediapipe as mp
import urllib.request
from pathlib import Path

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

# Initialize MediaPipe Hand Landmarker (Tasks API)
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Configure hand landmarker options
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
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
if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()

print("Press 'q' to quit")
frame_timestamp_ms = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to MediaPipe Image and detect landmarks
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)
    frame_timestamp_ms += 33  # ~30 FPS

    # Draw landmarks
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            draw_hand_landmarks(frame, hand_landmarks)

    # Show result
    cv2.imshow("Hand Tracking", frame)

    # Exit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

landmarker.close()
cap.release()
cv2.destroyAllWindows()