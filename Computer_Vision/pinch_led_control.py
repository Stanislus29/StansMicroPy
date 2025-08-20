import cv2
import mediapipe as mp
import socket

# --- Configuration ---
PICO_IP = "10.170.152.90"    # Replace with Pico's IP
PICO_PORT = 5005

# Setup socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)  # Mirror view
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    brightness = 0  # Default brightness

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Use Y position of index finger tip (landmark 8) for brightness
            index_tip_y = hand_landmarks.landmark[8].y
            brightness = int((1 - index_tip_y) * 255)  # Map 0-1 to 255

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Send brightness value over UDP
    message = str(brightness).encode()
    sock.sendto(message, (PICO_IP, PICO_PORT))

    # Display
    cv2.putText(image, f'Brightness: {brightness}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.imshow('Gesture Control', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()