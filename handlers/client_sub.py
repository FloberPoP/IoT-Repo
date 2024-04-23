import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from cryptography.fernet import Fernet

class MQTTSubscriber:
    def __init__(self, broker_url):
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
        self.url = urlparse(broker_url)
        self.messages = []
        self.cipher = Fernet(b'xqi9zRusHkcv3Om050HwX82eMTO-LbeW4YlqVVEzpw8=')

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
            client.subscribe("if22b009/motion/detection")
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        decrypted_message = self.decrypt_payload(msg.payload)
        self.messages.append((msg.topic, decrypted_message))

    def decrypt_payload(self, encrypted_payload):
        try:
            decrypted_payload = self.cipher.decrypt(encrypted_payload)
            return decrypted_payload.decode()
        except Exception as e:
            print("Failed to decrypt message:", str(e))
            return None

    def connect(self):
        self.client.connect(self.url.hostname, self.url.port)
        self.client.loop_start()

    def receive(self):
        if self.messages:
            return self.messages.pop(0)
        return None