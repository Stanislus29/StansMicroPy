import network
import socket
import time

class WiFiManager:
    # Connect to Wi-Fi and setup TCP server socket
    def __init__(self, SSID, PASSWORD, port=12345):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

        self.wlan.connect(SSID, PASSWORD)

        print("Connecting to Wi-Fi...")
        while not self.wlan.isconnected():
            time.sleep(0.5)
        print("Connected, IP:", self.wlan.ifconfig()[0])

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.wlan.ifconfig()[0], port))
        self.server_socket.listen(1)
        self.client_socket = None

    def wait_for_client(self):
        print("Waiting for client connection...")
        self.client_socket, addr = self.server_socket.accept()
        print(f"Client connected from {addr}") 
        return self.client_socket   

    def receive_command(self):
        if not self.client_socket:
            print("No client connected.")
            return None
        try:
            data = self.client_socket.recv(1024)
            if data:
                command = data.decode('utf-8').strip()
                return command
            else:
                print("Client disconnected.")
                self.close_client()
                return None
        except Exception as e:
            print(f"Error receiving command: {e}")
            self.close_client()
            return None

    def close_client(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None

    def close(self):
        self.close_client()
        self.server_socket.close()
        self.wlan.disconnect()
        self.wlan.active(False)