from ultralytics import YOLO
model = YOLO('models/model_1/weights/best.pt')
print('类别名 names:', model.names)
