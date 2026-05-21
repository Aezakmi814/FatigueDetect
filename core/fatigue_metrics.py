"""
疲劳参数计算模块
EFV(眼部疲劳值), MFV(嘴部疲劳值), 头部3D姿态角
适配 MediaPipe 468点模型
关键点索引:
- 左眼: 33(外眼角) 133(内眼角) 159(上眼睑) 145(下眼睑) 158(上睑内) 153(下睑内)
- 右眼: 362(内眼角) 263(外眼角) 386(上眼睑) 374(下眼睑) 385(上睑内) 380(下睑内)
- 嘴部: 61(左嘴角) 291(右嘴角) 13(上唇中) 14(下唇中)
- 鼻尖: 1, 下巴: 152
"""
import numpy as np
import cv2


def calculate_efv(landmarks):
    """
    计算眼部疲劳值 EFV (基于EAR算法)
    参数:
        landmarks: (468,2) 关键点坐标
    返回:
        EFV值, float；失败返回 1.0
    """
    if landmarks is None or len(landmarks) < 468:
        return 1.0

    # 左眼 EAR
    left_vertical1 = np.linalg.norm(landmarks[159] - landmarks[145])
    left_vertical2 = np.linalg.norm(landmarks[158] - landmarks[153])
    left_horizontal = np.linalg.norm(landmarks[33] - landmarks[133])

    # 右眼 EAR
    right_vertical1 = np.linalg.norm(landmarks[386] - landmarks[374])
    right_vertical2 = np.linalg.norm(landmarks[385] - landmarks[380])
    right_horizontal = np.linalg.norm(landmarks[362] - landmarks[263])

    left_ear = (left_vertical1 + left_vertical2) / (2.0 * left_horizontal) if left_horizontal > 0 else 0
    right_ear = (right_vertical1 + right_vertical2) / (2.0 * right_horizontal) if right_horizontal > 0 else 0

    return (left_ear + right_ear) / 2.0


def calculate_mfv(landmarks):
    """
    计算嘴部疲劳值 MFV (基于MAR算法)
    参数:
        landmarks: (468,2) 关键点坐标
    返回:
        MFV值, float；失败返回 0.0
    """
    if landmarks is None or len(landmarks) < 468:
        return 0.0

    vertical = np.linalg.norm(landmarks[13] - landmarks[14])
    horizontal = np.linalg.norm(landmarks[61] - landmarks[291])

    if horizontal == 0:
        return 0.0

    return vertical / horizontal


def estimate_head_pose(landmarks, img_size):
    """
    估计头部3D姿态角 (pitch, yaw, roll)
    使用 solvePnP
    参数:
        landmarks: (468,2)
        img_size: (宽, 高)
    返回:
        (pitch, yaw, roll) 角度值
    """
    if landmarks is None or len(landmarks) < 468:
        return (0.0, 0.0, 0.0)

    # 2D图像关键点
    image_points = np.array([
        landmarks[1],      # 鼻尖
        landmarks[152],    # 下巴底
        landmarks[33],     # 左眼外眼角
        landmarks[263],    # 右眼外眼角
        landmarks[61],     # 左嘴角
        landmarks[291],    # 右嘴角
    ], dtype=np.float64)

    # 3D模型关键点 (mm)
    model_points = np.array([
        (0.0, 0.0, 0.0),
        (0.0, -330.0, -65.0),
        (-225.0, 170.0, -135.0),
        (225.0, 170.0, -135.0),
        (-150.0, -150.0, -125.0),
        (150.0, -150.0, -125.0),
    ], dtype=np.float64)

    w, h = img_size
    focal_length = w
    center = (w / 2, h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype=np.float64)

    dist_coeffs = np.zeros((4, 1))

    try:
        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points, image_points, camera_matrix, dist_coeffs
        )
        if not success:
            return (0.0, 0.0, 0.0)

        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        euler_angles = _rotation_matrix_to_euler(rotation_matrix)

        pitch = np.degrees(euler_angles[0])
        yaw = np.degrees(euler_angles[1])
        roll = np.degrees(euler_angles[2])

        return (pitch, yaw, roll)

    except (cv2.error, np.linalg.LinAlgError):
        return (0.0, 0.0, 0.0)


def _rotation_matrix_to_euler(R):
    """旋转矩阵转欧拉角"""
    sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0
    return np.array([x, y, z])
