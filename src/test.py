import streamlit as st

# Initialize session state to store tabs if it doesn't exist
if "tabs" not in st.session_state:
    st.session_state["tabs"] = ["Home"]  # Start with a default tab

# Add or remove tabs based on user input
st.sidebar.title("Tab Management")

# Input to add a new tab
new_tab_name = st.sidebar.text_input("New Tab Name")
if st.sidebar.button("Add Tab"):
    if new_tab_name and new_tab_name not in st.session_state["tabs"]:
        st.session_state["tabs"].append(new_tab_name)

# Select the tab to remove
tab_to_remove = st.sidebar.selectbox("Remove Tab", st.session_state["tabs"])
if st.sidebar.button("Remove Tab"):
    if tab_to_remove in st.session_state["tabs"]:
        st.session_state["tabs"].remove(tab_to_remove)

# Dynamic tab selection
tab_selection = st.selectbox("Select Tab", st.session_state["tabs"])

# Display content based on selected tab
if tab_selection == "Home":
    st.title("Home Page")
    st.write("Welcome to the Home Page!")
else:
    st.title(f"{tab_selection} Page")
    st.write(f"Content for {tab_selection}.")

# Display current tabs
st.sidebar.write("Current Tabs:", st.session_state["tabs"])
