#define BLYNK_TEMPLATE_ID "YourTemplateID"
#define BLYNK_TEMPLATE_NAME "Water Level Monitor"
#define BLYNK_AUTH_TOKEN "YourAuthToken"

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

// Blynk credentials
char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "YourWiFiSSID";
char pass[] = "YourWiFiPassword";

// Ultrasonic sensor pins
#define TRIG_PIN D7
#define ECHO_PIN D8

// Tank height in cm (adjust as per your tank)
const int tankHeight = 100;

// Blynk virtual pin for water level
#define WATER_LEVEL_VPIN V0

void setup() {
  Serial.begin(115200);
  Blynk.begin(auth, ssid, pass);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  Blynk.run();
  sendWaterLevel();
  delay(2000); // Update every 2 seconds
}

void sendWaterLevel() {
  long duration;
  float distanceCM;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distanceCM = (duration * 0.0343) / 2;

  // Calculate water level
  float waterLevel = tankHeight - distanceCM;

  // Clamp the water level between 0 and tankHeight
  waterLevel = constrain(waterLevel, 0, tankHeight);

  Serial.print("Water Level: ");
  Serial.print(waterLevel);
  Serial.println(" cm");

  Blynk.virtualWrite(WATER_LEVEL_VPIN, waterLevel);
}
