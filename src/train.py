from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(
    data="dataset/data.yaml",
    epochs=100,
    imgsz=640,
    batch=8,
    device=0,
    workers=4,
    project="runs/detect",
    name="yolo11n_4classes_v2",
    patience=30,
    plots=True
)