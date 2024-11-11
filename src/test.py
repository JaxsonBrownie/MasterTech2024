import streamlit as st

# Inject custom CSS to create a red bar at the top of the app
st.markdown("""
    <style>
    .red-bar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 20px; /* Adjust the height as needed */
        background-color: red;
        z-index: 9999;
    }
    .main-content {
        padding-top: 20px; /* Adjust padding to prevent overlap */
    }
    </style>
    <div class="red-bar"></div>
    <div class="main-content">
""", unsafe_allow_html=True)

# Main content of your app
st.title("My Streamlit App")
st.write("This app has a red bar at the top.")

# Close the main content div
st.markdown("</div>", unsafe_allow_html=True)
