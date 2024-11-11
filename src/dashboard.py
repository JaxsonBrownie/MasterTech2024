# import packages
import streamlit as st
import cv2
# from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from time import sleep
from streamlit.runtime.scriptrunner import RerunException, StopException
from cam_detection import run_live_detection
from sku_manager import SKU_Manager
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

db = SKU_Manager("data/sku_manager.json")

def generate_sku(aisle: int, shelf: int, row: int) -> str:
    """Generate SKU based on location (e.g., A01S02R03 for aisle 1, shelf 2, row 3)"""
    return f"A{aisle:02d}S{shelf:02d}R{row:02d}"


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
        #here
        st.markdown("## Product Information")
        
        # Location inputs
        col1, col2, col3 = st.columns(3)
        with col1:
            aisle = st.number_input("Aisle Number", min_value=1, max_value=99, value=1)
        with col2:
            shelf = st.number_input("Shelf Number", min_value=1, max_value=10, value=1)
        with col3:
            row = st.number_input("Row Number", min_value=1, max_value=5, value=1)
        
        current_sku = generate_sku(aisle, shelf, row)
        st.text(f"Current SKU: {current_sku}")
        
        status_placeholder = st.empty()
        #

        cam, info = st.columns(2)

        with cam:
            st.markdown("#### Shelf Gap Detection")
            stframe = st.image([])

            try:
                # Get coordinate generator
                coordinate_generator = run_live_detection("../weights/shelf_detection_weights.pt", stframe)
                
                while True:
                    coordinate_data = next(coordinate_generator)
                    
                    if coordinate_data and len(coordinate_data) > 0:
                        # coordinate_data[0] is now a tuple of (bottom_left, top_right)
                        bottom_left, top_right = coordinate_data[0]
                        
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
                        
                        status_placeholder.text(f"Updated coordinates for {current_sku}\nCoordinates: BL{bottom_left}, TR{top_right}")
                        
                        # Small delay to prevent overwhelming the system
                        sleep(1)
                            
            except StopIteration:
                pass

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