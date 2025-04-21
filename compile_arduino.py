import os
import subprocess

def compile_arduino(code_str):
    # Define directory where Arduino sketch will be written
    sketch_dir = "sketch"
    os.makedirs(sketch_dir, exist_ok=True)

    # Path for the Arduino sketch
    sketch_path = os.path.join(sketch_dir, "sketch.ino")

    # Write the code to the .ino file
    with open(sketch_path, "w") as f:
        f.write(code_str)

    # Define the path to arduino-cli (make sure it's installed and accessible)
    arduino_cli_path = "./bin/arduino-cli"  # Update this if necessary

    # Define the command for compiling the sketch
    compile_cmd = [
        arduino_cli_path,
        "compile",
        "--fqbn",
        "arduino:avr:uno",  # Target board, change if needed
        sketch_dir
    ]

    try:
        # Run the compile command and capture output
        result = subprocess.run(
            compile_cmd, capture_output=True, text=True, check=True
        )
        # Return success and the result output
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        # Return failure and error output
        return False, e.stderr
