# import packages
import streamlit as st
import cv2
# from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from time import sleep
from streamlit.runtime.scriptrunner import RerunException, StopException
import cam_detection

# global variables
stframe = None

# configure the page
def configure():
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("""
        <style>
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
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
        st.markdown("## Global View")
        st.markdown("## Individual Shelf View")

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

# show a sensor
def display_sensor_row(sensor1, sensor2):
    with st.container(height=60, border=False):
        if sensor1 is not None: icon1, text1, status1 = sensor1 
        if sensor2 is not None: icon2, text2, status2 = sensor2 


        c_icon1, c_text1, c_status1, _, c_icon2, c_text2, c_status2 = st.columns([1,2,3,3,1,3,3], vertical_alignment="center")
        if sensor1 is not None:
            with c_icon1:
                st.image(icon1, width=35)
            with c_text1:
                st.markdown("**"+text1+"**")
            with c_status1:
                if status1 == "Active":
                    st.success(status1)
                else:
                    st.error(status1)

        if sensor2 is not None:
            with c_icon2:
                st.image(icon2, width=35)
            with c_text2:
                st.markdown("**"+text2+"**")
            with c_status2:
                if status2 == "Active":
                    st.success(status2)
                else:
                    st.error(status2)

# setup sensor info + location
def display_sensors():
    st.divider()
    loc, sensors, _ = st.columns([3, 7, 2])
    
    # location info
    with loc:
        with st.container(height=320):
            st.markdown("### Shelf Location")
            st.markdown("#### Aisle: 3")
            st.markdown("#### Shelf: 7")
    
    # sensor info
    with sensors:
        with st.container(height=320):
            st.markdown("### Available Sensors")

            image_sensor = ("images/camera_logo.svg", "Camera", "Active")
            weight_sensor = ("images/scale_logo.svg", "Weight", "Active")
            display_sensor_row(image_sensor, weight_sensor)
            humidity_sensor = ("images/water_logo.svg", "Humidity", "Active")
            temp_sensor = ("images/temp_logo.svg", "Temperature", "Inactive")
            display_sensor_row(humidity_sensor, temp_sensor)
            light_sensor = ("images/light_logo.svg", "Light", "Inactive")
            display_sensor_row(light_sensor, None)

# setup tabs for the sensors
def display_tabs():
    global stframe

    with st.container(height=600):
        # create tabs for the different inputs
        camera_tab, scale_tab, humidity_tab, temp_tab, light_tab = st.tabs(["Video Camera", "Weight Scale", "Humidity", "Temperature", "Light"])

        ############################################
        with camera_tab:
            cam, info = st.columns(2)

            with cam:
                st.markdown("#### Shelf Gap Detection")
                stframe = st.image([])

            with info:
                st.markdown("#### Information")

        ############################################
        with scale_tab:
            weight, options = st.columns(2)

            with weight:
                st.markdown("#### Scale Value")
            with options:
                st.markdown("#### Information")

            _, weight, _, options = st.columns([1,3,1,6])
            with weight:
                st.text("")
                st.text("")
                st.text("")
                st.markdown("<h1 style='text-align: center;'>Weight: 17.14" + "kg</h1>", unsafe_allow_html=True)
                st.image("images/scale.svg", width=500)
            
            _, but, _ = st.columns([2,3,5])
            with but:
                st.button("Tare", type="primary")

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
    configure()
    create_structure()
    display_sensors()
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