"""
人脸检测模块 - 基于eyesyawn模型
检测闭眼/睁眼/打哈欠，同时输出人脸区域
"""


class EyeYawnDetector:
    """
    闭眼/打哈欠检测器
    检测 closed_eye, open_eye, yawning
    同时根据检测框计算人脸区域
    """
    def __init__(self, model_path="eyesyawn.pt", conf_threshold=0.1):
        try:
            from ultralytics import YOLO
        except ImportError:
            raise ImportError(
                "ultralytics 库未安装\n"
                "  pip install ultralytics"
            )

        try:
            self.model = YOLO(model_path)
        except Exception as e:
            raise RuntimeError(
                f"模型加载失败: {str(e)}\n"
                f"请确认 eyesyawn.pt 在项目根目录下"
            )
        self.conf_threshold = conf_threshold
        self.class_names = {0: "closed_eye", 1: "open_eye", 2: "yawning"}

    def detect(self, image):
        """
        检测图片中的闭眼/睁眼/打哈欠

        参数:
            image: OpenCV BGR图像
        返回:
            (detections, face_bbox)
            detections: [(x1,y1,x2,y2,conf,cls_id), ...]
            face_bbox: [x1,y1,x2,y2] 或 None（无人脸区域时）
        """
        if image is None or image.size == 0:
            return [], None

        results = self.model(image, conf=self.conf_threshold, verbose=False)
        detections = []

        if results[0].boxes is not None and len(results[0].boxes) > 0:
            for box, conf, cls_id in zip(
                results[0].boxes.xyxy, results[0].boxes.conf, results[0].boxes.cls
            ):
                x1, y1, x2, y2 = map(int, box)
                detections.append([x1, y1, x2, y2, float(conf), int(cls_id)])

        # 从所有检测框计算人脸区域（取并集+向外扩展）
        face_bbox = self._compute_face_bbox(detections, image.shape)

        return detections, face_bbox

    def _compute_face_bbox(self, detections, img_shape):
        """从检测框估算人脸区域"""
        if not detections:
            return None

        h, w = img_shape[:2]
        xs = [d[0] for d in detections] + [d[2] for d in detections]
        ys = [d[1] for d in detections] + [d[3] for d in detections]

        x1 = min(xs)
        y1 = min(ys)
        x2 = max(xs)
        y2 = max(ys)

        # 向外扩展 60%（眼睛/嘴巴框通常比全脸小很多）
        fw = x2 - x1
        fh = y2 - y1
        pad_x = int(fw * 0.6)
        pad_y = int(fh * 0.8)

        x1 = max(0, x1 - pad_x)
        y1 = max(0, y1 - pad_y)
        x2 = min(w, x2 + pad_x)
        y2 = min(h, y2 + pad_y)

        return [x1, y1, x2, y2]
