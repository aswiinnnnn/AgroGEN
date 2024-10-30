import streamlit as st
from streamlit_option_menu import option_menu
import chatbot
import disease
import community
import recommentation  # Import the recommentation module

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",  # required
        options=["Chatbot", "Disease Recognition", "Farmers Community", "Recommentation"],  # added "Recommentation"
        icons=["robot", "tree", "people", "lightbulb"],  # added an icon for "Recommentation"
        menu_icon="cast",  # optional
        default_index=0,  # optional
        styles={
            "container": {"padding": "0!important", "background-color": "#262730"},
            "icon": {"color": "white", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "grey"},
            "nav-link-selected": {"background-color": "#02ab21"},
        },
    )

# Run the appropriate app based on the selected menu option
if selected == "Chatbot":
    chatbot.chatbot()
if selected == "Disease Recognition":
    disease.disease()
if selected == "Farmers Community":
    community.community()
if selected == "Recommentation":
    recommentation.recommendation()
  # Call the recommentation function
