"""测试 - 疲劳检测器"""
import numpy as np
import pytest
from core.fatigue_detector import FatigueResult


class TestFatigueResult:
    """测试疲劳结果数据类"""

    def test_default_values(self):
        result = FatigueResult()
        assert result.has_face is False
        assert result.face_bbox is None
        assert result.detections == []
        assert result.efv == 1.0
        assert result.mfv == 0.0
        assert result.head_pose == (0.0, 0.0, 0.0)
        assert result.is_eye_fatigue is False
        assert result.is_mouth_fatigue is False
        assert result.is_head_abnormal is False
        assert result.fatigue_level == "未检测"

    def test_fatigue_states(self):
        """测试疲劳状态设置"""
        result = FatigueResult()
        result.fatigue_level = "疲劳"
        assert result.fatigue_level == "疲劳"

        result.fatigue_level = "轻度疲劳"
        assert result.fatigue_level == "轻度疲劳"

        result.fatigue_level = "正常"
        assert result.fatigue_level == "正常"