# 架构设计

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                   main.pyw                      │
│                  (程序入口)                       │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              ui/main_window.py                  │
│              (PyQt5 主界面)                       │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│            core/fatigue_detector.py             │
│              (疲劳检测主逻辑)                     │
└────┬─────────────┬─────────────┬────────────────┘
     │             │             │
┌────▼────┐  ┌─────▼─────┐  ┌───▼────────────┐
│  core/  │  │  core/    │  │    core/       │
│  face   │  │ landmark  │  │    fatigue     │
│ detector│  │ detector  │  │   metrics      │
└─────────┘  └───────────┘  └────────────────┘
  (YOLOv8)   (MediaPipe)    (EFV/MFV/姿态)
```

## 核心模块

### 1. Face Detector (core/face_detector.py)

- **职责**: 使用 YOLOv8 ONNX 模型检测眼睛和嘴巴
- **输入**: OpenCV BGR 图像
- **输出**: 检测框列表 + 人脸区域
- **后端选择**: 自动按优先级选择 CUDA → DirectML → CPU(onnx) → CPU(OpenCV)

### 2. Landmark Detector (core/landmark_detector.py)

- **职责**: 使用 MediaPipe 检测 468 个面部关键点
- **输入**: OpenCV BGR 图像
- **输出**: (468, 2) 关键点数组

### 3. Fatigue Metrics (core/fatigue_metrics.py)

- **职责**: 计算疲劳指标
- **指标**:
  - EFV (Eye Fatigue Value): 眼睛疲劳值，基于 EAR 算法
  - MFV (Mouth Fatigue Value): 嘴巴疲劳值，基于 MAR 算法
  - Head Pose: 头部 3D 姿态 (pitch, yaw, roll)

### 4. Fatigue Detector (core/fatigue_detector.py)

- **职责**: 整合所有模块，执行完整疲劳检测流程
- **流程**:
  1. YOLOv8 检测眼睛/嘴巴
  2. MediaPipe 检测关键点
  3. 计算 EFV/MFV/头部姿态
  4. 综合判断疲劳等级

## 数据流

```
摄像头/图片
    │
    ▼
[YOLOv8 检测] → 检测框 (眼睛/嘴巴)
    │
    ▼
[MediaPipe 关键点] → 468 个关键点
    │
    ▼
[指标计算] → EFV, MFV, Head Pose
    │
    ▼
[疲劳判断] → 正常/轻度疲劳/疲劳
    │
    ▼
[UI 显示] → PyQt5 界面
```

## 配置管理

所有配置集中在 `config/settings.py`:

- `ModelConfig`: 模型路径、置信度阈值
- `FatigueThreshold`: 疲劳判断阈值
- `WindowConfig`: 窗口尺寸和标题
- `UIColor`: UI 颜色方案