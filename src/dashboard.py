# import packages
import streamlit as st
import cv2
# from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from time import sleep
from streamlit.runtime.scriptrunner import RerunException, StopException
from cam_detection import run_live_detection
import cam_detection
from sku_manager import SKU_Manager
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# global variables
stframe = None
db = SKU_Manager("data/sku_manager.json")

def generate_sku(aisle: int, shelf: int, row: int) -> str:
    """Generate SKU based on location (e.g., A01S02R03 for aisle 1, shelf 2, row 3)"""
    return f"A{aisle:02d}S{shelf:02d}R{row:02d}"


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
        _, col, _ = st.columns([1,10,1])
        with col:
            st.image("images/logo.svg", width=500)
        
        st.write('')
        st.write('')
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

        c_icon1, c_text1, c_status1, _, c_icon2, c_text2, c_status2 = st.columns([1,3,3,3,1,3,3], vertical_alignment="center")
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
            st.markdown("## Shelf Location")
            st.markdown("#### Aisle: 3")
            st.markdown("#### Shelf: 7")
    
    # sensor info
    with sensors:
        with st.container(height=320):
            st.markdown("## Available Sensors")

            image_sensor = ("images/camera_logo.svg", "Camera", "Active")
            weight_sensor = ("images/scale_logo.svg", "Weight", "Active")
            display_sensor_row(image_sensor, weight_sensor)
            humidity_sensor = ("images/water_logo.svg", "Humidity", "Active")
            temp_sensor = ("images/temp_logo.svg", "Temperature", "Inactive")
            display_sensor_row(humidity_sensor, temp_sensor)
            light_sensor = ("images/light_logo.svg", "Light", "Inactive")
            display_sensor_row(light_sensor, None)

# setup tabs for the sensors (not used anymore)
def display_tabs():
    global stframe

    with st.container(height=800):
        # create tabs for the different inputs
        camera_tab, scale_tab, humidity_tab, temp_tab, light_tab = st.tabs(["Video Camera", "Weight Scale", "Humidity", "Temperature", "Light"])

        with camera_tab:
            st.header("Camera Feed")
            #here
            st.markdown("## Product Information")

            cam, info = st.columns(2)

            with cam:
                st.markdown("#### Shelf Gap Detection")
                stframe = st.image([])
    
            with info:
                st.markdown("#### Information")

        ############################################
        with scale_tab:
            weight, info = st.columns(2)

            with weight:
                st.markdown("#### Scale Value")
            with info:
                st.markdown("#### Information")

            _, weight, _, info = st.columns([1,3,1,6])
            with weight:
                st.text("")
                st.text("")
                st.text("")
                st.markdown("<h1>Weight: 17.14" + "kg</h1>", unsafe_allow_html=True)
                st.image("images/scale.svg", width=500)
            
            _, but, _ = st.columns([2,3,5])
            with but:
                st.button("Tare", type="primary")

        ############################################
        with humidity_tab:
            humid, info = st.columns(2)
            
            with humid:
                st.markdown("#### Humidity Recording")
            with info:
                st.markdown("#### Information")
                
            _, humid, _= st.columns([1,3,7])
            with humid:
                st.text("")
                st.text("")
                st.text("")
                st.markdown("<h1>Humidity: 30%</h1>", unsafe_allow_html=True)
            _, humid, _= st.columns([2,2,10])
            with humid:
                st.image("images/water_drops.svg", width=200)

        ############################################
        with temp_tab:
            st.header("Temperature")

        ############################################
        with light_tab:
            st.header("Lighting")

# setup columns for the sensors
def display_columns():
    global stframe

    camera_col, env_col = st.columns([3, 2], gap='medium')

    with camera_col:
        st.markdown("# Camera Feed")

        # gap detection
        with st.container(border=True):
            st.markdown("#### Shelf Gap Detection")
            stframe = st.image([])
        st.markdown("#### Information")

    with env_col:
        st.markdown("# Environment Sensors")

        # weight
        with st.container(border=True):
            col1, col2 = st.columns([1,4])
            with col1:
                st.image("images/weight.svg", width=70)
            with col2:
                st.markdown("## Weight: 17.14kg", unsafe_allow_html=True)

        # humidity
        with st.container(border=True):
            col1, col2 = st.columns([1,4])
            with col1:
                st.image("images/water_drops.svg", width=70)
            with col2:
                st.markdown("## Humidity: 30%", unsafe_allow_html=True)

        # temperature
        with st.container(border=True):
            col1, col2 = st.columns([1,4])
            with col1:
                st.image("images/temp_logo.svg", width=70)
            with col2:
                st.markdown("## Temperature: 24°C", unsafe_allow_html=True)

        # lighting
        with st.container(border=True):
            col1, col2 = st.columns([1,4])
            with col1:
                st.image("images/light_logo.svg", width=70)
            with col2:
                st.markdown("## Lighting: On", unsafe_allow_html=True)

alerted_skus = set()

# main function 
def main():
    global stframe

    # render everything
    configure()
    create_structure()
    display_sensors()
    #display_tabs()
    display_columns()

    # start camera
    cam = cv2.VideoCapture(0)

    # start main loop
    try:
        
        aisle=5
        shelf=9
        row=4
        current_sku = generate_sku(aisle, shelf, row)
        st.text(f"Current SKU: {current_sku}")
        
        status_placeholder = st.empty()
        alert_placeholder = st.empty()

        # get coordinate generator (this starts a loop, but for some reason doesn't block???)
        coordinate_generator = run_live_detection("../weights/shelf_detection_weights.pt", stframe, cam)
        
        # start looping thread
        while True:
            coordinate_data = next(coordinate_generator)
            
            if coordinate_data and len(coordinate_data) > 0:
                # coordinate_data[0] is now a tuple of (bottom_left, top_right)
                bottom_left, top_right = coordinate_data[0]

                if current_sku not in alerted_skus:
                    alert_placeholder.error(f"Empty or Low product detected! - SKU: {current_sku} at Aisle {aisle}, Shelf {shelf}, Row {row}")
                    alerted_skus.add(current_sku)
                
                # Create product if it doesn't exist
                if not db.get_product_by_sku(current_sku):
                    db.add_product(
                        sku=current_sku,
                        name=f"Product at A{aisle}S{shelf}R{row}",
                        aisle_number=aisle,
                        shelf_number=shelf,
                        row_number=row,
                        bottom_left_coord=bottom_left,
                        top_right_coord=top_right
                    )
                else:
                    # Update existing product
                    db.update_product_coordinates(
                        current_sku,
                        bottom_left,
                        top_right
                    )
                
                # status_placeholder.text(f"Updated coordinates for {current_sku}\nCoordinates: BL{bottom_left}, TR{top_right}")
                
                # Small delay to prevent overwhelming the system
                #sleep(1)
    except (RerunException, StopException):
        cam.release()


if __name__ == '__main__':
    main()