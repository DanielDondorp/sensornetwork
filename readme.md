## Sensornetwork

This is a project to monitor temperature and humidity in my house, monitor it with a live dashboard, and store the data for future analytics. It has a few moving parts:

### SQL database
MariaDB running on a raspberry pi stores the data.

### MQTT
The same raspberry pi runs the mosquitto mqtt broker that relays messages from all the sensors.

### Python listener
A python program set up as a daemon process listens on the /sensors/* topic and writes the incoming messages to the database. This listener decouples incoming and outgoing messages by using a Queue and a threaded architecture. If new sensors are deployed they are automatically added to the database with a new and unique sensor_id.

### Streamlit dashboard.
All that data is no fun if you can not see it live! There is a streamlit dashboard for live monitoring of sensors. Newly deployed sensors show up on the dashboard automagically.


#### to do:
- Add date selection controls in the dashboard.
- create a fancier readme with screenshots and examples.
- run the dashboard on a raspberry pi in kiosk mode as a daemon.
- create a small tutorial on how to set up this project.
