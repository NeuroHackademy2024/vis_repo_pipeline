import os
import json
import base64
from IPython.display import Image, display

# Function to create JSON files for each script in the scripts directory
def create_json_files(script_dir, vis_dir):
    if not os.path.exists(script_dir):
        raise FileNotFoundError(f"Error: '{script_dir}' directory not found.")
    
    if not os.path.exists(vis_dir):
        os.makedirs(vis_dir)

    for filename in os.listdir(script_dir):
        if filename.endswith(('.py', '.R', '.sh', '.mat')):
            script_path = os.path.join(script_dir, filename)
            with open(script_path, 'r') as f:
                script = f.read()
            
            json_obj = {'input': [], 'output': []}
            json_file_path = os.path.join(vis_dir, os.path.splitext(filename)[0] + '.json')
            with open(json_file_path, 'w') as f:
                json.dump(json_obj, f)

# Function to fill in the input and output fields of each JSON file in the vis directory
def fill_json_files(vis_dir):
    try:
        json_files = [f for f in os.listdir(vis_dir) if f.endswith('.json')]
        
        for json_file in json_files:
            with open(os.path.join(vis_dir, json_file), 'r') as f:
                json_obj = json.load(f)
            
            print(f"Fill in the input and output fields for {json_file}:")
            json_obj['input'] = input("Input: ").split(',')
            json_obj['output'] = input("Output: ").split(',')
            
            with open(os.path.join(vis_dir, json_file), 'w') as f:
                json.dump(json_obj, f)
    except Exception as e:
        print(f"Error filling JSON files: {e}")

# Function to initialize a Mermaid diagram with a custom theme and legend
def initialize_mermaid_diagram():
    return [
        " %%{init: {'theme':'base', 'themeVariables': {",
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

# Function to add a script's inputs and outputs to the Mermaid diagram
def add_script_to_diagram(script, script_name, node_connections, mermaid_diagram, icon=True):
    script_input = script['input'] if isinstance(script['input'], list) else [script['input']]
    script_output = script['output'] if isinstance(script['output'], list) else [script['output']]
    
    try:
        mermaid_diagram.append(f"{script_name}((\"{script_name}\")):::lightGreen")
        if icon:
            mermaid_diagram.append(f"{script_name}((\"{script_name}\n fa:fa-code\"))")

        for input_item in script_input:
            if input_item not in node_connections:
                node_connections[input_item] = {'inputs': 0, 'outputs': 0}
            node_connections[input_item]['inputs'] += 1
            mermaid_diagram.append(f"{input_item} --> {script_name}")

        for output_item in script_output:
            if output_item not in node_connections:
                node_connections[output_item] = {'inputs': 0, 'outputs': 0}
            node_connections[output_item]['outputs'] += 1
            mermaid_diagram.append(f"{script_name} --> {output_item}")  
    except Exception as e:
        print(f"Error creating input/output nodes or connections: {e}")

# Function to display the Mermaid graph
def display_mermaid_graph(graph):
    graph_bytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graph_bytes)
    base64_string = base64_bytes.decode("ascii")
    mermaid_url = "https://mermaid.ink/img/" + base64_string
    display(Image(url=mermaid_url))

# Function to create and optionally save the visualization
def create_viz(vis_dir, root_dir, export_as_md, output_path, add_to_readme):
    json_files = [f for f in os.listdir(vis_dir) if f.endswith('.json')]
    mermaid_diagram = initialize_mermaid_diagram()
    node_connections = {}

    for json_file in json_files:
        script_name = os.path.splitext(json_file)[0]
        with open(os.path.join(vis_dir, json_file), 'r') as f:
            script = json.load(f)
            add_script_to_diagram(script, script_name, node_connections, mermaid_diagram)

    for node, connections in node_connections.items():
        if connections['inputs'] > 0 and connections['outputs'] > 0:
            mermaid_diagram.append(f"{node}:::lightPurple")
        elif connections['inputs'] > 0:
            mermaid_diagram.append(f"{node}:::lightRed")
        elif connections['outputs'] > 0:
            mermaid_diagram.append(f"{node}:::lightBlue")

    mermaid_diagram_str = "\n".join(mermaid_diagram)

    with open(os.path.join(root_dir, 'flowchart.mmd'), 'w') as f:
        f.write(mermaid_diagram_str)

    print("Mermaid diagram saved to 'flowchart.mmd'")

    if output_path is None:
        output_path = './'

    if export_as_md:
        try:
            with open(f'{output_path}flowchart.md', 'w') as f:
                f.write("```mermaid\n")
                f.write(mermaid_diagram_str)
                f.write("\n```")
            print(f"Mermaid diagram saved to '{output_path}flowchart.md'")
        except Exception as e:
            print(f"Error saving Mermaid diagram as .md file: {e}")

    if add_to_readme:
        try:
            with open('README.md', 'r') as f:
                readme_lines = f.readlines()

            mermaid_exists = any("```mermaid" in line for line in readme_lines)

            if mermaid_exists:
                start_index, end_index = None, None
                for i, line in enumerate(readme_lines):
                    if line.strip() == "```mermaid":
                        start_index = i
                    elif start_index is not None and line.strip() == "```":
                        end_index = i
                        break

                if start_index is not None and end_index is not None:
                    readme_lines = readme_lines[:start_index] + ["```mermaid\n"] + [mermaid_diagram_str + "\n"] + ["```\n"] + readme_lines[end_index+1:]

                with open('README.md', 'w') as f:
                    f.writelines(readme_lines)
            else:
                with open('README.md', 'a') as f:
                    f.write("\n```mermaid\n")
                    f.write(mermaid_diagram_str + "\n")
                    f.write("```\n")
        except Exception as e:
            print(f"Error updating README.md: {e}")

    display_mermaid_graph(mermaid_diagram_str)

# Main function to create a visualization flowchart from scripts in a directory
def scripts2viz(script_dir='scripts', vis_dir='vis', export_as_md=True, output_path=None, add_to_readme=True):
    root_dir = os.getcwd()
    create_json_files(script_dir, vis_dir)
    fill_json_files(vis_dir)
    create_viz(vis_dir, root_dir, export_as_md, output_path, add_to_readme)
