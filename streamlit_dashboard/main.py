import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from mysql import connector
import time
import os
import dotenv

dotenv.load_dotenv()
SQL_HOST = os.getenv("SQL_HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")



st.set_page_config("sensornetwork", layout = "wide")

st.write("## SensorNetwork Dashboard")

container = st.empty()
container1 = st.empty()
container2 = st.empty()

db = connector.connect(host=SQL_HOST, user=USERNAME, password=PASSWORD, database=DATABASE)
sensors = pd.read_sql("SELECT * FROM sensors;", db)

def load_data(n_hours):
    df = pd.read_sql(f"SELECT s.name, m.measured_at, m.temperature, m.humidity "
                     f"FROM measurements m "
                     f"JOIN sensors s "
                     f"ON s.id = m.sensor_id "
                     f"WHERE m.measured_at >= NOW() - INTERVAL {n_hours} HOUR;", db)
    db.commit()
    return df

n_hours = st.number_input(label = "Show data for hours:", min_value = 1, max_value =7*24, value = 24)
while True:

    with container.container():
        st.write(time.strftime("%H:%M"))


    data = load_data(n_hours)
    with container1.container():
        columns = st.columns(len(sensors))
        for col, s in zip(columns, sensors.name.values):
            try:
                for m in ["temperature", "humidity"]:
                    vals = data[m][data["name"] == s].values
                    now = vals[-1]
                    delta = now - vals[-2]
                    delta = round(delta, 2)
                    if m == "temperature":
                        suffix = "°C"
                    else:
                        suffix = "%"
                    col.metric(s, str(now)+suffix, delta)


            except:
                col.metric(s, 0, 0)

    with container2.container():
        fig_cols = st.columns([1,1])
        with fig_cols[0]:
            fig = px.line(data, x = "measured_at", y = "temperature", color = "name", title = f"Temperature last {n_hours}h")
            st.write(fig)
        with fig_cols[1]:
            fig = px.line(data, x = "measured_at", y = "humidity", color = "name", title = f"Humidity last {n_hours}h")
            st.write(fig)

    time.sleep(10)

