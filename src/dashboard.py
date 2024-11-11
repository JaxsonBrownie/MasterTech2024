# import packages
import streamlit as st
import cv2
# from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from time import sleep
from streamlit.runtime.scriptrunner import RerunException, StopException
from cam_detection import run_live_detection

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
    st.title("Smart Shelves Dashboard")

    # create sidebar
    with st.sidebar:
        st.markdown("## Example Sidebar")


# setup tabs for the sensor
def display_tabs():
    global stframe

    # create tabs for the different inputs
    camera_tab, scale_tab = st.tabs(["Camera", "Scale"])

    with camera_tab:
        st.header("Camera Feed")
        cam, info = st.columns(2)

        with cam:
            st.markdown("#### Shelf Gap Detection")
            stframe = st.image([])

        with info:
            st.markdown("#### Information")


    with scale_tab:
        st.header("Weight Scale")


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
            run_live_detection("../weights/shelf_detection_weights.pt", stframe)
        except (RerunException, StopException):
            cap.release()


if __name__ == '__main__':
    main()