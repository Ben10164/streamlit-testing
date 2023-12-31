import streamlit as st


def setup_page(name: str, parent="Home", icon="💡"):
    config(name, icon)
    if name != "Home":
        switch_page_button(parent, "Go Home")


def config(name: str, icon: str):
    st.set_page_config(
        page_title=name,
        page_icon=icon,
        initial_sidebar_state="collapsed",
    )
    st.title(name)


def switch_page_button(page_name: str, button_text=None):
    """
    Switch page programmatically in a multipage app

    Args:
        page_name (str): Target page name
    """
    if button_text == None:
        button_text = page_name

    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    button = st.button(label=button_text)

    if button:
        page_name = standardize_name(page_name)

        pages = get_pages("streamlit_app.py")  # OR whatever your main page is called

        for page_hash, config in pages.items():
            if standardize_name(config["page_name"]) == page_name:
                raise RerunException(
                    RerunData(
                        page_script_hash=page_hash,
                        page_name=page_name,
                    )
                )

        page_names = [
            standardize_name(config["page_name"]) for config in pages.values()
        ]

        raise ValueError(
            f"Could not find page {page_name}. Must be one of {page_names}"
        )
