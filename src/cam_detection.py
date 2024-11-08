import os
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
from IPython.display import display, Image
import matplotlib.pyplot as plt

def run_live_detection(weights_path):
    """
    Run live shelf detection using the webcam and display the results.
    Parameters:
        weights_path: Path to the trained YOLOv8 weights.
    """
    # Load the trained model
    model = YOLO(weights_path)

    # Open the default camera
    cam = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cam.read()

        # Run inference on the frame
        results = model(frame)[0]

        # Setup supervision for visualization
        # detections = sv.Detections.from_yolov8(results)
        detections = sv.Detections.from_ultralytics(results)

        # Create box annotator
        box_annotator = sv.BoxAnnotator()

        # Annotate the frame
        annotated_frame = box_annotator.annotate(
            scene=frame.copy(),
            detections=detections,
            labels=[f"{results.names[class_id]} {confidence:0.2f}"
                    for class_id, confidence in zip(detections.class_id, detections.confidence)]
        )

        # Display the annotated frame
        cv2.imshow('Shelf Detection', annotated_frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the camera and close all windows
    cam.release()
    cv2.destroyAllWindows()

def main():
    WEIGHTS_PATH = "../weights/shelf_detection_weights.pt"

    run_live_detection(WEIGHTS_PATH)

if __name__ == "__main__":
    main()