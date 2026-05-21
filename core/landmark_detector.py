"""
关键点定位模块 - 基于MediaPipe Face Landmarker
使用 mp.tasks.vision.FaceLandmarker (mediapipe 0.10.x API)
模型文件: models/face_landmarker.task
"""
import os
import numpy as np
import cv2

_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                           "models", "face_landmarker.task")


class LandmarkDetector:
    """
    MediaPipe Face Landmarker 面部468点关键点检测器
    检测整张图片中的人脸，返回468个关键点坐标
    """
    def __init__(self):
        if not os.path.exists(_MODEL_PATH):
            raise FileNotFoundError(
                f"MediaPipe模型文件未找到: {_MODEL_PATH}\n"
                f"请下载 face_landmarker.task 放到 models/ 目录下"
            )
        try:
            import mediapipe as mp
            self._mp = mp
            options = mp.tasks.vision.FaceLandmarkerOptions(
                base_options=mp.tasks.BaseOptions(model_asset_path=_MODEL_PATH),
                running_mode=mp.tasks.vision.RunningMode.IMAGE,
                num_faces=1,
                min_face_detection_confidence=0.5,
                output_face_blendshapes=False,
                output_facial_transformation_matrixes=False,
            )
            self._landmarker = mp.tasks.vision.FaceLandmarker.create_from_options(options)
        except ImportError:
            raise ImportError(
                "mediapipe 库未安装\n"
                "  pip install mediapipe -i https://pypi.tuna.tsinghua.edu.cn/simple"
            )

    def get_landmarks(self, image):
        """
        获取面部468个关键点
        参数:
            image: 完整图像 (BGR)
        返回:
            (468,2) numpy array，失败时返回 None
        """
        if image is None or image.size == 0:
            return None

        try:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = self._mp.Image(
                image_format=self._mp.ImageFormat.SRGB, data=rgb
            )
            result = self._landmarker.detect(mp_image)

            if not result.face_landmarks:
                return None

            face_landmarks = result.face_landmarks[0]
            h, w = image.shape[:2]
            landmarks = np.array([
                (lm.x * w, lm.y * h) for lm in face_landmarks
            ], dtype=np.float64)
            return landmarks

        except Exception:
            return None

    def __del__(self):
        if hasattr(self, '_landmarker'):
            self._landmarker.close()
