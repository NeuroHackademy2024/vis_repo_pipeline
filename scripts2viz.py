# main function that takes the path to a scripts directory as input and produces a visualization flowchat
# will have an option to save the flowchart as a .png file with specified output path
# also option to add the flowchart to README.md file if it exists via a README.md file path

# a function that loops through all scripts in the scripts directory, and for each one creates a matching .json file in the vis directory

# save the current path as a variable
import os
import json
import base64
from IPython.display import Image, display

def create_jsons():
    # check if the scripts directory exists in the current directory

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

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



def fill_jsons():
    """
    Fill in the input and output fields of each JSON file in the vis directory.
    """
    try:
        # Change the current directory to the directory of this script
        
        
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




def create_viz(export_as_md, output_path, add_to_readme):

    def initialize_mermaid_diagram():
        """
        Initialize a Mermaid diagram with a custom theme and legend.

        Returns
        -------
        list of str
            A list of strings representing the Mermaid diagram definition.
        """
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
        
    def add_script_to_diagram(script, script_name, node_connections):
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

    # Get a list of all the JSON files in the directory
    json_files = [f for f in os.listdir('vis') if f.endswith('.json')]   

    # Initialize a Mermaid diagram with a custom theme
    mermaid_diagram = initialize_mermaid_diagram()

    # Option to have icons in diagram 
    icon = True 

    # Dictionary
    node_connections = {}

    # Read each JSON file and add to the diagram
    for json_file in json_files:
        file_path = os.path.join('vis', json_file)
        script_name = os.path.splitext(json_file)[0]
        with open(file_path, 'r') as f:
            script = json.load(f)
            add_script_to_diagram(script, script_name, node_connections)

    # Update node colors based on their connections
    for node, connections in node_connections.items():
        if connections['inputs'] > 0 and connections['outputs'] > 0:
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

    if output_path is None:
        output_path = './'

    # if export_as_md = True, create a .md file with the Mermaid diagram
    if export_as_md:
        try:
            # Save the diagram as a .md file
            with open(f'{output_path}flowchart.md', 'w') as f:
                # first line should be "```mermaid"
                f.write("```mermaid\n")
                f.write(mermaid_diagram_str)
                # go down a line
                f.write("\n")
                # last line should be "```"
                f.write("```")
            print(f"Mermaid diagram saved to '{output_path}flowchart.md'")
        except Exception as e:
            print(f"Error saving Mermaid diagram as .md file: {e}")

    # if add_to_readme = True, add the Mermaid diagram to the README.md file
    # if there is already a mermaid diagram in the README.md file, replace it
    if add_to_readme:
        # Read the contents of the README.md file
        with open('README.md', 'r') as f:
            readme_lines = f.readlines()

        # check if there is already a mermaid diagram in the README.md file
        mermaid_exists = False
        for line in readme_lines:
            if "```mermaid\n" in line:
                mermaid_exists = True
                break

        # if there is a mermaid diagram in the README.md file, replace it
        if mermaid_exists:
            # Initialize variables to find the start and end indices
            start_index = None
            end_index = None

            # Identify the start and end of the existing mermaid diagram
            for i, line in enumerate(readme_lines):
                if line.strip() == "```mermaid":
                    start_index = i
                elif start_index is not None and line.strip() == "```":
                    end_index = i
                    break

            if start_index is not None and end_index is not None:
                # Replace the existing mermaid diagram
                readme_lines = readme_lines[:start_index] + ["```mermaid\n"] + [mermaid_diagram_str + "\n"] + ["```\n"] + readme_lines[end_index+1:]

            # write the updated README.md file
            with open('README.md', 'w') as f:
                f.writelines(readme_lines)
        else:
            # Add a new mermaid diagram at the end if none exists
            readme_lines.append("\n```mermaid\n")
            readme_lines.append(mermaid_diagram_str + "\n")
            readme_lines.append("```\n")

            # write the updated README.md file
            with open('README.md', 'w') as f:
                f.writelines(readme_lines)

        # try:
        #     with open('README.md', 'r') as f:
        #         readme_lines = f.readlines()

        #     # Initialize variables to find the start and end indices
        #     start_index = None
        #     end_index = None

        #     # Identify the start and end of the existing mermaid diagram
        #     for i, line in enumerate(readme_lines):
        #         if line.strip() == "```mermaid":
        #             start_index = i
        #         elif start_index is not None and line.strip() == "```":
        #             end_index = i
        #             break

        #     if start_index is not None and end_index is not None:
        #         # Replace the existing mermaid diagram
        #         readme_lines = readme_lines[:start_index] + ["```mermaid\n"] + [mermaid_diagram_str + "\n"] + ["```\n"] + readme_lines[end_index+1:]
        #     else:
        #         # Add a new mermaid diagram at the end if none exists
        #         readme_lines.append("\n```mermaid\n")
        #         readme_lines.append(mermaid_diagram_str + "\n")
        #         readme_lines.append("```\n")

        #     with open('README.md', 'w') as f:
        #         f.writelines(readme_lines)

        #     print("Mermaid diagram added/replaced in README.md")
        # except Exception as e:
        #     print(f"Error adding Mermaid diagram to README.md: {e}")


    # Display the Mermaid graph
    return display_mermaid_graph(mermaid_diagram_str)



def scripts2viz(export_as_md = True, output_path=None, add_to_readme = True):
    """
    Create a visualization flowchart from scripts in a directory.
    
    Parameters
    ----------
    base_dir: str
        Path to the base directory containing a "scripts/" directory.
    output_path: str, optional
        Path to save the flowchart as a .png file.
    readme_path: str, optional
        Path to the README.md file to add the flowchart.
    """
    
    create_jsons()

    fill_jsons()

    create_viz(export_as_md, output_path, add_to_readme)
