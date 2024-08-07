# a function that loops through all scripts in the scripts directory, and for each one creates a matching .json file in the vis directory

# save the current path as a variable
import os
import json

# change the current directory to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# if vis directory does not exist in this github repo, create it
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
        # write the json object to a file
        with open('vis/' + filename[:-4] + '.json', 'w') as f:
            json.dump(json_obj, f)

