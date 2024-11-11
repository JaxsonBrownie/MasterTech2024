# import packages
import streamlit as st
import cv2
# from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from time import sleep
from streamlit.runtime.scriptrunner import RerunException, StopException
import cam_detection

# configure the page
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

# camera config
#cap = cv2.VideoCapture(0)
stframe = None

# setup the page structure
def create_structure():
    
    img, title = st.columns([1,18], vertical_alignment='bottom')

    with img:
        st.image("images/shelf.svg", width=55)
    with title:
        st.title("Smart Shelves Dashboard")

    # create sidebar
    with st.sidebar:
        st.image("images/logo.svg", width=200)
        st.markdown("## Example Sidebar")


    # Remove whitespace from the top of the page and sidebar
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 3rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)


# setup tabs for the sensor
def display_tabs():
    global stframe

    st.divider()
    loc, sensors, _ = st.columns([3, 3, 3])
    
    # location info
    with loc:
        with st.container(border=True, height=200):
            st.markdown("### Shelf Location")
            st.markdown("**Aisle: <num>**")
            st.markdown("**Shelf: <num>**")
    # sensor info
    with sensors:
        with st.container(border=True, height=200):
            st.markdown("### Available Sensors")

            box, text, _ = st.columns([1,4,10], vertical_alignment="center")
            with box:
                st.image("images/checkbox-checked.svg", width=20)
            with text:
                st.markdown("**Camera**")

            
            box, text, _ = st.columns([1,4,10], vertical_alignment="center")
            with box:
                st.image("images/checkbox-checked.svg", width=20)
            with text:
                st.markdown("**Scale**")



    # create tabs for the different inputs
    #st.header("Sensors")
    camera_tab, scale_tab, humidity_tab, temp_tab, light_tab = st.tabs(["Video Camera", "Weight Scale", "Humidity", "Temperature", "Light"])

    ############################################
    with camera_tab:
        #st.header("Camera Feed")
        cam, info = st.columns(2)

        with cam:
            st.markdown("#### Shelf Gap Detection")
            stframe = st.image([])

        with info:
            st.markdown("#### Information")

    ############################################
    with scale_tab:
        st.header("Weight Scale")

    ############################################
    with humidity_tab:
        st.header("Humidity")

    ############################################
    with temp_tab:
        st.header("Temperature")

    ############################################
    with light_tab:
        st.header("Lighting")

# main function 
def main():
    global stframe, cap

    # render everything
    create_structure()
    display_tabs()

    # start main loop
    while True:
        try:
            #_, frame = cap.read()
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #stframe.image(frame, channels="RGB")
            cam_detection.run_live_detection("../weights/shelf_detection_weights.pt", stframe)
        except (RerunException, StopException):
            cap.release()


if __name__ == '__main__':
    main()