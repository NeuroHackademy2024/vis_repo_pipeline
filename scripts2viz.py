# main function that takes the path to a scripts directory as input and produces a visualization flowchat
# will have an option to save the flowchart as a .png file with specified output path
# also option to add the flowchart to README.md file if it exists via a README.md file path

# import os
# import json
# import base64

def scripts2viz(export_as_md = False, output_path=None, add_to_readme = False):
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

