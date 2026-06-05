"""
人脸检测模块 - 自动选择最佳推理后端
优先顺序: CUDA → DirectML → CPU(onnxruntime) → CPU(OpenCV DNN)

用户只需 pip install -r requirements.txt，代码自动适配硬件
"""

import numpy as np
import cv2
import sys

# ── 后处理函数（所有后端共用） ──────────────────────

def _letterbox(img, target_size=(640, 640), color=(114, 114, 114)):
    shape = img.shape[:2]
    r = min(target_size[0] / shape[0], target_size[1] / shape[1])
    new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
    dw, dh = target_size[1] - new_unpad[0], target_size[0] - new_unpad[1]
    dw /= 2; dh /= 2
    img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right,
                             cv2.BORDER_CONSTANT, value=color)
    return img, r, (dw, dh)


def _nms(boxes, scores, iou_threshold=0.45):
    if len(boxes) == 0:
        return []
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    keep = []
    while len(order) > 0:
        i = order[0]
        keep.append(i)
        if len(order) == 1:
            break
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)
        inter = w * h
        iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-7)
        order = order[1:][iou <= iou_threshold]
    return keep


def _parse_yolo_output(outputs, conf_threshold, orig_shape, ratio, dw, dh, input_size):
    """解析 YOLOv8 ONNX 输出，返回检测结果列表"""
    orig_h, orig_w = orig_shape
    outputs = np.squeeze(outputs, axis=0)      # (7, 8400)
    outputs = np.transpose(outputs, (1, 0))     # (8400, 7)

    boxes = outputs[:, :4]
    cls_scores = outputs[:, 4:]
    max_scores = np.max(cls_scores, axis=1)
    max_classes = np.argmax(cls_scores, axis=1)

    mask = max_scores >= conf_threshold
    if not np.any(mask):
        return []

    boxes = boxes[mask]
    scores = max_scores[mask]
    classes = max_classes[mask]

    # 坐标转换
    boxes[:, 0] = (boxes[:, 0] * input_size[0] - dw) / ratio
    boxes[:, 1] = (boxes[:, 1] * input_size[1] - dh) / ratio
    boxes[:, 2] = boxes[:, 2] * input_size[0] / ratio
    boxes[:, 3] = boxes[:, 3] * input_size[1] / ratio

    half_w, half_h = boxes[:, 2] / 2, boxes[:, 3] / 2
    x1y1 = boxes[:, :2] - np.column_stack([half_w, half_h])
    x2y2 = boxes[:, :2] + np.column_stack([half_w, half_h])
    boxes_xyxy = np.concatenate([x1y1, x2y2], axis=1)

    boxes_xyxy[:, 0] = np.clip(boxes_xyxy[:, 0], 0, orig_w)
    boxes_xyxy[:, 1] = np.clip(boxes_xyxy[:, 1], 0, orig_h)
    boxes_xyxy[:, 2] = np.clip(boxes_xyxy[:, 2], 0, orig_w)
    boxes_xyxy[:, 3] = np.clip(boxes_xyxy[:, 3], 0, orig_h)

    # 逐类 NMS
    keep_indices = []
    for cls_id in range(3):
        cls_mask = classes == cls_id
        if np.any(cls_mask):
            cls_boxes = boxes_xyxy[cls_mask]
            cls_scores_arr = scores[cls_mask]
            cls_keep = _nms(cls_boxes, cls_scores_arr)
            global_idx = np.where(cls_mask)[0][cls_keep]
            keep_indices.extend(global_idx)

    if not keep_indices:
        return []

    detections = []
    for idx in keep_indices:
        x1, y1, x2, y2 = boxes_xyxy[idx].astype(int)
        detections.append([
            int(x1), int(y1), int(x2), int(y2),
            float(scores[idx]), int(classes[idx])
        ])
    return detections


