# vis_repo_pipeline
A tool to visualize repository pipelines of script inputs and outputs

```mermaid
 %%{init: {'theme':'base', 'themeVariables': {
  'primaryColor': '#ffcaca',
  'primaryTextColor': '#000',
  'primaryBorderColor': '#000000',
  'lineColor': '#000000',
  'tertiaryColor': '#fff'
}}}%%
graph LR
classDef lightRed fill:#ffcaca,stroke:#333,stroke-width:2px;
classDef lightGreen fill:#ebfcda,stroke:#333,stroke-width:2px;
classDef lightBlue fill:#cefbfb,stroke:#333,stroke-width:2px;
classDef lightPurple fill:#f8aaf8,stroke:#333,stroke-width:2px;

subgraph Legend
    key1[<b>Input]:::lightRed
    key2[<b>Function]:::lightGreen
    key3[<b>Output]:::lightBlue
    key4[<b>Intermediate</b><br> Both an input and output]:::lightPurple
end
extract_functions(("extract_functions")):::lightGreen
extract_functions(("extract_functions
 fa:fa-code"))
script_path:::lightRed
script_path --> extract_functions
functions:::lightBlue
extract_functions --> functions
initialize_mermaid_diagram(("initialize_mermaid_diagram")):::lightGreen
initialize_mermaid_diagram(("initialize_mermaid_diagram
 fa:fa-code"))
top_down:::lightRed
top_down --> initialize_mermaid_diagram
initialize:::lightBlue
initialize_mermaid_diagram --> initialize
add_function_to_diagram(("add_function_to_diagram")):::lightGreen
add_function_to_diagram(("add_function_to_diagram
 fa:fa-code"))
func:::lightRed
func --> add_function_to_diagram
node_connections:::lightRed
node_connections --> add_function_to_diagram
mermaid_diagram:::lightRed
mermaid_diagram --> add_function_to_diagram
icon:::lightRed
icon --> add_function_to_diagram
create_viz_from_script(("create_viz_from_script")):::lightGreen
create_viz_from_script(("create_viz_from_script
 fa:fa-code"))
script_path --> create_viz_from_script
top_down --> create_viz_from_script
export_as_md:::lightRed
export_as_md --> create_viz_from_script
output_path:::lightRed
output_path --> create_viz_from_script
add_to_readme:::lightRed
add_to_readme --> create_viz_from_script
script_to_viz(("script_to_viz")):::lightGreen
script_to_viz(("script_to_viz
 fa:fa-code"))
script_path --> script_to_viz
export_as_md --> script_to_viz
output_path --> script_to_viz
add_to_readme --> script_to_viz
top_down --> script_to_viz
script_path:::lightRed
functions:::lightBlue
top_down:::lightRed
initialize:::lightBlue
func:::lightRed
node_connections:::lightRed
mermaid_diagram:::lightRed
icon:::lightRed
export_as_md:::lightRed
output_path:::lightRed
add_to_readme:::lightRed
```
