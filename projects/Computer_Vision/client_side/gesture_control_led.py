from desktop.compVision import GestureControl
import cv2
import socket

# --- Setup TCP connection to Pico ---
PICO_IP = "10.149.168.242"
PICO_PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((PICO_IP, PICO_PORT))

def main():
    gc = GestureControl(movement_threshold=0.015)

    try:
        while True:
            ret, frame = gc.cap.read()
            if not ret:
                break

            command = gc.detect(frame)

            if command:
                print("Gesture detected:", command)
                # Send over TCP
                client_socket.send(command.encode('utf-8'))

            cv2.imshow("Gesture Control", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        gc.close()
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()