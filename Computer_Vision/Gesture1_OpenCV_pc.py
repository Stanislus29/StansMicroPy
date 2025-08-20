import cv2
import numpy as np
import socket

# --- Setup Wi-Fi connection to Pico ---
PICO_IP = "10.170.152.90"   # Replace with your Pico's IP
PICO_PORT = 12345           # Same port used on Pico
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((PICO_IP, PICO_PORT))

# --- Initialize camera ---
cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Optical flow to detect motion
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None,
                                        0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    # Average vertical motion
    vertical_motion = np.mean(flow[..., 1])

    command = None
    if vertical_motion < -1:   # hand moves upward/forward
        command = "FORWARD"
    elif vertical_motion > 1:  # hand moves downward/backward
        command = "BACKWARD"

    if command:
        print("Sending:", command)
        client_socket.send(command.encode('utf-8'))

    # Show camera feed
    cv2.imshow("Gesture Control", frame)
    prev_gray = gray

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
client_socket.close()
cv2.destroyAllWindows()