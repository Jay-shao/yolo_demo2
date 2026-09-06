from pathlib import Path
import time

import cv2
import torch
import rclpy

from rclpy.node import Node
from std_msgs.msg import String
from ultralytics import YOLO


class YoloDetectorNode(Node):

    def __init__(self):
        super().__init__("yolo_detector")

        self.publisher = self.create_publisher(
            String,
            "/detected_objects",
            10
        )

        self.project_dir = Path.home() / "yolo_demo"
        self.model_path = self.project_dir / "weights" / "best.pt"

        self.success_dir = self.project_dir / "results" / "success"
        self.error_dir = self.project_dir / "results" / "error_cases"

        self.success_dir.mkdir(parents=True, exist_ok=True)
        self.error_dir.mkdir(parents=True, exist_ok=True)

        if not self.model_path.exists():
            raise FileNotFoundError(f"模型不存在：{self.model_path}")

        self.device = 0 if torch.cuda.is_available() else "cpu"

        print(f"Device: {self.device}")
        self.model = YOLO(str(self.model_path))

        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

        if not self.cap.isOpened():
            raise RuntimeError("无法打开摄像头")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.previous_time = time.time()
        self.fps = 0.0

        self.success_count = 0
        self.error_count = 0

        self.timer = self.create_timer(0.01, self.detect)

        print("Started | Q: quit | S: save success | E: save error")


    def detect(self):
        ret, frame = self.cap.read()

        if not ret:
            print("Camera read failed")
            return

        results = self.model.predict(
            source=frame,
            imgsz=640,
            conf=0.40,
            device=self.device,
            verbose=False
        )

        result = results[0]
        annotated_frame = result.plot()

        if len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                class_name = self.model.names[class_id]

                msg = String()
                msg.data = (
                    f"class={class_name}, "
                    f"confidence={confidence:.2f}, "
                    f"bbox=[{x1},{y1},{x2},{y2}]"
                )

                self.publisher.publish(msg)

        current_time = time.time()
        delta_time = current_time - self.previous_time
        self.previous_time = current_time

        if delta_time > 0:
            current_fps = 1.0 / delta_time
            self.fps = 0.9 * self.fps + 0.1 * current_fps

        cv2.putText(
            annotated_frame,
            f"FPS: {self.fps:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            annotated_frame,
            "Q:Quit S:Save E:Error",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        cv2.imshow("YOLO11 ROS2 Detection", annotated_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            rclpy.shutdown()

        elif key == ord("s"):
            self.success_count += 1
            save_path = self.success_dir / f"success_{self.success_count:03d}.jpg"
            cv2.imwrite(str(save_path), annotated_frame)
            print(f"Success saved: {save_path}")

        elif key == ord("e"):
            self.error_count += 1
            save_path = self.error_dir / f"error_{self.error_count:03d}.jpg"
            cv2.imwrite(str(save_path), annotated_frame)
            print(f"Error saved: {save_path}")


    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = YoloDetectorNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()