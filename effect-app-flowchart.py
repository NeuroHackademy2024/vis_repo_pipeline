import os
import json
import base64
from IPython.display import Image, display

def display_mermaid_graph(graph):
    """
    Display a Mermaid.js graph in a Jupyter notebook.
    
    Parameters                   
    __________
    graph: str, Mermaid.js graph definition
    """
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    mermaid_url = "https://mermaid.ink/img/" + base64_string
    display(Image(url=mermaid_url))

    
    #######

# Directory where JSON files are located
json_dir = 'vis'

# get a list of all the JSON files in the directory
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

# Initialize a Mermaid diagram
mermaid_diagram = ["graph TD"]

def add_script_to_diagram(script, script_name):
    """
    Add a script's inputs and outputs to the Mermaid diagram.
    
    Parameters:
    - script (dict): A dictionary containing the script details with keys 'input' and 'output'.
    - script_name (str): The name of the script.
    """
 
    def process_io(input_list, output_list):
        """
        Create connections in the Mermaid diagram for each pair of input and output items.
        
        Parameters:
        - input_list (list): List of input items.
        - output_list (list): List of output items.
        """

        # loop through each input in input_list and turn it into a string with the format "input & input & input"
        input_list = " & ".join(input_list)
        for output_item in output_list:
            # Append connection information to the diagram
            mermaid_diagram.append(f"{input_list} -->|{script_name}| {output_item}")

    # Ensure input and output are treated as lists
    script_input = script['input'] if isinstance(script['input'], list) else [script['input']]
    script_output = script['output'] if isinstance(script['output'], list) else [script['output']]

    # Process input and output
    process_io(script_input, script_output)

# Read each JSON file and add to the diagram
for json_file in json_files:
    # Construct the full file path
    file_path = os.path.join(json_dir, json_file)
    # Extract the script name without the .json extension
    script_name = os.path.splitext(json_file)[0]
    with open(file_path, 'r') as f:
        # Load the script from the JSON file
        script = json.load(f)
        # Add the script to the Mermaid diagram
        add_script_to_diagram(script, script_name)

# Combine all lines of the Mermaid diagram into a single string
mermaid_diagram_str = "\n".join(mermaid_diagram)

# Save the diagram to a file with the '.mmd' extension
with open('flowchart.mmd', 'w') as f:
    f.write(mermaid_diagram_str)

print("Mermaid diagram saved to 'flowchart.mmd'")

# Function to display the mermaid graph (assuming this function is already defined in your environment)
display_mermaid_graph(mermaid_diagram_str)

# TODO: treat scripts as nodes as well, and then try to fix the two nodes using one script to make output
