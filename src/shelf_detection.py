# Install required packages
#!pip install ultralytics
#!pip install opencv-python-headless
#!pip install supervision

# Mount to Google Drive
# from google.colab import drive
# drive.mount('/content/drive/', force_remount=True)

import os
import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
from IPython.display import display, Image
import matplotlib.pyplot as plt

import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

def test_model_on_image(weights_path, image_path):
    """
    Test trained model on a single image and display results
    Parameters:
        weights_path: Path to your trained weights (.pt file)
        image_path: Path to test image
    """
    # Load the model with trained weights
    model = YOLO(weights_path)
    
    # Run inference on the image
    results = model(image_path)[0]
    
    # Load the image for visualization
    frame = cv2.imread(image_path)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    
    # Setup supervision for visualization
    # detections = sv.Detections.from_yolov8(results)
    detections = sv.Detections.from_ultralytics(results)
    
    # Create box annotator
    box_annotator = sv.BoxAnnotator()
    
    # Annotate image
    annotated_frame = box_annotator.annotate(
        scene=frame.copy(),
        detections=detections,
    #     labels=[f"{results.names[class_id]} {confidence:0.2f}"
    #             for class_id, confidence in zip(detections.class_id, detections.confidence)]
    )
    
    # Display the results
    plt.figure(figsize=(12, 8))
    plt.imshow(annotated_frame)
    plt.axis('off')
    plt.show()
    
    # Print detection results
    # Check if detection is a tuple and has class_id as attribute
        # Print detection results - Fixed version
    for i in range(len(detections.xyxy)):
        class_id = detections.class_id[i]
        confidence = detections.confidence[i]
        box = detections.xyxy[i]
        print(f"Detected {results.names[class_id]} with confidence: {confidence:.2f}")
        print(f"Bounding box: {box}")
        
def main():
    # Update these paths to match your Google Drive locations
    WEIGHTS_PATH = "../weights/shelf_detection_weights.pt"
    TEST_IMAGE_PATH = "../images/test_img_9.jpg"
    
    test_model_on_image(WEIGHTS_PATH, TEST_IMAGE_PATH)

if __name__ == "__main__":
    main()
