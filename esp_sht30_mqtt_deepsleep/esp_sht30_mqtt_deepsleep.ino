#include <WEMOS_SHT3X.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>


const char* ssid = "ssid";
const char* password = "password";
const char* mqtt_server = "broker ip";

WiFiClient espClient;
PubSubClient client(espClient);
SHT3X sht30(0x45);


void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
    if (!client.connected()) {
    reconnect();
  }

  sht30.get();
  float temp = sht30.cTemp;
  float h = sht30.humidity; 

  char sensorvals[10];
  dtostrf(temp, 0,2,sensorvals);
  char hum[10];
  dtostrf(h, 0,2,hum);
  strcat(sensorvals, ",");
  strcat(sensorvals, hum);

  Serial.println("Publishing data:");
  Serial.println(sensorvals);
  client.publish("/sensors/bathroom",sensorvals);
//  delay(100);


  Serial.println("Going to sleep");
  delay(100);
  ESP.deepSleep(60*10e6);
}


void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      //client.publish("test", "hello there!");
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void loop() {
  // keep empty for deepsleep stuff

}
