import paho.mqtt.client as mqtt
import datetime
from queue import Queue
import dotenv
import os

class MQTT_listener:
    def __init__(self, hostname: str = "localhost", port: int = 1883, subscription:str = "/sensors"):
        self.q = Queue()
        self.client = mqtt.Client("python_listener")
        self.client.connect(hostname, port)
        self.client.subscribe(f"{subscription}/+")
        self.client.on_message = self.on_message

    def start(self):
        print("starting mqtt client loop")
        self.client.loop_forever()
    def stop(self):
        print("stopping mqtt client loop")
        self.client.loop_stop()

    def on_message(self, client, userdata, message):
        sensor_name = message.topic
        sensor_name = sensor_name.split("/")[-1]
        message = str(message.payload.decode("utf-8"))
        t, h = message.split(",")
        temperature = float(t)
        humidity = float(h)
        time_recieved = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        data = (sensor_name, time_recieved, temperature, humidity)
        print("data received:", data)
        self.q.put(data)