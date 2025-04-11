from ultralytics import YOLO
import os

# Load a model
model = YOLO(r"runs\train\wang\best.pt")  # pretrained YOLOv8n model
test_root=r"D:\project\scsx\datasets\windows_v1.8.1\images\test"
# Run batched inference on a list of images
results = model([test_root+"/"+i for i in os.listdir(test_root)])  # return a list of Results objects

# Process results list
for i,result in enumerate(results):
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    # result.save(filename=f"result_{i}.jpg")  # save to disk
