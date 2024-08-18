import os
import time
import glob
import json
import numpy as np

from time import sleep
from itertools import cycle
from threading import Thread
from datetime import datetime
from shutil import get_terminal_size


class Loader:
    def __init__(self, desc="Loading...", end="Imaging software ready for use...", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

def generate_id():
    # Generate an ID based on the current date and time
    now = datetime.now()
    id_str = now.strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
    return id_str

def create_blank_json_file(filename):
    # Create a blank JSON file with the given filename
    with open("virtual_dropbox/observations/" + filename, 'w') as file:
        json.dump({'ID': filename.split(".")[0].split("_")[0]}, file) 
        # Dump an empty dictionary into the file

def main():

    # Step 0: Doug loads machine
    print("Mombot intiated.")
    # Step 1: Generate an ID
    file_id = generate_id()

    try:
        exp_ids = np.load("experiment_ids.npy", allow_pickle=True).item()
        exp_ids['current'].append(file_id)
        np.save("experiment_ids", exp_ids)
    except:
        np.save("experiment_ids", {'current': [file_id]})

    with Loader("Loading biobot imaging..."):
        for i in range(5):
            sleep(0.25)

    loader = Loader(f"Experiment {file_id} commencing...", "0th observation complete!", 0.05).start()
    for i in range(20):
        sleep(0.25)
    loader.stop()

    # Step 2: Create a blank JSON file with the generated ID
    filename = f"{file_id}_0.json"
    create_blank_json_file(filename)
    
    print(f"Observation saved: {filename}")

if __name__ == "__main__":
    main()
