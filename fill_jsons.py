# loop through all json files in the vis directory
# for each one, prompt the user to fill in the input and output fields
# save the filled json file in the vis directory

import os
import json

def fill_jsons():
    """
    Fill in the input and output fields of each JSON file in the vis directory.
    """
    try:
        # Change the current directory to the directory of this script
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Get a list of all the JSON files in the directory
        json_files = [f for f in os.listdir('vis') if f.endswith('.json')]
        
        # Loop through all JSON files in the vis directory
        for json_file in json_files:
            with open('vis/' + json_file, 'r') as f:
                json_obj = json.load(f)
            
            # Prompt the user to fill in the input and output fields using the input() function
            print(f"Fill in the input and output fields for {json_file}:")
            json_obj['input'] = input("Input: ").split(',')
            json_obj['output'] = input("Output: ").split(',')
            
            # Save the filled JSON file in the vis directory
            with open('vis/' + json_file, 'w') as f:
                json.dump(json_obj, f)
    except Exception as e:
        print(f"Error filling JSON files: {e}")

# Call the fill_jsons function

fill_jsons()
