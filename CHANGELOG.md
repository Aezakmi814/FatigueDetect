# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

## [0.1.0] - 2026-05-31

### 新增

- 基于 YOLOv8 (ONNX) 的眼睛/打哈欠检测
- 基于 MediaPipe 的面部关键点检测（468点）
- 疲劳指标计算：EFV（眼睛疲劳值）、MFV（嘴巴疲劳值）、头部姿态估计
- PyQt5 图形界面，支持图片检测和摄像头实时检测
- 自动选择推理后端：CUDA → DirectML → CPU(onnxruntime) → CPU(OpenCV)
- 一键安装脚本（Windows）
- CI/CD 工作流
- Issue 和 PR 模板

### 技术栈

- Python 3.8+
- PyQt5
- OpenCV
- YOLOv8 (ONNX)
- MediaPipe

### 训练数据

- [yawn_eye_dataset_new](https://www.kaggle.com/datasets/serenaraju/yawn-eye-dataset-new) (Kaggle)