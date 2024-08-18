import os
import sys
import json

import numpy as np

from time import sleep
from itertools import cycle
from threading import Thread
from shutil import get_terminal_size

class Loader:
    def __init__(self, desc="Loading...", end="Launching Mombot", timeout=0.1):
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

def load_json_file(filename):
    """Load and return the content of the given JSON file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file {filename} does not exist.")
    with open(filename, 'r') as file:
        return json.load(file)

def create_blank_json_file(filename):
    # Create a blank JSON file with the given filename
    with open("virtual_dropbox/observations/" + filename, 'w') as file:
        json.dump({'ID': filename.split(".")[0].split("_")[0]}, file)
        # Dump an empty dictionary into the file

def main(exp, iteration):

    exp_ids = np.load("experiment_ids.npy", allow_pickle=True).item()
    ID = exp_ids['current'][exp]

    input_filename = f"virtual_dropbox/interventions/{ID}_{iteration}.json"

    with Loader(f"Loading biobot {ID} intervention number {iteration}..."):
        for i in range(5):
            sleep(0.25)

    try:
        # Step 1: Load the JSON file
        json_data = load_json_file(input_filename)

        # Assume the JSON file contains an ID field
        if 'ID' not in json_data:
            raise KeyError("The JSON file does not contain an 'ID' field.")

        # Extract the ID
        file_id = json_data['ID']

        loader = Loader(f"Applying intervention {iteration} to biobot {ID}...", 
                        "Intervention complete. Exporting observation.", 0.05).start()
        for i in range(20):
            sleep(0.25)
        loader.stop()

        # Step 2: Create a new JSON file containing dummy "obseration"

        obs_filename = f"{file_id}_{iteration+1}.json"
        create_blank_json_file(obs_filename)

        print(f"Observation number {iteration+1} for biobot {ID} captured: {obs_filename}")

    except (FileNotFoundError, KeyError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    exp = int(sys.argv[1])
    iteration = int(sys.argv[2])
    main(exp, iteration)
