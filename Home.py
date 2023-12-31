import streamlit

import utils

utils.setup_page("Home")


import os

for file in os.listdir("pages"):
    utils.switch_page_button(file[:-3])  # trim off .py
