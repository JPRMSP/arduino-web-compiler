import streamlit as st
from compile_arduino import compile_arduino

st.set_page_config(page_title="Arduino Compiler", layout="centered")
st.title("Arduino Compiler (ESP8266)")

# Text area to paste Arduino code
default_code = """\
#define BLYNK_TEMPLATE_ID "YourTemplateID"
#define BLYNK_TEMPLATE_NAME "Water Level Monitor"
#define BLYNK_AUTH_TOKEN "YourAuthToken"

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "YourWiFiSSID";
char pass[] = "YourWiFiPassword";

#define TRIG_PIN D7
#define ECHO_PIN D8
const int tankHeight = 100;
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
  delay(2000);
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
  float waterLevel = tankHeight - distanceCM;
  if (waterLevel < 0) waterLevel = 0;
  if (waterLevel > tankHeight) waterLevel = tankHeight;

  Serial.print("Water Level: ");
  Serial.print(waterLevel);
  Serial.println(" cm");
  Blynk.virtualWrite(WATER_LEVEL_VPIN, waterLevel);
}
"""

st.subheader("Paste your Arduino code:")
user_code = st.text_area("Arduino Sketch (.ino)", value=default_code, height=400)

if st.button("Compile"):
    with st.spinner("Compiling your sketch..."):
        success, result = compile_arduino(user_code)
        if success:
            st.success("Compilation successful!")
            st.code(result, language="bash")
        else:
            st.error("Compilation failed.")
            st.code(result, language="bash")

st.markdown("---")
st.caption("Made with Streamlit and Arduino CLI")
