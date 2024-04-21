import threading
import subprocess
import time

# Define function to monitor readout
def execute_script():
    while True:
        subprocess.run(["python", "./SPELLMAN/SpellmanCTL_py3.py", "SendToDB"])
        time.sleep(2)

# Create a thread that will execute the script with the input parameters
script_thread = threading.Thread(target=execute_script)

# Start the thread
script_thread.start()