import picamera
import numpy as np
import time

class MotionDetection:
    def __init__(self, threshold=40000000, save_directory="captures"):
        self.threshold = threshold
        self.save_directory = save_directory
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30
        self.last_frame = None

    def detect_motion(self):
            current_frame = np.empty((480, 640, 3), dtype=np.uint8)
            self.camera.capture(current_frame, format='rgb', use_video_port=True)

            if self.last_frame is None:
                self.last_frame = current_frame
                return None

            diff = np.sum(np.abs(current_frame.astype(np.int32) - self.last_frame.astype(np.int32)))

            if diff > self.threshold:           
                return current_frame
            else:
                self.last_frame = current_frame
                return None
            
    def capture_image(self):
        frame = np.empty((480, 640, 3), dtype=np.uint8)
        self.camera.capture(frame, format='rgb', use_video_port=True)
        return frame