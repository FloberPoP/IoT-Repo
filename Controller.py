import os
import time
import signal
import threading
from PIL import Image
from threading import Thread

from sensors.motion import MotionDetection
from sensors.sensehat import read_sensehat_data

from handlers.Email_handler import send_email
from handlers.client_pub import send_to_broker
from handlers.client_pub import connect_to_broker
from handlers.client_sub import MQTTSubscriber
from handlers.storeFileFB import FirebaseStorageHandler
from handlers.blynk_handler import set_event
from handlers.blynk_handler import set_motion
from handlers.blynk_handler import check_button_press


class SmartHomeController:
    def __init__(self):
        self.shutdown_flag = threading.Event()
        self.filepath = "/home/if22b009/Repo/pictures"
        self.singlePicPath = "/home/if22b009/Repo/tmp"

        self.motion_detector = MotionDetection()
        self.motion_thread = Thread(target=self.motion_detection_loop)
        self.motion_thread.daemon = True

        self.publish_data_thread = Thread(target=self.publish_data)
        self.publish_data_thread.daemon = True

        self.control_thread = Thread(target=self.control_loop)
        self.control_thread.daemon = True

        self.storageHandler = FirebaseStorageHandler()

        self.subscriber = MQTTSubscriber("mqtt://broker.emqx.io:1883")
    

    def motion_detection_loop(self):
        connect_to_broker("mqtt://broker.emqx.io:8883")
        os.makedirs(self.filepath, exist_ok=True) 

        while not self.shutdown_flag.is_set():
            motion_image = self.motion_detector.detect_motion()
            if motion_image is not None:
                print("Motion detected!")
                filename = f"{int(time.time())}.jpg"
                filepath = os.path.join(self.filepath, filename)
                image = Image.fromarray(motion_image)
                image.save(filepath)
                topic = "if22b009/motion/detection"
                send_to_broker(topic, "1")
            time.sleep(5)

    def publish_data(self):
        self.subscriber.connect()
        while not self.shutdown_flag.is_set():
            data = read_sensehat_data()
            received_data = self.subscriber.receive()
            if received_data and received_data[1] == "1":
                latest_image = sorted(os.listdir(self.filepath))[-1]
                image_path = os.path.join(self.filepath, latest_image)
                #send_email(image_path, data, 0) 
                image_url = self.storageHandler.store_file(image_path)
                set_motion(image_url)
                os.remove(image_path)
            set_event(data)
            time.sleep(10)

    def control_loop(self):
        while not self.shutdown_flag.is_set():
            if check_button_press():
                data = read_sensehat_data()
                image_data = self.motion_detector.capture_image()
                filename = f"{int(time.time())}.jpg"
                filepath = os.path.join(self.singlePicPath, filename)
                image = Image.fromarray(image_data)
                image.save(filepath)
                set_event(data)
                send_email(filepath, data, 1)
                image_url = self.storageHandler.store_file(filepath)
                set_motion(image_url)
                os.remove(filepath)

    def run(self):
        self.motion_thread = threading.Thread(target=self.motion_detection_loop)
        self.publish_data_thread = threading.Thread(target=self.publish_data)
        self.control_thread = threading.Thread(target=self.control_loop)

        self.motion_thread.start()
        self.publish_data_thread.start()
        self.control_thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutdown requested")
            self.shutdown_flag.set()

        self.motion_thread.join()
        self.publish_data_thread.join()
        self.control_thread.join()
        print("All threads terminated.")

if __name__ == "__main__":
    controller = SmartHomeController()
    controller.run()