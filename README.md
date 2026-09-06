# Experiment I: Object Detection and Recognition

This repository contains my implementation for the object detection experiment. The project mainly uses **YOLO11, NVIDIA Jetson, and ROS 2** to perform real-time detection of desktop objects.

The experiment mainly evaluates three object categories:

- `book`
- `keyboard`
- `laptop`

After the program starts, it can display bounding boxes, class labels, confidence scores, and FPS in real time. The detection results are also published through ROS 2. In addition, correct detection results and representative error cases can be saved during testing.

---

## 1. Project Files

The main project files are organized as follows:

```text
yolo_demo/
├── src/
│   └── detect.py
│   └── train.py
├── weights/
│   └── best.pt
├── results/
│   ├── success/
│   └── error_cases/
├── run_jetson.sh
└── README.md
```

Main files:

- `train.py`: trains the YOLO11n model
- `src/detect.py`: performs real-time detection on Jetson and publishes ROS 2 results
- `weights/best.pt`: trained model used for inference
- `run_jetson.sh`: starts the Jetson detection program
- `results/success/`: stores correct detection results
- `results/error_cases/`: stores representative error cases

---

## 2. Model Training

The model used in this experiment is YOLO11n. The main training parameters are:

```text
epochs = 100
imgsz = 640
batch = 8
device = 0
workers = 4
patience = 30
```

Run the following command in the project directory on the PC:

```bash
python train.py
```

After training, place the final model at:

```text
weights/best.pt
```

---

## 3. Running on Jetson

The project path on Jetson is:

```text
/home/nvidia/yolo_demo
```

Enter the project directory:

```bash
cd /home/nvidia/yolo_demo
```

Start the program:

```bash
bash run_jetson.sh
```

If the `.sh` file is not used, the program can also be started directly:

```bash
source /opt/ros/humble/setup.bash
python3 src/detect.py
```

After the program starts, the camera window displays:

- Object class
- Bounding box
- Confidence score
- FPS

---

## 4. Saving Detection Results

During runtime, click the detection window first so that it receives keyboard input.

Use the following keys:

```text
S: save a correct detection result
E: save an error case
Q: quit the program
```

Correct detection results are saved to:

```text
/home/nvidia/yolo_demo/results/success/
```

Error cases are saved to:

```text
/home/nvidia/yolo_demo/results/error_cases/
```

---

## 5. Viewing ROS 2 Results

While the detection program is running, open another terminal on Jetson.

First, load the ROS 2 environment:

```bash
source /opt/ros/humble/setup.bash
```

Check the available topics:

```bash
ros2 topic list
```

The detection results are published to:

```text
/detected_objects
```

View the real-time ROS 2 output:

```bash
ros2 topic echo /detected_objects
```

Example output:

```text
data: 'class=book, confidence=0.84, bbox=[78,119,583,644]'
---
```

The message fields mean:

```text
class       object category
confidence  detection confidence
bbox        bounding box coordinates
```

---

## 6. Experiment Verification

I mainly followed the steps below during the final verification.

### 1) Start the Detection Program

```bash
cd /home/nvidia/yolo_demo
bash run_jetson.sh
```

### 2) Test Multi-Object Detection

Place two different object categories in front of the camera at the same time, for example:

```text
keyboard + laptop
```

Check whether both categories can be detected simultaneously.

### 3) Check FPS

The program displays FPS in the detection window.

Requirement:

```text
FPS >= 5
```

During my test, the detection speed was around:

```text
8.9 FPS
```

### 4) Check ROS 2 Output

Open another terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /detected_objects
```

Check whether the class, confidence score, and bounding box coordinates are published correctly.

### 5) Save Results

```text
S: save a correct result
E: save an error case
```

### 6) Perform 20 Detection Tests

A total of 20 detection tests were recorded, with 19 correct detections:

```text
19 / 20 = 95%
```

This satisfies the experiment requirement:

```text
Accuracy >= 80%
```

---

## 7. Problems Encountered During Deployment

During Jetson deployment, I first tried to connect my PC to the Jetson through SSH, but the connection was not stable. Later, I switched to a direct data-cable connection, which allowed me to complete file transfer and testing successfully.

I also spent quite a lot of time configuring the Python and Conda environment. The main difficulty was making sure that PyTorch, Ultralytics, OpenCV, and ROS 2 could all work correctly in the same environment. After the environment was configured successfully, model loading and real-time detection worked much more smoothly.

---

## 8. Submission Files

The main submission files for this experiment are:

```text
dataset
best.pt
train.py
detect.py
run_jetson.sh
detection results
result video
README.md
experiment report
```
