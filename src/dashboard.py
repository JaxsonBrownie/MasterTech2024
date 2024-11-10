# import packages
import streamlit as st
#from streamlit_navigation_bar import st_navbar

# configure the page
def set_page_config():
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

# setup the page structure
def create_structure():
    st.title("Smart Shelves Dashboard")

    # create sidebar
    with st.sidebar:
        st.markdown("## Example Sidebar")

# setup tabs for the sensor
def display_tabs():
    # create tabs for the different inputs
    camera_tab, scale_tab = st.tabs(["Camera", "Scale"])

    with camera_tab:
        st.header("Camera Feed and Shelf Gap Detection")
        cam, info = st.columns(2)

        with cam:
            st.header("HAAA")
        with info:
            st.header("info")


    with scale_tab:
        st.header("Weight Scale")

def main():
    set_page_config()
    create_structure()
    display_tabs()

if __name__ == '__main__':
    main()



#tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

#with tab1:
#    st.header("A cat")
#    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
#with tab2:
#    st.header("A dog")
#    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
#with tab3:
#    st.header("An owl")
#    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)