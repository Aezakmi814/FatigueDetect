"""测试 - 疲劳指标计算"""
import numpy as np
import pytest
from core.fatigue_metrics import calculate_efv, calculate_mfv, estimate_head_pose


class TestCalculateEFV:
    """测试眼睛疲劳值计算"""

    def test_normal_eyes(self):
        """正常睁眼 - EFV 应较高"""
        landmarks = np.zeros((468, 2))
        # 左眼
        landmarks[33] = [100, 200]   # 左外眼角
        landmarks[133] = [200, 200]  # 左内眼角
        landmarks[159] = [150, 190]  # 左眼上
        landmarks[145] = [150, 210]  # 左眼下
        landmarks[158] = [150, 192]  # 左眼上2
        landmarks[153] = [150, 208]  # 左眼下2
        # 右眼
        landmarks[362] = [300, 200]  # 右外眼角
        landmarks[263] = [400, 200]  # 右内眼角
        landmarks[386] = [350, 190]  # 右眼上
        landmarks[374] = [350, 210]  # 右眼下
        landmarks[385] = [350, 192]  # 右眼上2
        landmarks[380] = [350, 208]  # 右眼下2

        efv = calculate_efv(landmarks)
        assert 0.0 < efv < 1.0

    def test_closed_eyes(self):
        """闭眼 - EFV 应接近 0"""
        landmarks = np.zeros((468, 2))
        # 左眼 - 上下眼睑重合
        landmarks[33] = [100, 200]
        landmarks[133] = [200, 200]
        landmarks[159] = [150, 200]
        landmarks[145] = [150, 200]
        landmarks[158] = [150, 200]
        landmarks[153] = [150, 200]
        # 右眼
        landmarks[362] = [300, 200]
        landmarks[263] = [400, 200]
        landmarks[386] = [350, 200]
        landmarks[374] = [350, 200]
        landmarks[385] = [350, 200]
        landmarks[380] = [350, 200]

        efv = calculate_efv(landmarks)
        assert efv == 0.0

    def test_none_landmarks(self):
        """空关键点 - 应返回默认值 1.0"""
        assert calculate_efv(None) == 1.0

    def test_insufficient_landmarks(self):
        """关键点不足 - 应返回默认值 1.0"""
        landmarks = np.zeros((100, 2))
        assert calculate_efv(landmarks) == 1.0


class TestCalculateMFV:
    """测试嘴巴疲劳值计算"""

    def test_mouth_open(self):
        """张嘴 - MFV 应较高"""
        landmarks = np.zeros((468, 2))
        landmarks[61] = [100, 300]   # 左嘴角
        landmarks[291] = [200, 300]  # 右嘴角
        landmarks[13] = [150, 280]   # 上唇
        landmarks[14] = [150, 350]   # 下唇（张嘴）

        mfv = calculate_mfv(landmarks)
        assert mfv > 0.5

    def test_mouth_closed(self):
        """闭嘴 - MFV 应较低"""
        landmarks = np.zeros((468, 2))
        landmarks[61] = [100, 300]
        landmarks[291] = [200, 300]
        landmarks[13] = [150, 298]
        landmarks[14] = [150, 302]

        mfv = calculate_mfv(landmarks)
        assert mfv < 0.1

    def test_none_landmarks(self):
        """空关键点 - 应返回默认值 0.0"""
        assert calculate_mfv(None) == 0.0

    def test_zero_width(self):
        """嘴角宽度为0 - 应返回 0.0"""
        landmarks = np.zeros((468, 2))
        landmarks[61] = [100, 300]
        landmarks[291] = [100, 300]  # 同一位置
        landmarks[13] = [100, 290]
        landmarks[14] = [100, 310]

        mfv = calculate_mfv(landmarks)
        assert mfv == 0.0


class TestEstimateHeadPose:
    """测试头部姿态估计"""

    def test_normal_pose(self):
        """正常头部姿态"""
        landmarks = np.zeros((468, 2))
        landmarks[1] = [320, 150]    # 鼻尖
        landmarks[152] = [320, 350]  # 下巴
        landmarks[33] = [280, 200]   # 左眼
        landmarks[263] = [360, 200]  # 右眼
        landmarks[61] = [290, 300]   # 左嘴角
        landmarks[291] = [350, 300]  # 右嘴角

        pitch, yaw, roll = estimate_head_pose(landmarks, (640, 480))
        assert isinstance(pitch, float)
        assert isinstance(yaw, float)
        assert isinstance(roll, float)

    def test_none_landmarks(self):
        """空关键点 - 应返回默认值"""
        pose = estimate_head_pose(None, (640, 480))
        assert pose == (0.0, 0.0, 0.0)

    def test_insufficient_landmarks(self):
        """关键点不足 - 应返回默认值"""
        landmarks = np.zeros((100, 2))
        pose = estimate_head_pose(landmarks, (640, 480))
        assert pose == (0.0, 0.0, 0.0)