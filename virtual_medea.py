import os
import sys
import json

import numpy as np

def load_json_file(filename):
    """Load and return the content of the given JSON file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file {filename} does not exist.")
    with open(filename, 'r') as file:
        return json.load(file)

def create_blank_json_file(filename):
    # Create a blank JSON file with the given filename
    with open("virtual_dropbox/interventions/" + filename, 'w') as file:
        json.dump({'ID': filename.split(".")[0].split("_")[0]}, file)
        # Dump an empty dictionary into the file

def main(exp, iteration):

    # Input filename
    #input_filename = input("Enter the name of the JSON file to load: ")
    exp_ids = np.load("experiment_ids.npy", allow_pickle=True).item()
    ID = exp_ids['current'][exp]
    input_filename = f"virtual_dropbox/observations/{ID}_{iteration}.json"
    print("Launching Medea")

    try:
        # Step 1: Load the JSON file
        json_data = load_json_file(input_filename)
        
        # Assume the JSON file contains an ID field
        if 'ID' not in json_data:
            raise KeyError("The JSON file does not contain an 'ID' field.")
        
        # Extract the ID
        file_id = json_data['ID']
        # Step 2: Create a new JSON file containing dummy "intervention"
        
        intervention_filename = f"{file_id}_{iteration}.json"
        create_blank_json_file(intervention_filename)
        
        print(f"Intervention number {iteration} for biobot {ID} proposed: {intervention_filename}")
    
    except (FileNotFoundError, KeyError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    exp = int(sys.argv[1])
    iteration = int(sys.argv[2])
    main(exp, iteration)
