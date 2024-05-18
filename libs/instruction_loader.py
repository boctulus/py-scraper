# instruction_loader.py

import os
import json
from glob import glob

class InstructionLoader:
    """
    # Uso de la clase

    loader    = InstructionLoader()
    test_file = 'pablotol.json'  # o 'pablotol.py' dependiendo del archivo
    
    instructions = loader.load_instructions(test_file)
    if instructions is None:
        print("Failed to load instructions.")
    else:
        print(instructions)
    """
    def load_instructions_from_python(self, test_file):
        instructions = {}
        test_file_path = os.path.join('instructions', test_file)
        
        if not os.path.isfile(test_file_path):
            print(f"Error: File '{test_file}' not found.")
            return

        with open(test_file_path, 'r') as f:
            exec(f.read(), instructions)
            
        return instructions 

    def load_instructions_from_json(self, json_file):
        json_file_path = os.path.join('instructions', json_file)
        
        if not os.path.isfile(json_file_path):
            print(f"Error: File '{json_file}' not found.")
            return

        try:
            with open(json_file_path, 'r') as f:
                data = f.read()
                if not data:
                    print(f"Error: File '{json_file}' is empty.")
                    return
                instructions = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file '{json_file}': {e}")
            return
        except Exception as e:
            print(f"Unexpected error reading file '{json_file}': {e}")
            return
        
        return instructions

    def load_instructions(self, file_name):
        if file_name.endswith('.json'):
            return self.load_instructions_from_json(file_name)
        else:
            return self.load_instructions_from_python(file_name)

    def get_last_modified_file(self):
        list_of_files = glob(os.path.join('instructions', '*'))
        if not list_of_files:
            print("Error: No files found in 'instructions' directory.")
            return None
        latest_file = max(list_of_files, key=os.path.getmtime)
        return os.path.basename(latest_file)

