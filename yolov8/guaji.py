from ultralytics import YOLO
import os
import shutil

# Load a model
model = YOLO(r"runs\train\safety_helmet2\weights\best.pt")  # pretrained YOLOv8n model
test_root = r"D:\project\scsx\datasets\windows_v1.8.1\image\4"

# Create a directory to save label files
label_dir = "yolo_labels_unnormalized"
os.makedirs(label_dir, exist_ok=True)

# Run batched inference on a list of images
image_files = [os.path.join(test_root, f) for f in os.listdir(test_root)]
results = model(image_files)  # return a list of Results objects

failed_detections = []

# Process results list
for i, result in enumerate(results):
    boxes = result.boxes  # Boxes object for bounding box outputs
    
    # Get original image filename
    original_filename = os.path.basename(image_files[i])
    
    # Create and open a text file to write YOLO format labels
    txt_filename = os.path.splitext(original_filename)[0] + '.txt'
    
    if len(boxes) == 0:
        # No detections for this image
        failed_detections.append(image_files[i])
    else:
        with open(os.path.join(label_dir, txt_filename), 'w') as f:
            # For each detected object in this image
            for box in boxes:
                # Get class, and bounding box coordinates
                cls = int(box.cls)
                x, y, w, h = box.xywh[0]  # xywh are in pixel coordinates
                
                # Write to file in YOLO format (without normalization)
                f.write(f"{cls} {x} {y} {w} {h}\n")
    
    # Optionally, save the result image
    # result.save(filename=f"result_{i}.jpg")  # save to disk

print(f"YOLO format labels (unnormalized) saved in {label_dir} directory")

if failed_detections:
    print("\nThe following images had no detections:")
    for filename in failed_detections:
        print(os.path.basename(filename))
    
    # Ask for confirmation before deleting
    confirm = input("\nDo you want to delete these files? (y/n): ").lower()
    if confirm == 'y':
        for file in failed_detections:
            try:
                os.remove(file)
                print(f"Deleted: {os.path.basename(file)}")
            except Exception as e:
                print(f"Error deleting {os.path.basename(file)}: {e}")
        print("Deletion complete.")
    else:
        print("Deletion cancelled.")
else:
    print("\nAll images had at least one detection.")
























#     from ultralytics import YOLO
# import os
# import csv

# # Load a model
# model = YOLO(r"runs\train\safety_helmet2\weights\best.pt")  # pretrained YOLOv8n model
# test_root = r"D:\project\scsx\datasets\windows_v1.8.1\images\4"

# # Run batched inference on a list of images
# results = model([test_root+"/"+i for i in os.listdir(test_root)])  # return a list of Results objects

# # Prepare CSV file for saving results
# with open('detection_results.csv', 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(['Image', 'Class', 'Confidence', 'X1', 'Y1', 'X2', 'Y2'])

#     # Process results list
#     for i, result in enumerate(results):
#         boxes = result.boxes  # Boxes object for bounding box outputs
        
#         # Save the result image
#         result.save(filename=f"result_{i}.jpg")  # save to disk
        
#         # Get the original image filename
#         original_filename = os.listdir(test_root)[i]
        
#         # For each detected object in this image
#         for box in boxes:
#             # Get class, confidence and coordinates
#             cls = int(box.cls)
#             conf = float(box.conf)
#             x1, y1, x2, y2 = box.xyxy[0].tolist()
            
#             # Write to CSV
#             csvwriter.writerow([original_filename, cls, conf, x1, y1, x2, y2])

# print("Results saved to detection_results.csv")