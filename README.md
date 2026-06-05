![CI](https://img.shields.io/github/actions/workflow/status/Aezakmi814/FatigueDetect/ci.yml?branch=main)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![PyQt5](https://img.shields.io/badge/UI-PyQt5-brightgreen)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-orange)
![ONNX](https://img.shields.io/badge/ONNX-CPU-blueviolet)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face_Landmark-ff69b4)
![License](https://img.shields.io/badge/License-GPLv3-green)

# 驾驶员疲劳检测系统

基于 **YOLOv8 (ONNX) + MediaPipe + PyQt5** 的驾驶员疲劳检测桌面应用，通过普通摄像头实时监测眼睛、嘴巴状态来判断驾驶员是否疲劳。

## 功能

- 🎯 实时检测：眼睛、嘴巴、打哈欠
- 📊 指标显示：EFV（眼睛疲劳值）、MFV（嘴巴疲劳值）、头部姿态
- ⚠️ 疲劳判断：检测到闭眼或打哈欠时触发警报
- 🖥️ 图形界面：PyQt5 可视化界面，操作简单直观
- 📷 支持图片检测和摄像头实时检测

## 环境要求

- Python 3.8+
- Windows / Linux / macOS

## 截图预览

> 准备好检测图片后运行程序

## 安装与运行

### 方式一：一键安装（推荐）

双击 `一键安装.bat`，自动安装依赖并启动程序。

### 方式二：手动安装

**有 NVIDIA 显卡的用户（GPU 加速）：**

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python main.pyw
```

**没有 NVIDIA 显卡的用户（CPU 推理）：**

```bash
# 先替换推理库（GPU版 → CPU版）
pip install onnxruntime
# 再安装其他依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 启动
python main.pyw
```

也可以直接双击 `main.pyw` 运行。

> 💡 **显卡说明**：程序会自动检测硬件，NVIDIA 用户安装 `onnxruntime-gpu` 获 CUDA 加速，Intel/AMD 用户可换 `onnxruntime-directml`，无独显自动回退 CPU，**无需手动配置**。

## 使用说明

1. 启动程序后，点击"选择图片"或"打开摄像头"
2. 系统自动检测并标注疲劳状态
3. 右侧面板显示详细疲劳指标

## 项目结构

```
FatigueDetect/
├── main.pyw                 # 程序入口
├── config/
│   └── settings.py          # 配置文件
├── core/
│   ├── face_detector.py     # 人脸检测
│   ├── fatigue_detector.py  # 疲劳检测
│   ├── fatigue_metrics.py   # 疲劳指标计算
│   └── landmark_detector.py # 人脸关键点
├── ui/
│   └── main_window.py       # PyQt5 主界面
├── utils/
│   └── messages.py          # 工具函数
├── models/
│   └── face_landmarker.task # 人脸关键点模型
├── eyesyawn.onnx            # YOLOv8 ONNX 检测模型
├── tests/                   # 单元测试
├── docs/                    # 架构文档
├── requirements.txt         # 依赖清单
├── 一键安装.bat             # 一键部署脚本
└── 使用说明.txt             # 使用说明
```

## 检测类别

| 类别 | 说明 |
|------|------|
| closed_eye | 闭眼 |
| open_eye | 睁眼 |
| yawning | 打哈欠 |

## 疲劳判断阈值

| 指标 | 阈值 | 说明 |
|------|------|------|
| EFV | < 0.42 | 眼睛疲劳度低于此值判断为疲劳 |
| MFV | > 0.97 | 嘴巴张度高于此值判断为打哈欠 |
| 头部俯仰角 | > 30° | 头部角度超过此值判断疲劳 |

## 贡献

欢迎贡献代码！请查看 [贡献指南](CONTRIBUTING.md) 了解如何参与项目开发。

## 致谢

- 本项目目标检测模型基于 [YOLOv8](https://github.com/ultralytics/ultralytics)（AGPL-3.0 许可证）训练并导出为 ONNX 格式
- 人脸关键点模型来自 [Google MediaPipe](https://github.com/google/mediapipe)（Apache 2.0 许可证）
- 训练数据集：[yawn_eye_dataset_new](https://www.kaggle.com/datasets/serenaraju/yawn-eye-dataset-new)（Kaggle）

## 许可证

本项目采用 [GNU General Public License v3.0](LICENSE) 开源协议。