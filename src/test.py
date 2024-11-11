import streamlit as st
import cv2
import threading
import time
from PIL import Image

# Shared variable for the latest frame
latest_frame = None
running = True  # Flag to control the camera thread

# Camera capture function to run in a separate thread
def capture_camera():
    global latest_frame, running
    cap = cv2.VideoCapture(0)  # Initialize camera

    while running:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to grab frame.")
            break
        
        # Convert frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Update the latest frame
        latest_frame = frame
        
        # Add a slight delay
        time.sleep(0.03)  # About 30 FPS

    cap.release()

# Start the camera thread
camera_thread = threading.Thread(target=capture_camera)
camera_thread.start()

st.title("Live Camera Feed")

# Display the camera feed
stframe = st.empty()

try:
    while running:
        if latest_frame is not None:
            stframe.image(latest_frame, channels="RGB")

        # Stop button to end the camera feed
        #if st.button("Stop"):
        #    running = False
        #    break

    # Wait for the camera thread to finish
    camera_thread.join()

except Exception as e:
    st.error(f"An error occurred: {e}")
finally:
    running = False












# import packages
import streamlit as st
import threading
import cv2
from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from time import sleep

# configure the page
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

# camera config
cap = cv2.VideoCapture(0)
latest_frame = None
running = True
stframe = None

# camera function to run in separate thread
def capture_camera():
    global latest_frame, running
    cap = cv2.VideoCapture(0)  # Initialize camera

    while running:
        _, frame = cap.read()
        
        # Convert frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        latest_frame = frame
        sleep(0.03)  # About 30 FPS

    cap.release()

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

            # start camera thread
            cam_thread = threading.Thread(target=capture_camera)
            cam_thread.start()





            #webrtc_streamer(
            #    key="streamer",
            #    sendback_audio=False,
            #    video_transformer_factory=VideoTransformer
            #)


        with info:
            st.markdown("Information")


    with scale_tab:
        st.header("Weight Scale")


def main():
    create_structure()
    display_tabs()

    # start the main loop
    while True:
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")



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



try:
    launch_task()
except (RerunException, StopException):
    cleanup_task()
    raise