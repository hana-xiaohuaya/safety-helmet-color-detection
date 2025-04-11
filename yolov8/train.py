# #fire 
# from ultralytics import YOLO

# # Load a model
# model = YOLO(r"ultralytics\cfg\models\v8\yolov8n_fire.yaml")  # build a new model from scratch
# # model = YOLO("weights/yolov8n.pt")  # load a pretrained model 不使用预训练权重，就注释这一行即可
# # train
# model.train(data=r'ultralytics\cfg\datasets\fire.yaml',
#                 cache=False,
#                 imgsz=640,
#                 epochs=5,
#                 batch=16,
#                 close_mosaic=0,
#                 workers=0,
#                 device='0',
#                 optimizer='SGD', # using SGD
#                 amp=False, # close amp
#                 project='runs/train',
#                 name='fire',
#                 )


# safety_helmet
from ultralytics import YOLO

# Load a model
model = YOLO(r"ultralytics/cfg/models/v8/yolov8_safety_helmet.yaml")  # build a new model from scratch
# model = YOLO("weights/yolov8n.pt")  # load a pretrained model 不使用预训练权重，就注释这一行即可
# train
model.train(data=r'ultralytics\cfg\datasets\safety_helmet.yaml',
                cache=False,
                imgsz=640,
                epochs=20,
                batch=16,
                close_mosaic=0,
                workers=0,
                device='0',
                optimizer='SGD', # using SGD
                amp=False, # close amp
                project='runs/train',
                name='safety_helmet',
                )