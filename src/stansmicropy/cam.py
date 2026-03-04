"""ESP32 Camera module library for capturing frames and streaming video over TCP."""

from stansmicropy.wifiManager import WiFiManager
import camera
import struct
import time


class Camera:
    """
    A Camera control class for ESP32-CAM.
    Supports frame capture, JPEG configuration, and video streaming over TCP.
    """

    def __init__(self, frameSize=camera.FRAME_QVGA, pixelFormat=camera.JPEG, jpegQuality=10):
        """
        Initialize the ESP32 camera hardware.

        Args:
            frameSize (int): Resolution constant (e.g. camera.FRAME_QVGA, camera.FRAME_VGA).
            pixelFormat (int): Pixel format constant (e.g. camera.JPEG, camera.RGB565).
            jpegQuality (int): JPEG quality (0-63, lower is higher quality).
        """
        self.frameSize = frameSize
        self.pixelFormat = pixelFormat
        self.jpegQuality = jpegQuality
        self.streaming = False
        self.streamClient = None
        self.delay = 0
        self.lastUpdate = time.ticks_ms()

        # Initialize camera
        camera.init(0, format=pixelFormat, framesize=frameSize)
        camera.quality(jpegQuality)

    # ------------------- Core Helper -------------------

    def _sendFrame(self, clientSocket, frame):
        """
        Send a single JPEG frame over TCP with a 4-byte length header.
        """
        frameLen = struct.pack('<I', len(frame))
        clientSocket.send(frameLen)
        clientSocket.send(frame)

    # ------------------- Public Methods -------------------

    def capture(self):
        """
        Capture a single frame from the camera.

        Returns:
            bytes: The captured frame data (JPEG or raw depending on pixel format).
        """
        return camera.capture()

    def setFrameSize(self, frameSize):
        """
        Change the camera resolution.

        Args:
            frameSize (int): Resolution constant (e.g. camera.FRAME_QVGA).
        """
        self.frameSize = frameSize
        camera.framesize(frameSize)

    def setQuality(self, quality):
        """
        Set JPEG compression quality.

        Args:
            quality (int): Quality value 0-63 (lower is higher quality).
        """
        self.jpegQuality = quality
        camera.quality(quality)

    def flip(self, enable=True):
        """
        Vertically flip the camera image.

        Args:
            enable (bool): True to flip, False for normal orientation.
        """
        camera.flip(1 if enable else 0)

    def mirror(self, enable=True):
        """
        Horizontally mirror the camera image.

        Args:
            enable (bool): True to mirror, False for normal orientation.
        """
        camera.mirror(1 if enable else 0)

    def startStream(self, wifiManager, fps=15):
        """
        Begin non-blocking video stream. Call update() in a loop to send frames.
        Must call wifiManager.wait_for_client() before starting.

        Args:
            wifiManager (WiFiManager): An active WiFiManager with a connected client.
            fps (int): Target frames per second.
        """
        if not wifiManager.client_socket:
            print("No client connected. Call wifiManager.wait_for_client() first.")
            return

        self.streamClient = wifiManager.client_socket
        self.delay = int((1 / fps) * 1000)  # store as ms
        self.streaming = True
        self.lastUpdate = time.ticks_ms()
        print("Streaming started...")

    def stopStream(self):
        """
        Stop an active video stream.
        """
        self.streaming = False
        self.streamClient = None
        print("Streaming stopped.")

    def release(self):
        """
        Deinitialize the camera hardware.
        """
        camera.deinit()

    # ------------------- Non-blocking Update -------------------

    def update(self):
        """
        Must be called in a loop for non-blocking streaming.
        Captures and sends one frame per tick at the configured FPS.
        """
        if not self.streaming:
            return

        now = time.ticks_ms()

        # Respect delay timing
        if time.ticks_diff(now, self.lastUpdate) < self.delay:
            return

        self.lastUpdate = now

        try:
            frame = self.capture()
            if frame:
                self._sendFrame(self.streamClient, frame)
        except Exception as e:
            print(f"Stream error: {e}")
            self.stopStream()
