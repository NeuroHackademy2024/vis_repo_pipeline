# vis_repo_pipeline
A tool to visualize repository pipelines of script inputs and outputs

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor': '#C8E6C9', 'primaryTextColor': '#000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'tertiaryColor': '#fff' }}}%%
graph TD
classDef lightGreen fill:#C8E6C9,stroke:#333,stroke-width:2px;
classDef lightBlue fill:#BBDEFB,stroke:#333,stroke-width:2px;
classDef lightPurple fill:#E1BEE7,stroke:#333,stroke-width:2px;

subgraph Legend
    key1[Input Node]:::lightGreen
    key2[Script Node]:::lightBlue
    key3[Output Node]:::lightPurple
end
a_script(("a_script"))
test --> a_script:::lightBlue
a_script --> test1:::lightPurple
last_script(("last_script"))
test1 --> last_script:::lightBlue
 test2 --> last_script:::lightBlue
last_script --> test2:::lightPurple
last_script -->  test3:::lightPurple
another_script(("another_script"))
test3 --> another_script:::lightBlue
 test4 --> another_script:::lightBlue
another_script --> test5:::lightPurple
```
