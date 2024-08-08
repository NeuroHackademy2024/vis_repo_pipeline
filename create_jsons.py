# a function that loops through all scripts in the scripts directory, and for each one creates a matching .json file in the vis directory

# save the current path as a variable
import os
import json

def create_jsons():
    # check if the scripts directory exists in the current directory
    if not os.path.exists('scripts'):
        print('Error: scripts directory not found in current directory. Please navigate to parent directory of scripts directory and try again.')
    else :
        print('Scripts directory found')

    # if vis directory does not exist in current directory, create it
    if not os.path.exists('vis'):
        os.makedirs('vis')

    # loop through all scripts in the scripts directory
    for filename in os.listdir('scripts'):
        # if filename is a script name
        if filename.endswith('.py') or filename.endswith('.R') or filename.endswith('.sh') or filename.endswith('.mat'):
            # open the script file
            with open('scripts/' + filename, 'r') as f:
                script = f.read()
            # create a json object that contains input as an empty list and output as an empty list
            json_obj = {'input': [], 'output': []}
            # write the json object to a file with the filename as the script name without the extension
            with open('vis/' + os.path.splitext(filename)[0] + '.json', 'w') as f:
                json.dump(json_obj, f)

# Call the create_jsons function


