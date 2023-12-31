import os

import streamlit as st
from jupyter_notebook_parser import JupyterNotebookParser

import utils

utils.setup_page("Jupyter Notebook Viewer", icon="🤖")

file = st.selectbox("Chose the file", os.listdir("media/Notebooks"), index=None)

if file is not None:
    parsed = JupyterNotebookParser("media/Notebooks/" + file)

    cells = parsed.get_all_cells()
    # st.write(cells)
    markdown = parsed.get_markdown_cell_sources()
    code = parsed.get_code_cell_sources()
    markdown_indexes = parsed.get_markdown_cell_indices()
    code_indexes = parsed.get_code_cell_indices()

    curr_md_idx = 0
    curr_src_idx = 0
    namespace = {}

    def display_code(idx, overall_idx, run_code_experimental=False):
        # with st.echo():
        st.code(code[idx].raw_source)
        if run_code_experimental:
            exec_code = code[idx].raw_source
            # handle print statements
            exec_code = exec_code.replace("print(", "st.write(")
            # Execute the code in the specified namespace
            try:
                exec(exec_code, namespace)
            except Exception as e:
                st.error(f"Error executing code: {e}")
            # handle magic (i.e. not explicitely saying print, but since it is at the end, printing)
            try:
                print("dshfj")
                st.write(exec("print(" + exec_code.split("\n")[-1] + ")"))
            except:
                print("lol failed for idx:", idx)
                print("print(" + exec_code.split("\n")[-1] + ")")
                pass
        else:
            # check for outputs
            for output in cells[overall_idx]["outputs"]:
                # st.write(output)
                with st.expander("View output"):
                    if output["output_type"] == "stream":
                        st.markdown("```\n" + "\n".join(output["text"]) + "\n```")
                    elif output["output_type"] == "execute_result":
                        st.markdown(
                            "```\n" + "\n".join(output["data"]["text/plain"]) + "\n```"
                        )
                    else:
                        st.markdown(output)

    def display_markdown(idx):
        markdown[idx]

    markdown = parsed.get_markdown_cell_sources()
    code = parsed.get_code_cell_sources()
    markdown_indexes = parsed.get_markdown_cell_indices()
    code_indexes = parsed.get_code_cell_indices()

    curr_md_idx = 0
    curr_src_idx = 0
    namespace = {}
    exec("import streamlit as st", namespace)

    for i in range(len(cells)):
        if i in markdown_indexes:
            display_markdown(curr_md_idx)
            curr_md_idx += 1
        else:
            display_code(curr_src_idx, i)
            curr_src_idx += 1
