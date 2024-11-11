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
import time

# function to mark bottom left of bounding box as (0,0) and then find the coordinate of the top right corner via number of pixels 
def add_box_coordinates(frame, boxes, scale_factor=100):
    for box in boxes:
        x1, y1, x2, y2 = box.astype(int)
        
        # calculate the  relative coordinates (using bottom left as origin)
        width = (x2 - x1) / scale_factor
        height = (y2 - y1) / scale_factor
        
        # Format coordinates 
        bottom_left = "(0.0, 0.0)"
        top_right = f"({width:.1f}, {height:.1f})"
        
        # Bottom left coordinates just below box
        cv2.putText(frame, bottom_left,
                    (x1, y2 + 20),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 255, 0), 1)
        
        # Top right cordinates just above
        cv2.putText(frame, top_right,
                    (x2 - 100, y1 - 10),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.5, (0, 255, 0), 1)
    
    return frame

#function for doing the cv with the camera integrated
def run_live_detection(weights_path, stframe):

    # check if jetson use gpu instead of cpu (answer: it does not)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")


    #use trained model(best weights stored in mastertech2024/weights folder)
    model = YOLO(weights_path)
    
    # open camera at index 0 (0 is default cam, so integrated webcam for laptops, but usb for jetson)
    cam = cv2.VideoCapture(0)
    
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
                if len(detections) > 0:
                    annotated_frame = add_box_coordinates(
                        annotated_frame, 
                        detections.xyxy,  # Gets boxes in xyxy format
                        scale_factor=100
                    )
                
                #cv2.imshow('Shelf Detection', annotated_frame)
                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                stframe.image(annotated_frame, channels="RGB")
            
        except (RerunException, StopException):
            cam.release()
    
    # release and close cam
    cam.release()
    cv2.destroyAllWindows()

def main():
    WEIGHTS_PATH = "../weights/shelf_detection_weights.pt"
    run_live_detection(WEIGHTS_PATH)

if __name__ == "__main__":
    main()