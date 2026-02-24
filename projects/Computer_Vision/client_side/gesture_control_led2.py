"""Use index finger vertical motion to control LED brightness over Wi-Fi."""

from desktop.compVision import HandLandmarker
import cv2
import socket

# --- Setup TCP connection to Pico ---
PICO_IP = "10.149.168.242"
PICO_PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((PICO_IP, PICO_PORT))


def main():
    tracker = HandLandmarker()
    cap = cv2.VideoCapture(0)

    last_brightness = None
    smoothed_y = None
    alpha = 0.2  # smoothing factor (lower = smoother)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape

        results = tracker.detect(frame)
        tracker.draw(frame, results)

        brightness = None
        direction = ""

        if results.hand_landmarks:
            hand_landmarks = results.hand_landmarks[0]  # First detected hand

            # Convert normalized y to pixel space
            index_tip_y = int(hand_landmarks[8].y * h)

            # Smooth movement
            if smoothed_y is None:
                smoothed_y = index_tip_y
            else:
                smoothed_y = int(alpha * index_tip_y + (1 - alpha) * smoothed_y)

            # Map pixel height to brightness (invert so up = brighter)
            brightness = int((1 - smoothed_y / h) * 255)
            brightness = max(0, min(255, brightness))

            # Only send if meaningful change
            if last_brightness is None or abs(brightness - last_brightness) > 5:
                client_socket.send((str(brightness) + "\n").encode("utf-8"))

                if last_brightness is not None:
                    if brightness > last_brightness:
                        direction = "UP"
                    elif brightness < last_brightness:
                        direction = "DOWN"

                last_brightness = brightness

        # --- Overlay Text ---
        if brightness is not None:
            cv2.putText(frame,
                        f"Brightness: {brightness}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2)

            if direction:
                cv2.putText(frame,
                            f"Direction: {direction}",
                            (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (255, 255, 0),
                            2)

        cv2.imshow("Gesture Brightness Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()