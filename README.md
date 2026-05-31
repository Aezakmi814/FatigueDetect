# 驾驶员疲劳检测系统

基于 **YOLOv5 + PyQt5** 的驾驶员疲劳检测桌面应用，通过摄像头实时检测闭眼和打哈欠行为，判断驾驶员是否疲劳。

## 功能

- ✅ 实时检测：闭眼、打哈欠
- ✅ 显示参数：EFV（眼裂宽比）、MFV（嘴高比）、头部姿态
- ✅ 疲劳判断：检测到闭眼或打哈欠时发出警告
- ✅ 图形界面：PyQt5 可视化操作，无需编写代码
- ✅ 支持图片检测和摄像头实时检测

## 环境要求

- Python 3.8+
- Windows / Linux / macOS

## 安装与运行

### 方式一：一键安装（推荐）

双击 `一键安装.bat`，自动安装所有依赖。

### 方式二：手动安装

```bash
pip install -r requirements.txt
python main.pyw
```

或直接双击 `main.pyw`。

## 使用说明

1. 运行程序后，点击"选择图片"或"开启摄像头"
2. 系统自动检测人脸并分析疲劳状态
3. 右侧显示检测结果和疲劳参数

## 项目结构

```
FatigueDetect/
├── main.pyw                 # 主程序入口
├── config/
│   └── settings.py          # 配置文件
├── core/
│   ├── face_detector.py     # 人脸检测
│   ├── fatigue_detector.py  # 疲劳检测
│   ├── fatigue_metrics.py   # 疲劳指标计算
│   └── landmark_detector.py # 人脸关键点
├── ui/
│   └── main_window.py       # PyQt5 界面
├── utils/
│   └── messages.py          # 工具函数
├── models/
│   └── face_landmarker.task # 人脸关键点模型
├── eyesyawn.pt              # YOLOv5 检测模型
├── requirements.txt         # 依赖清单
├── 一键安装.bat             # 离线一键部署
└── 使用说明.txt             # 使用说明
```

## 检测类别

| 类别 | 说明 |
|------|------|
| closed_eye | 闭眼 |
| open_eye | 睁眼 |
| yawning | 打哈欠 |

## 疲劳判定阈值

| 参数 | 阈值 | 说明 |
|------|------|------|
| EFV | < 0.42 | 眼裂宽比低于此值判定闭眼疲劳 |
| MFV | > 0.97 | 嘴高比高于此值判定打哈欠 |
| 头部俯仰角 | > 30° | 低头角度超过此值判定疲劳 |

## 致谢与声明

- 本项目的检测模型基于 [YOLOv5](https://github.com/ultralytics/yolov5)（AGPL-3.0 许可证）训练
- 人脸关键点模型来自 [Google MediaPipe](https://github.com/google/mediapipe)（Apache 2.0 许可证）
- 训练数据集：[yawn_eye_dataset_new](https://www.kaggle.com/datasets/serenaraju/yawn-eye-dataset-new)（Kaggle）

## 许可证

本项目基于 [GNU General Public License v3.0](LICENSE) 开源。
