import os
import subprocess

def compile_arduino(sketch_code, sketch_name="esp_code", fqbn="esp8266:esp8266:nodemcuv2"):
    # Create folder structure
    sketch_dir = os.path.join(os.getcwd(), sketch_name)
    os.makedirs(sketch_dir, exist_ok=True)

    # Write sketch code to .ino file
    ino_path = os.path.join(sketch_dir, f"{sketch_name}.ino")
    with open(ino_path, "w") as f:
        f.write(sketch_code)

    # Compile using arduino-cli
    compile_cmd = [
        "./bin/arduino-cli",
        "compile",
        "--fqbn", fqbn,
        sketch_name
    ]

    try:
        result = subprocess.run(compile_cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
