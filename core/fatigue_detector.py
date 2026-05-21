"""
疲劳检测调度器
组合管线：
  1. eyesyawn 直接检测闭眼/打哈欠（主判定，精度高）
  2. MediaPipe 关键点 → EFV/MFV/头部姿态（匹配报告描述）
"""
from dataclasses import dataclass, field
import cv2
import numpy as np

from core.face_detector import EyeYawnDetector
from core.landmark_detector import LandmarkDetector
from core.fatigue_metrics import calculate_efv, calculate_mfv, estimate_head_pose
from config.settings import ModelConfig, FatigueThreshold

# 类别中文名（Qt面板用）
CLASS_NAMES_CN = {
    0: "闭眼",
    1: "睁眼",
    2: "打哈欠",
}
# 类别英文名（OpenCV图片标注用，避免中文变问号）
CLASS_NAMES_EN = {
    0: "closed_eye",
    1: "open_eye",
    2: "yawning",
}
# 检测框颜色
CLASS_COLORS = {
    0: (0, 0, 255),
    1: (0, 255, 0),
    2: (0, 165, 255),
}


@dataclass
class FatigueResult:
    """疲劳检测结果"""
    has_face: bool = False
    face_bbox: list = None
    detections: list = field(default_factory=list)  # [(cls_name, conf, bbox), ...]
    landmarks: np.ndarray = None
    efv: float = 1.0
    mfv: float = 0.0
    head_pose: tuple = (0.0, 0.0, 0.0)
    is_eye_fatigue: bool = False
    is_mouth_fatigue: bool = False
    is_head_abnormal: bool = False
    fatigue_level: str = "未检测"


class FatigueDetector:
    """疲劳检测调度器"""

    def __init__(self):
        model_cfg = ModelConfig()
        threshold_cfg = FatigueThreshold()

        self.efv_threshold = threshold_cfg.efv_threshold
        self.mfv_threshold = threshold_cfg.mfv_threshold
        self.head_threshold = threshold_cfg.head_pitch_threshold

        # 子模块
        self.detector = EyeYawnDetector(
            model_path=model_cfg.yolo_path,
            conf_threshold=model_cfg.conf_threshold
        )
        self.landmark_detector = LandmarkDetector()

        self.model_info = {
            "检测模型": "eyesyawn",
            "关键点模型": "MediaPipe 468点",
            "EFV阈值": str(self.efv_threshold),
            "MFV阈值": str(self.mfv_threshold),
        }

    def detect(self, image):
        """
        完整疲劳检测

        参数:
            image: OpenCV BGR图像
        返回:
            FatigueResult 对象
        """
        result = FatigueResult()
        img_h, img_w = image.shape[:2]

        # === 1. eyesyawn 直接检测 ===
        detections, face_bbox = self.detector.detect(image)
        if not detections:
            result.fatigue_level = "未检测到人脸"
            return result

        result.has_face = True
        result.face_bbox = face_bbox

        # 整理检测结果
        has_closed_eye = False
        has_yawning = False
        det_list = []
        for det in detections:
            x1, y1, x2, y2, conf, cls_id = det
            cls_name = self.detector.class_names.get(cls_id, f"class_{cls_id}")
            det_list.append((cls_name, conf, (x1, y1, x2, y2)))
            if cls_id == 0:
                has_closed_eye = True
            elif cls_id == 2:
                has_yawning = True
        result.detections = det_list

        # === 2. MediaPipe 关键点 ===
        landmarks = self.landmark_detector.get_landmarks(image)
        if landmarks is not None:
            result.landmarks = landmarks
            result.efv = calculate_efv(landmarks)
            result.mfv = calculate_mfv(landmarks)
            result.head_pose = estimate_head_pose(landmarks, (img_w, img_h))

        # === 3. 疲劳判定 ===
        # 主信号：eyesyawn 直接检测（保留精度）
        result.is_eye_fatigue = has_closed_eye
        result.is_mouth_fatigue = has_yawning
        pitch, yaw, roll = result.head_pose
        result.is_head_abnormal = abs(pitch) > self.head_threshold

        # EFV/MFV 阈值仅用于显示/报告对比，不参与判定
        # （MediaPipe 468点与报告原 dlib 68点阈值不兼容）

        fatigue_count = sum([result.is_eye_fatigue,
                            result.is_mouth_fatigue])
        if fatigue_count >= 2:
            result.fatigue_level = "疲劳"
        elif fatigue_count == 1:
            result.fatigue_level = "轻度疲劳"
        else:
            result.fatigue_level = "正常"

        return result

    # ---- 图片标注 ----

    def _draw_label_bg(self, img, text, x, y, color):
        """带深灰底色的文字标注"""
        font_scale = 0.5
        thickness = 1
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX,
                                       font_scale, thickness)
        pad = 3
        cv2.rectangle(img,
                      (x, y - th - pad), (x + tw + pad * 2, y + pad),
                      (64, 64, 64), -1)
        cv2.rectangle(img,
                      (x, y - th - pad), (x + tw + pad * 2, y + pad),
                      color, 1)
        cv2.putText(img, text, (x + pad, y - pad),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)

    def draw_result(self, image, result):
        """
        在图像上绘制检测结果（英文标注，避免OpenCV中文变问号）
        """
        img = image.copy()

        if not result.has_face or not result.detections:
            cv2.putText(img, "No face detected", (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return img

        name_to_id = {v: k for k, v in self.detector.class_names.items()}

        # 每个类别只标最高置信度
        best_per_class = {}
        for cls_name, conf, bbox in result.detections:
            cls_id = name_to_id.get(cls_name, -1)
            if cls_id not in best_per_class or conf > best_per_class[cls_id][0]:
                best_per_class[cls_id] = (conf, bbox)

        # 画所有框
        for cls_name, conf, bbox in result.detections:
            x1, y1, x2, y2 = map(int, bbox)
            cls_id = name_to_id.get(cls_name, -1)
            color = CLASS_COLORS.get(cls_id, (0, 255, 0))
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 1)

        # 标最高置信度标签
        for cls_id, (conf, bbox) in best_per_class.items():
            x1, y1, x2, y2 = map(int, bbox)
            color = CLASS_COLORS.get(cls_id, (0, 255, 0))
            en_name = CLASS_NAMES_EN.get(cls_id, "unknown")
            self._draw_label_bg(img, f"{en_name} {conf:.2f}", x1 + 3, y1 + 3, color)

        # 状态标签（左上角含EFV/MFV）
        status = result.fatigue_level
        if status == "疲劳":
            status_en = "FATIGUE"
            s_color = (0, 0, 255)
        elif status == "轻度疲劳":
            status_en = "Mild Fatigue"
            s_color = (0, 165, 255)
        elif status == "正常":
            status_en = "Normal"
            s_color = (0, 255, 0)
        else:
            status_en = status
            s_color = (0, 0, 255)

        info = f"{status_en} | EFV:{result.efv:.3f} MFV:{result.mfv:.3f}"
        self._draw_label_bg(img, info, 15, 35, s_color)

        return img
