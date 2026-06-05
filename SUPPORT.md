# 技术支持

## 常见问题

### 安装问题

**Q: 安装 onnxruntime-gpu 失败？**

A: 请确认你有 NVIDIA 显卡且已安装 CUDA。如果没有，使用 CPU 版本：
```bash
pip install onnxruntime>=1.20.0
```

**Q: PyQt5 安装失败？**

A: 尝试使用清华镜像源：
```bash
pip install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 运行问题

**Q: 程序启动后黑屏？**

A: 确保摄像头权限已开启，或尝试使用图片检测模式。

**Q: 检测不准确？**

A: 调整 `config/settings.py` 中的阈值参数，确保光线充足。

## 获取帮助

- 📖 [使用说明](README.md#使用说明)
- 🐛 [报告 Bug](https://github.com/Aezakmi814/FatigueDetect/issues/new?template=bug_report.md)
- 💡 [功能建议](https://github.com/Aezakmi814/FatigueDetect/issues/new?template=feature_request.md)

## 相关资源

- [YOLOv8 文档](https://docs.ultralytics.com/)
- [MediaPipe 文档](https://google.github.io/mediapipe/)
- [PyQt5 文档](https://www.riverbankcomputing.com/static/Docs/PyQt5/)