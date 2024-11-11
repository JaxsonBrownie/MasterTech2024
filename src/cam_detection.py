import os
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
from IPython.display import display, Image
import matplotlib.pyplot as plt
import streamlit as st
import torch
from streamlit.runtime.scriptrunner import RerunException, StopException
from sku_manager import SKU_Manager

db = SKU_Manager()

def get_cordinates(box, scale_factor = 100): 
    x1, y1, x2, y2 = box.astype(int)
    width = (x2 - x1) /scale_factor
    height = (y2 - y1)/scale_factor

    bottom_left = (0.0, 0.0)
    top_right = (width, height)
    return bottom_left, top_right

# function to mark bottom left of bounding box as (0,0) and  then find the coordinate of the top right corner via number of pixels 
def add_box_coordinates(frame, boxes, scale_factor=100):
    # coordinate_data = []
    coordinate_data = []
    for box in boxes:
        x1, y1, x2, y2 = box.astype(int)

# store the coordinate data
        bottom_left, top_right = get_cordinates(box, scale_factor)
        coordinate_data.append({
            "bottom_left": bottom_left,
            "top_right": top_right,
            "pixel_coords": (x1, y1, x2, y2)
        })
        
        # calculate the  relative coordinates (using bottom left as origin)
        # width = (x2 - x1) / scale_factor
        # height = (y2 - y1) / scale_factor
        
        # Format coordinates 
        # bottom_left = "(0.0, 0.0)"
        # top_right = f"({width:.1f}, {height:.1f})"

        bottom_left_text = "(0.00, 0.00)"
        top_right_text = f"({top_right[0]:.2f}, {top_right[1]:.2f})"
        
        
        # bottom left coordinates just below box
        cv2.putText(frame, bottom_left_text,
                    (x1, y2 + 20),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 255, 0), 1)
        
        # top right cordinates just above
        cv2.putText(frame, top_right_text,
                    (x2 - 100, y1 - 10),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 255, 0), 1)
        
        # i think i can use the bottom_left and top_right variables and feed them to sku_manager for a specific product
        # but idk how to assign that specific coordinate for a specific aile/shelf/row location
    
    return frame, coordinate_data

#function for doing the cv with the camera integrated
def run_live_detection(weights_path, stframe):

    coordinate_data = []
    # check if jetson use gpu instead of cpu (answer: it does not)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")


    #use trained model(best weights stored in mastertech2024/weights folder)
    model = YOLO(weights_path)
    
    # open camera at index 0 (0 is default cam, so integrated webcam for laptops, but usb for jetson)
    cam = cv2.VideoCapture(0)

    latest_coordinate = None

    
    
    while True:
        try:
            #read and inference frame
            ret, frame = cam.read()
            
            if ret:
                #time.sleep(0.5)
                results = model(frame)[0]
                
                # Setup supervision for visualisation
                detections = sv.Detections.from_ultralytics(results)
                
                # Annotate image and corner cordinates
                box_annotator = sv.BoxAnnotator()
                annotated_frame = box_annotator.annotate(
                    scene=frame.copy(),
                    detections=detections,
                )

                # coordinate_data = None
                if len(detections) > 0:
                    annotated_frame, coordinate_data = add_box_coordinates(
                        annotated_frame, 
                        detections.xyxy,  # Gets boxes in xyxy format
                        scale_factor=100
                    )

                    latest_coordinate = []
                    for box in detections.xyxy:
                        x1, y1, x2, y2 = box.astype(int)

                        # store the coordinate data
                        bottom_left, top_right = get_cordinates(box, 100)
                        latest_coordinate.append((bottom_left, top_right))





                    
                else:
                    latest_coordinate = None
                
                #cv2.imshow('Shelf Detection', annotated_frame)
                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                stframe.image(annotated_frame, channels="RGB")
            
            # if coordinate_data:
            #     return coordinate_data
            
                # return latest_coordinate
                yield latest_coordinate
            
            # Press 'q' to exit the loop
                if cv2.waitKey(1) == ord('q'):
                    break
        except (RerunException, StopException):
            cam.release()
            # break
            break
    
    # release and close cam
    cam.release()
    cv2.destroyAllWindows()

def main():
    WEIGHTS_PATH = "../weights/shelf_detection_weights.pt"
    run_live_detection(WEIGHTS_PATH)

if __name__ == "__main__":
    main()