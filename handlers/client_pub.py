import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from cryptography.fernet import Fernet

def encrypt_payload(payload):
    cipher_key = b'xqi9zRusHkcv3Om050HwX82eMTO-LbeW4YlqVVEzpw8='
    cipher = Fernet(cipher_key)
    encrypted_payload = cipher.encrypt(payload.encode('utf-8'))
    return encrypted_payload.decode()

def connect_to_broker(url_str):
    global mqttc
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqttc.on_connect = on_connect

    ca_cert_path = "/home/if22b009/projects/Smart Home Monitoring/handlers/broker.emqx.io-ca.crt"
    mqttc.tls_set(ca_cert_path)

    url = urlparse(url_str)
    if url.username:
        mqttc.username_pw_set(url.username, url.password)
    try:
        print("Connecting to " + url_str)
        mqttc.connect(url.hostname, url.port)
        mqttc.loop_start()
        return mqttc
    except Exception as e:
        print("Connection failed: " + str(e))
        exit(1)


def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    print("Message ID: " + str(mid))

def send_to_broker(topic, payload):
    mqttc.on_publish = on_publish
    try:
        encrypted_payload = encrypt_payload(payload)
        mqttc.publish(topic, encrypted_payload) 
    except Exception as e:
        print("Failed to send message: " + str(e))