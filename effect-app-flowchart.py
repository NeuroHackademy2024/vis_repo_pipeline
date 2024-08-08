import os
import json
import base64
from IPython.display import Image, display

def initialize_mermaid_diagram():
    """
    Initialize a Mermaid diagram with a custom theme and legend.

    Returns
    -------
    list of str
        A list of strings representing the Mermaid diagram definition.
    """
    return [
        "%%{init: {'theme':'base', 'themeVariables': {",
        "  'primaryColor': '#ffcaca',",
        "  'primaryTextColor': '#000',",
        "  'primaryBorderColor': '#000000',",
        "  'lineColor': '#000000',",
        "  'tertiaryColor': '#fff'",
        "}}}%%",
        "graph TD",
        "classDef lightRed fill:#ffcaca,stroke:#333,stroke-width:2px;",
        "classDef lightGreen fill:#ebfcda,stroke:#333,stroke-width:2px;",
        "classDef lightBlue fill:#cefbfb,stroke:#333,stroke-width:2px;",
        "classDef lightPurple fill:#f8aaf8,stroke:#333,stroke-width:2px;",
        "",
        "subgraph Legend",
        "    key1[<b>Input]:::lightRed",
        "    key2[<b>Script]:::lightGreen",
        "    key3[<b>Output]:::lightBlue",
        "    key4[<b>Intermediate</b><br> Both an input and output]:::lightPurple",
        "end"
    ]    
    
def add_script_to_diagram(script, script_name):
    """
    Add a script's inputs and outputs to the Mermaid diagram.
    
    Parameters
    ----------
    script: dict
      A dictionary containing the script details with keys 'input' and 'output'.
    script_name: str
        The name of the script, used to create the script node in the diagram.
    """
    def create_input_output_node(input_list, output_list):
        """
        Create connections in the Mermaid diagram for each pair of input and output items from script.
        
        Parameters
        ----------
        input_list: list
            List of input items.
        output_list: list
            List of output items.
        mermaid_diagram: list of str
            The Mermaid diagram definition to which nodes and connections will be added.
        """
   
        # Add the script node to the diagram
        try:
            mermaid_diagram.append(f"{script_name}((\"{script_name}\")):::lightGreen")
         
            if icon:
                mermaid_diagram.append(f"{script_name}((\"{script_name}\n fa:fa-code\"))")

            # Handle inputs
            for input_item in input_list:
                if input_item not in node_connections:
                    node_connections[input_item] = {'inputs': 0, 'outputs': 0}
                node_connections[input_item]['inputs'] += 1
                mermaid_diagram.append(f"{input_item} --> {script_name}")

            # Handle outputs
            for output_item in output_list:
                if output_item not in node_connections:
                    node_connections[output_item] = {'inputs': 0, 'outputs': 0}
                node_connections[output_item]['outputs'] += 1
                mermaid_diagram.append(f"{script_name} --> {output_item}")    
        except Exception as e:
            print(f"Error creating input/output nodes or connections: {e}")

    # Ensure input and output are treated as lists
    script_input = script['input'] if isinstance(script['input'], list) else [script['input']]
    script_output = script['output'] if isinstance(script['output'], list) else [script['output']]

    # Add nodes and connections for the script
    create_input_output_node(script_input, script_output)

def display_mermaid_graph(graph):
    """
    Create and display a Mermaid.js graph.
    
    Parameters                   
    ----------
    graph: str
        Mermaid.js graph definition
    """
    graph_bytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")
    mermaid_url = "https://mermaid.ink/img/" + base64_string
    display(Image(url=mermaid_url))

# Directory where JSON files are located
json_dir = 'vis'

# Get a list of all the JSON files in the directory
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]   

# Initialize a Mermaid diagram with a custom theme
mermaid_diagram = initialize_mermaid_diagram()

# Option to have icons in diagram 
include_icon = True 

# Dictionary
node_connections = {}

# Read each JSON file and add to the diagram
for json_file in json_files:
    file_path = os.path.join(json_dir, json_file)
    script_name = os.path.splitext(json_file)[0]
    with open(file_path, 'r') as f:
        script = json.load(f)
        add_script_to_diagram(script, script_name)
        
# Update node colors based on their connections
for node, connections in node_connections.items():
    if connections['inputs'] > 0 and connections['outputs'] > 0: # Checks if a node has both inputs and outputs (i.e., it's both a source and destination in the graph).
        mermaid_diagram.append(f"{node}:::lightPurple")
    elif connections['inputs'] > 0:
        mermaid_diagram.append(f"{node}:::lightRed")
    elif connections['outputs'] > 0:
        mermaid_diagram.append(f"{node}:::lightBlue")

# Combine all lines of the Mermaid diagram into a single string
mermaid_diagram_str = "\n".join(mermaid_diagram)

# Save the diagram to a file with the '.mmd' extension
with open('flowchart.mmd', 'w') as f:
    f.write(mermaid_diagram_str)

print("Mermaid diagram saved to 'flowchart.mmd'")

# Display the Mermaid graph
display_mermaid_graph(mermaid_diagram_str)

