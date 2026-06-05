"""测试 - 配置模块"""
import os
import pytest
from config.settings import ModelConfig, FatigueThreshold, WindowConfig, UIColor


class TestModelConfig:
    """测试模型配置"""

    def test_default_values(self):
        cfg = ModelConfig()
        assert cfg.conf_threshold == 0.1
        assert cfg.class_names == {0: "closed_eye", 1: "open_eye", 2: "yawning"}

    def test_model_path_exists(self):
        cfg = ModelConfig()
        assert os.path.isabs(cfg.yolo_path)


class TestFatigueThreshold:
    """测试疲劳阈值"""

    def test_default_thresholds(self):
        cfg = FatigueThreshold()
        assert cfg.efv_threshold == 0.42
        assert cfg.mfv_threshold == 0.97
        assert cfg.head_pitch_threshold == 30.0


class TestWindowConfig:
    """测试窗口配置"""

    def test_default_window(self):
        cfg = WindowConfig()
        assert cfg.width == 1200
        assert cfg.height == 800
        assert cfg.title == "驾驶员疲劳检测系统"


class TestUIColor:
    """测试UI颜色配置"""

    def test_colors_defined(self):
        ui = UIColor()
        assert ui.bg_dark.startswith("#")
        assert ui.accent_cyan.startswith("#")
        assert ui.status_normal.startswith("#")
        assert ui.status_fatigue.startswith("#")