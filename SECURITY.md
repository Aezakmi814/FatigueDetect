# 安全策略

## 报告安全漏洞

如果你发现本项目存在安全漏洞，请**不要**通过公开的 Issue 报告。

请通过以下方式报告：

1. 在 [Issues](https://github.com/Aezakmi814/FatigueDetect/issues) 中创建一个标题为 `[SECURITY] 安全漏洞报告` 的 Issue
2. **不要**在 Issue 中包含漏洞的详细利用方式
3. 描述漏洞的影响范围和潜在风险

我们会在 48 小时内回复，并与你合作解决问题。

## 安全最佳实践

使用本项目时，请注意：

- 本项目仅用于学习和研究目的
- 不要在生产环境中直接使用
- 模型文件（`.onnx`、`.task`）来自第三方，请确保来源可信
- 本项目不收集任何用户数据

## 依赖安全

本项目使用的依赖：

| 依赖 | 版本要求 | 许可证 |
|------|----------|--------|
| PyQt5 | >= 5.15.0 | GPL v3 |
| opencv-python | >= 4.8.0 | Apache 2.0 |
| numpy | >= 1.24.0 | BSD 3-Clause |
| mediapipe | >= 0.10.0 | Apache 2.0 |
| onnxruntime | >= 1.20.0 | MIT |

建议定期更新依赖以获取安全补丁：

```bash
pip install --upgrade -r requirements.txt
```