# 驾驶员疲劳检测系统

基于图像处理的驾驶员疲劳检测系统，使用 YOLOv5 目标检测 + MediaPipe 面部关键点定位 + EFV/MFV 参数分析，综合判断驾驶员疲劳状态。

## 功能特点

- 基于 YOLOv5 的闭眼/睁眼/打哈欠目标检测
- 基于 MediaPipe 的 468 点面部关键点定位
- EFV 眼部疲劳值和 MFV 嘴部疲劳值计算
- 头部 3D 姿态角估计（pitch / yaw / roll）
- PyQt5 图形界面，直观显示检测结果

## 环境要求

- Windows 10 / 11
- Python 3.10 ~ 3.12
- 无需 GPU（CPU 即可运行）

## 安装步骤

### 方式一：一键安装（推荐）

双击 `install.bat`，脚本会自动完成：
1. 检查 Python 版本
2. 创建虚拟环境
3. 从国内镜像安装所有依赖
4. 验证安装结果

### 方式二：手动安装

```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 2. 安装依赖（国内推荐清华镜像）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用方法

双击 `run.bat` 启动程序：

1. 点击「选择图片」按钮，选择驾驶员面部照片（支持 jpg/png/bmp）
2. 点击「开始检测」，等待检测完成
3. 查看结果：
   - 左侧：原始图像
   - 右侧：检测标注图（显示检测框和标签）
   - 中部：疲劳状态显示（正常/轻度疲劳/疲劳）
   - 下方：检测参数详情（EFV、MFV、头部姿态角）

## 目录结构

```
├── main.pyw                 # 程序入口（双击运行）
├── eyesyawn.pt              # YOLO 疲劳检测模型
├── install.bat              # 一键安装环境
├── run.bat                  # 启动程序
├── requirements.txt         # 依赖清单
├── config/
│   └── settings.py          # 系统配置
├── core/
│   ├── face_detector.py     # 目标检测模块
│   ├── landmark_detector.py # 关键点定位模块
│   ├── fatigue_metrics.py   # EFV/MFV/头部姿态计算
│   └── fatigue_detector.py  # 疲劳检测主调度
├── ui/
│   └── main_window.py       # PyQt5 主界面
├── utils/
│   └── messages.py          # 提示文案
├── models/
│   └── face_landmarker.task # MediaPipe 模型
└── data/                    # 测试图片
```

## 技术栈

- Python 3.12
- PyQt5（图形界面）
- Ultralytics YOLO（目标检测）
- MediaPipe（面部关键点定位）
- OpenCV（图像处理）
- NumPy（数值计算）
