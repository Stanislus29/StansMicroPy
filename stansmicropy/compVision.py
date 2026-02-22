"""Computer Vision library wrapping MediaPipe Hand Landmarker for simplified hand tracking."""

import cv2
import mediapipe as mp
import numpy as np
import urllib.request
from pathlib import Path

# Model is stored alongside this library file
_MODEL_PATH = Path(__file__).resolve().parent / "hand_landmarker.task"
_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
)

# Hand landmark connections for drawing
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),          # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),          # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12),     # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16),   # Ring finger
    (13, 17), (17, 18), (18, 19), (19, 20),  # Pinky
    (0, 17),                                  # Palm
]

# Landmark indices by name for convenience
LANDMARK = {
    "wrist": 0,
    "thumb_tip": 4,
    "index_tip": 8,
    "middle_tip": 12,
    "ring_tip": 16,
    "pinky_tip": 20,
}


def _ensure_model():
    """Download the hand landmarker model if it doesn't exist locally."""
    if not _MODEL_PATH.exists():
        print("Downloading hand landmarker model...")
        urllib.request.urlretrieve(_MODEL_URL, str(_MODEL_PATH))
        print("Download complete.")


class HandLandmarker:
    """Wrapper for MediaPipe Hand Landmarker (Tasks API).

    Usage:
        tracker = HandLandmarker()
        while True:
            # ... capture frame as BGR numpy array ...
            results = tracker.detect(frame)
            if results.hand_landmarks:
                tracker.draw(frame, results)
            cv2.imshow("Hands", frame)
        tracker.close()
    """

    def __init__(self, num_hands=2, min_detection_confidence=0.5,
                 min_presence_confidence=0.5, min_tracking_confidence=0.5):
        _ensure_model()

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(_MODEL_PATH)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self._landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)
        self._timestamp_ms = 0

    def detect(self, bgr_frame):
        """Detect hand landmarks in a BGR image (e.g. from cv2.VideoCapture).

        Args:
            bgr_frame: A BGR numpy array (OpenCV format).

        Returns:
            A HandLandmarkerResult with .hand_landmarks and .handedness lists.
        """
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self._landmarker.detect_for_video(mp_image, self._timestamp_ms)
        self._timestamp_ms += 33  # ~30 FPS
        return result

    def draw(self, image, results):
        """Draw all detected hand landmarks and connections onto the image.

        Args:
            image:   The BGR frame to draw on (modified in place).
            results: The HandLandmarkerResult returned by detect().
        """
        if not results.hand_landmarks:
            return
        for hand_landmarks in results.hand_landmarks:
            self._draw_single_hand(image, hand_landmarks)

    @staticmethod
    def get_landmark(results, landmark_name, hand_index=0):
        """Get the (x, y, z) normalized coordinates of a named landmark.

        Args:
            results:       HandLandmarkerResult from detect().
            landmark_name: One of 'wrist', 'thumb_tip', 'index_tip',
                           'middle_tip', 'ring_tip', 'pinky_tip',
                           or an integer index (0–20).
            hand_index:    Which detected hand (default 0 = first).

        Returns:
            A landmark object with .x, .y, .z (0.0–1.0 normalized),
            or None if no hand was detected.
        """
        if not results.hand_landmarks or hand_index >= len(results.hand_landmarks):
            return None
        if isinstance(landmark_name, int):
            idx = landmark_name
        else:
            idx = LANDMARK[landmark_name]
        return results.hand_landmarks[hand_index][idx]

    def close(self):
        """Release MediaPipe resources."""
        self._landmarker.close()

    # --- Private helpers ---

    @staticmethod
    def _draw_single_hand(image, hand_landmarks):
        """Draw landmarks and connections for one hand."""
        h, w, _ = image.shape
        points = []
        for lm in hand_landmarks:
            px, py = int(lm.x * w), int(lm.y * h)
            points.append((px, py))
            cv2.circle(image, (px, py), 5, (0, 255, 0), -1)
        for start, end in HAND_CONNECTIONS:
            cv2.line(image, points[start], points[end], (255, 255, 255), 2)

class gestureControl:
    # --- Initialize camera ---

    def __init__(self):
        cap = cv2.VideoCapture(0)
        ret, prev_frame = cap.read()
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Optical flow to detect motion
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, np.zeros_like(prev_gray, dtype=np.float32), 0.5, 3, 15, 3, 5, 1.2, 0)
                                                
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

            # Average vertical motion
            vertical_motion = np.mean(flow[..., 1])

            command = None
            if vertical_motion < -1:   # hand moves upward/forward
                command = "FORWARD"
            elif vertical_motion > 1:  # hand moves downward/backward
                command = "BACKWARD"

            # Show camera feed
            cv2.imshow("Gesture Control", frame)
            prev_gray = gray

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        return command



def main():
    """Test the HandLandmarker by showing webcam feed with landmarks drawn."""
    tracker = HandLandmarker()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = tracker.detect(frame)
        tracker.draw(frame, results)
        cv2.imshow("Hand Landmarks", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    tracker.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()                