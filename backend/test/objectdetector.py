import cv2
from ultralytics import YOLO
import os
# Load pre-trained YOLOv5 model (YOLOv8 is latest from Ultralytics)
model = YOLO("yolov8n.pt")  # Small and fast; use yolov8m or yolov8l for better accuracy

import cv2
from ultralytics import YOLO
filePath=os.path.dirname(os.path.abspath(__file__))
# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Choose a larger model for better accuracy if needed

def detect_objects_with_boxes(image_path, show=True, save_path=None):
    """
    Detects objects in an image, draws boxes and labels, and returns detections.
    
    :param image_path: Path to the input image.
    :param show: Whether to display the image with detections.
    :param save_path: Path to save the output image with boxes (optional).
    :return: List of tuples (label, (x1, y1, x2, y2))
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unreadable")

    results = model(img)[0]  # First item from the results list

    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls[0])
        label = model.names[class_id]
        confidence = float(box.conf[0])

        # Append detection
        detections.append((label, (x1, y1, x2, y2)))

        # Draw rectangle and label on the image
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f"{label} {confidence:.2f}"
        cv2.putText(img, text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show image with detections
    if show:
        cv2.imshow("Detected Objects", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Save output image if specified
    if save_path:
        cv2.imwrite(save_path, img)

    return detections

def detect_objects(image_path):
    """
    Detect objects in an image and return the list of object names.
    :param image_path: Path to the image file.
    :return: List of detected object names.
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unreadable")

    # Run detection
    results = model(img)

    # Extract object names
    detected_objects = set()
    boxes=set()
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            detected_objects.add(class_name)
            boxes.add(box)
    # Print detected objects and their bounding boxes

    return list(detected_objects)
def getHouseObjects(houseNum):
    """
    Get objects detected in a specific house image.
    :param houseNum: House number to identify the image.
    :return: List of detected object names and their bounding boxes.
    """
    image_path = filePath+"/images/house{0}/".format(houseNum)  # Adjust path as needed
    paths=os.listdir(image_path)
    list=[]
    for path in paths:
        print("Running image analysis Path:{0}".format(path))
        if path.endswith(".webp") or path.endswith(".jpg") or path.endswith(".png"):
            #image_path = os.path.join(image_path, path)
            path=image_path + path
            objects = detect_objects(path)
            for ob in objects:
                list.append(ob)
    
    
    # For simplicity, we return the objects without bounding boxes
    return list

# Example usage
if __name__ == "__main__":
    image_file = "./backend/test/images/house1/test.webp"  # Replace with your image path
    #objects,boxes = detect_objects(image_file)
    objects=getHouseObjects(1)
    for ob in objects:
        print("Objects:{0}".format(ob)) 
    #print("Detected objects:", ", ".join(objects))