def _compute_face_bbox(detections, img_shape):
    if not detections:
        return None
    h, w = img_shape[:2]
    xs = [d[0] for d in detections] + [d[2] for d in detections]
    ys = [d[1] for d in detections] + [d[3] for d in detections]
    x1, x2 = min(xs), max(xs)
    y1, y2 = min(ys), max(ys)
    fw, fh = x2 - x1, y2 - y1
    pad_x, pad_y = int(fw * 0.6), int(fh * 0.8)
    x1 = max(0, x1 - pad_x)
    y1 = max(0, y1 - pad_y)
    x2 = min(w, x2 + pad_x)
    y2 = min(h, y2 + pad_y)
    return [x1, y1, x2, y2]


# ── 主检测器 ──────────────────────────────────────

class EyeYawnDetector:
    """
    闭眼/打哈欠检测器
    自动选择最佳后端: CUDA → DirectML → CPU(onnx) → CPU(OpenCV)

    用户按自己需求装包即可，无需改代码:
      pip install onnxruntime            →  CPU 推理（默认，轻量）
      pip install onnxruntime-gpu        →  NVIDIA GPU 推理
      pip install onnxruntime-directml   →  Intel/AMD 显卡推理
    """

    def __init__(self, model_path="eyesyawn.onnx", conf_threshold=0.1):
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.class_names = {0: "closed_eye", 1: "open_eye", 2: "yawning"}
        self.input_size = (640, 640)

        # 选择后端
        self._backend = None
        self._session = None
        self._net = None
        self._select_backend()

    def _select_backend(self):
        """按优先级选择可用的推理后端"""
        backends = []

        # 1. onnxruntime-gpu (CUDA) — NVIDIA 显卡
        try:
            import onnxruntime as ort
            providers = ort.get_available_providers()
            if 'CUDAExecutionProvider' in providers:
                backends.append(('CUDA (onnxruntime-gpu)', ort, ['CUDAExecutionProvider', 'CPUExecutionProvider']))
        except ImportError:
            pass

        # 2. onnxruntime-directml — Intel/AMD 显卡
        try:
            import onnxruntime as ort
            providers = ort.get_available_providers()
            if 'DmlExecutionProvider' in providers:
                backends.append(('DirectML (onnxruntime-directml)', ort, ['DmlExecutionProvider', 'CPUExecutionProvider']))
        except ImportError:
            pass

        # 3. onnxruntime CPU — 通用，轻量
        try:
            import onnxruntime as ort
            if 'CPUExecutionProvider' in ort.get_available_providers():
                backends.append(('CPU (onnxruntime)', ort, ['CPUExecutionProvider']))
        except ImportError:
            pass

        # 4. OpenCV DNN — 终极兜底（打包版用）
        if cv2.__version__:
            backends.append(('CPU (OpenCV DNN)', None, None))

        # 选第一个可用的
        name, ort_mod, providers = backends[0]

        if ort_mod is not None:
            # onnxruntime 系列
            self._backend = name
            self._session = ort_mod.InferenceSession(
                self.model_path, providers=providers
            )
        else:
            # OpenCV DNN 兜底
            self._backend = name
            self._net = cv2.dnn.readNetFromONNX(self.model_path)
            self._net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self._net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def detect(self, image):
        if image is None or image.size == 0:
            return [], None

        orig_shape = image.shape[:2]
        letter_img, ratio, (dw, dh) = _letterbox(image, self.input_size)

        if self._session is not None:
            # ── onnxruntime 推理 ──
            blob = np.transpose(letter_img.astype(np.float32) / 255.0, (2, 0, 1))
            blob = np.expand_dims(blob, axis=0).astype(np.float32)
            outputs = self._session.run(None, {self._session.get_inputs()[0].name: blob})[0]
        else:
            # ── OpenCV DNN 推理 ──
            blob = cv2.dnn.blobFromImage(
                letter_img, 1.0 / 255.0, self.input_size,
                swapRB=False, crop=False
            )
            self._net.setInput(blob)
            outputs = self._net.forward()

        detections = _parse_yolo_output(
            outputs, self.conf_threshold, orig_shape,
            ratio, dw, dh, self.input_size
        )
        face_bbox = _compute_face_bbox(detections, image.shape)
        return detections, face_bbox
