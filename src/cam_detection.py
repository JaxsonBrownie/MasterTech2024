import os
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
from IPython.display import display, Image
import matplotlib.pyplot as plt
import torch

# function to mark bottom left of bounding box as (0,0) and then find the coordinate of the top right corner via number of pixels 
def add_corner_coordinates(frame, scale_factor=100):
    height, width = frame.shape[:2]
    
    # calc coordinates after scaling (e.g. 640 pixels and 100 scale = 640/100 = 6.40)
    top_right = f"({width/scale_factor:.1f}, {height/scale_factor:.1f})"
    bottom_left = "(0.0, 0.0)"
    
    # Top right corner
    cv2.putText(frame, top_right, 
                (width - 150, 30), 
                cv2.FONT_HERSHEY_DUPLEX, 
                0.7, (0, 255, 0), 2)
    
    # Bottom left corner
    cv2.putText(frame, bottom_left, 
                (10, height - 10), 
                cv2.FONT_HERSHEY_DUPLEX, 
                0.7, (0, 255, 0), 2)
    
    return frame

#function for doing the cv with the camera integrated
def run_live_detection(weights_path):

    # force jetson to use gpu instead of cpu 
    device = "cuda" if torch.cuda.is_available() else "cpu"

    #use trained model(best weights stored in mastertech2024/weights folder)
    model = YOLO(weights_path)
    
    # open camera at index 0 (0 is default cam, so integrated webcam for laptops, but usb for jetson)
    cam = cv2.VideoCapture(0)
    
    while True:
        
        #read and inference frame
        ret, frame = cam.read()
        results = model(frame)[0]
        
        # Setup supervision for visualisation
        detections = sv.Detections.from_ultralytics(results)
        
        # Annotate image and corner cordinates
        box_annotator = sv.BoxAnnotator()
        annotated_frame = box_annotator.annotate(
            scene=frame.copy(),
            detections=detections,
        )
        annotated_frame = add_corner_coordinates(annotated_frame)
        
        cv2.imshow('Shelf Detection', annotated_frame)
        
        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break
    
    # release and close cam
    cam.release()
    cv2.destroyAllWindows()

def main():
    WEIGHTS_PATH = "../weights/shelf_detection_weights.pt"
    run_live_detection(WEIGHTS_PATH)

if __name__ == "__main__":
    main()