# 实验一：目标检测与识别

这是我这次目标检测实验的项目说明。项目主要使用 **YOLO11、Jetson 和 ROS 2**，完成桌面物体的实时检测。

这次实验主要测试了 3 类物体：

- `book`
- `keyboard`
- `laptop`

程序运行后可以显示检测框、类别、置信度和 FPS，同时会把检测结果通过 ROS 2 发布出去。也可以保存正确检测图片和错误案例。

---

## 1. 项目文件

项目主要文件如下：

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

各文件作用：

- `train.py`：训练 YOLO11n 模型
- `src/detect.py`：在 Jetson 上进行实时检测，同时发布 ROS 2 结果
- `weights/best.pt`：训练完成后使用的模型
- `run_jetson.sh`：启动 Jetson 检测程序
- `results/success/`：保存正常检测结果
- `results/error_cases/`：保存错误案例

---

## 2. 模型训练

训练使用的是 YOLO11n，主要参数如下：

```text
epochs = 100
imgsz = 640
batch = 8
device = 0
workers = 4
patience = 30
```

在电脑项目目录下运行：

```bash
python train.py
```

训练完成后，将最终使用的模型放到：

```text
weights/best.pt
```

---

## 3. Jetson 上运行

Jetson 中项目路径为：

```text
/home/nvidia/yolo_demo
```

进入项目目录：

```bash
cd /home/nvidia/yolo_demo
```

启动程序：

```bash
bash run_jetson.sh
```

如果不使用 `.sh` 文件，也可以直接运行：

```bash
source /opt/ros/humble/setup.bash
python3 src/detect.py
```

程序运行后会打开摄像头检测窗口，窗口中会显示：

- 目标类别
- 检测框
- 置信度
- FPS

---

## 4. 保存检测结果

运行时先点击检测窗口，然后使用下面几个按键：

```text
S：保存正确检测结果
E：保存错误案例
Q：退出程序
```

正确结果保存在：

```text
/home/nvidia/yolo_demo/results/success/
```

错误案例保存在：

```text
/home/nvidia/yolo_demo/results/error_cases/
```

---

## 5. 查看 ROS 2 结果

检测程序运行后，再打开一个 Jetson 终端。

先加载 ROS 2：

```bash
source /opt/ros/humble/setup.bash
```

查看当前 Topic：

```bash
ros2 topic list
```

可以看到：

```text
/detected_objects
```

查看实时检测结果：

```bash
ros2 topic echo /detected_objects
```

输出像：

```text
data: 'class=book, confidence=0.84, bbox=[78,119,583,644]'
---
```

其中：

```text
class       表示类别
confidence  表示置信度
bbox        表示检测框坐标
```

---

## 6. 实验验收

验收时我主要按下面的顺序进行：

### 1）启动检测程序

```bash
cd /home/nvidia/yolo_demo
bash run_jetson.sh
```

### 2）测试多目标识别

在摄像头前同时放两个不同类别的物体，例如：

```text
keyboard + laptop
```

检查是否能够同时识别两个类别。

### 3）检查 FPS

程序窗口会实时显示 FPS。

实验要求：

```text
FPS >= 5
```

实际测试时基本在：

```text
8.9 FPS
```

左右。

### 4）查看 ROS 2

打开第二个终端：

```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /detected_objects
```

检查类别、置信度和检测框坐标是否能够正常发布。

### 5）保存结果

```text
S：保存正确结果
E：保存错误案例
```

### 6）20 次测试

实验中进行了 20 次检测测试，其中 19 次识别正确：

```text
19 / 20 = 95%
```

满足实验要求的：

```text
Accuracy >= 80%
```

---

## 7. 运行中遇到的问题

在部署 Jetson 的过程中，我一开始使用 SSH 连接电脑和 Jetson，但是连接不是很稳定，后面改成直接使用数据线连接之后才正常完成文件传输和测试。

然后配置 Python 和 Conda 环境也花了比较长时间，主要是为了确认 PyTorch、Ultralytics、OpenCV 和 ROS 2 都能正常使用。环境配置完成之后，后面的模型加载和实时检测就比较顺利了。

---

## 8. 提交内容

这次实验提交的主要内容包括：

```text
dataset
best.pt
train.py
detect.py
run_jetson.sh
检测结果
结果视频
README.md
实验报告
```
