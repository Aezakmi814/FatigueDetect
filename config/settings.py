"""
配置模块 - 驾驶员疲劳检测系统
集中管理所有配置参数
"""
import os
from dataclasses import dataclass, field

# 项目根目录（settings.py 所在目录的上级）
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@dataclass
class ModelConfig:
    yolo_path: str = os.path.join(_PROJECT_ROOT, "eyesyawn.pt")
    conf_threshold: float = 0.1
    class_names: dict = field(default_factory=lambda: {0: "closed_eye", 1: "open_eye", 2: "yawning"})

@dataclass
class FatigueThreshold:
    """疲劳判定阈值（对应报告中的阈值）"""
    efv_threshold: float = 0.42   # EFV < 0.42 判定闭眼疲劳
    mfv_threshold: float = 0.97   # MFV > 0.97 判定打哈欠
    head_pitch_threshold: float = 30.0  # 俯仰角 > 30 判定低头

@dataclass
class WindowConfig:
    """窗口配置"""
    title: str = "驾驶员疲劳检测系统"
    width: int = 1200
    height: int = 800

@dataclass
class UIColor:
    """UI配色配置（简洁清晰风格）"""
    bg_dark: str = "#f0f0f0"       # 浅灰背景
    bg_panel: str = "#ffffff"      # 白色面板
    accent_cyan: str = "#2196F3"   # 蓝色强调
    accent_orange: str = "#FF9800" # 橙色告警
    text_light: str = "#333333"    # 深色文字
    status_normal: str = "#4CAF50"  # 正常状态颜色（绿色）
    status_fatigue: str = "#f44336" # 疲劳状态颜色（红色）