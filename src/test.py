import streamlit as st
import cv2
from PIL import Image

# Load the image using OpenCV
image = cv2.imread("images/test_img_9.jpg")  # Replace with the path to your image

# Check if image loaded successfully
if image is not None:
    # Define text and position
    text = "Hello, Streamlit!"
    position = (50, 50)  # (x, y) coordinates for the text position
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 5
    color = (255, 255, 255)  # White color in BGR
    thickness = 2

    # Put text on the image
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

    # Convert the image to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Display the image in Streamlit
    st.image(image_rgb, caption="Image with Text Overlay")
else:
    st.error("Error loading image. Please check the file path.")
