from mqtt_objects import MQTT_listener
from databasetools import DBWriter
import time
import os
import dotenv

#get our secrets
dotenv.load_dotenv()
MQTT_BROKER_IP = os.getenv("MQTT_BROKER_IP")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
SQL_HOST = os.getenv("SQL_HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


listener = MQTT_listener(hostname=MQTT_BROKER_IP, port=MQTT_PORT)
writer = DBWriter(data_queue=listener.q,
                  host=SQL_HOST,
                  user=USERNAME,
                  password=PASSWORD,
                  database=DATABASE)

if __name__ == "__main__":
    writer.start()
    listener.start()
    time.sleep(60)
    listener.stop()
    writer.stop()
    writer.join()