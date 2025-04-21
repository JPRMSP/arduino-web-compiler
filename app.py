import streamlit as st
import os
import subprocess
import time

# Function to save Arduino code to a file
def save_code(user_code, folder="project"):
    os.makedirs(folder, exist_ok=True)
    ino_path = os.path.join(folder, f"{folder}.ino")
    with open(ino_path, "w") as f:
        f.write(user_code)
    return ino_path

# Function to compile code using Arduino CLI
def compile_code(ino_path, board="arduino:avr:uno"):
    folder = os.path.dirname(ino_path)
    result = subprocess.run(
        ["./bin/arduino-cli", "compile", "--fqbn", board, folder],
        capture_output=True, text=True
    )
    return result.stdout + result.stderr

# Streamlit UI
st.set_page_config(page_title="Arduino Web Compiler", page_icon="🛠️")

st.title("Arduino Web Compiler")
st.markdown("Write and compile Arduino code from your browser!")

# Default Arduino sketch
default_code = """\
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
"""

user_code = st.text_area("Enter your Arduino Code", value=default_code, height=300)

board = st.selectbox("Select Board", [
    "arduino:avr:uno",
    "esp8266:esp8266:nodemcuv2"
])

if st.button("Compile"):
    with st.spinner("Compiling..."):
        timestamp = str(int(time.time()))
        folder = f"sketch_{timestamp}"
        ino_path = save_code(user_code, folder=folder)
        result = compile_code(ino_path, board=board)
    st.success("Compilation finished!")
    st.text_area("Compiler Output", result, height=300)
