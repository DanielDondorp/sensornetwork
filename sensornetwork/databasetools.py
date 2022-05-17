from threading import Thread
from mysql import connector
import pandas as pd
import datetime

class DBWriter(Thread):
    def __init__(self, data_queue, host, user, password, database):
        Thread.__init__(self)
        self.db = connector.connect(host = host, user = user, password = password, database = database)
        self.q = data_queue
        self.alive = False

    def run(self):
        self.alive = True
        print("starting database writing object")
        while self.alive:
            try:
                data = self.q.get()
                print(data)
                self.write_values_to_database(data)
            except Exception:
                print(Exception)
        print("database writing object stopped")

    def stop(self):
        self.alive = False


    def retrieve_or_create_sensor_id(self, sensor_name):
        df = pd.read_sql(f"SELECT * FROM sensors", self.db)
        if len(df) == 0 or sensor_name not in df["name"].values:
            print(f"Creating new id for {sensor_name}")
            new_id = df["id"].max() + 1
            datecreated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            cursor = self.db.cursor()
            cursor.execute(f"INSERT INTO sensors VALUES ({new_id}, '{sensor_name}', '{datecreated}')")
            self.db.commit()
            cursor.close()
            return new_id
        else:
            return df["id"][df["name"]==sensor_name].values[0]



    def write_values_to_database(self, data):
        sensor_name, time_received, temperature, humidity = data
        # time_received = time_received.strftime("%Y-%m-%dT%H:%M:%S")
        sensor_id = self.retrieve_or_create_sensor_id(sensor_name)
        cursor = self.db.cursor()
        query = f"INSERT INTO measurements VALUES ('{sensor_id}', '{time_received}', '{temperature}', '{humidity}');"
        print(f"Executing query: {query}")
        cursor.execute(query)
        self.db.commit()
        print(f"\n Done \n")
        cursor.close()