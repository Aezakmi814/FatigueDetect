# 贡献指南

感谢你对 FatigueDetect 项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告 Bug

1. 在 [Issues](https://github.com/Aezakmi814/FatigueDetect/issues) 页面搜索是否已有类似问题
2. 如果没有，点击 "New Issue" 选择 "Bug 报告" 模板
3. 填写详细信息，包括复现步骤、截图、环境信息

### 提交功能建议

1. 在 Issues 中选择 "功能建议" 模板
2. 描述你希望添加的功能和使用场景

### 提交代码

1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feature/your-feature`
3. 提交你的修改：`git commit -m 'feat: add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 创建一个 Pull Request

## 开发环境搭建

### 前置条件

- Python 3.8+
- pip
- Git

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/Aezakmi814/FatigueDetect.git
cd FatigueDetect

# 2. 创建虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 安装开发依赖
pip install pytest ruff
```

### 代码规范

- 使用 [Ruff](https://github.com/astral-sh/ruff) 进行代码格式化和检查
- 行宽限制：100 字符
- 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范

```bash
# 格式化代码
ruff format .

# 检查代码
ruff check .
```

### 运行测试

```bash
pytest tests/ -v
```

## 项目结构

```
FatigueDetect/
├── main.pyw              # 程序入口
├── config/               # 配置模块
├── core/                 # 核心检测逻辑
├── ui/                   # PyQt5 界面
├── utils/                # 工具函数
├── models/               # 模型文件
└── tests/                # 测试代码
```

## 提交规范

| 前缀 | 说明 |
|------|------|
| feat: | 新功能 |
| fix: | Bug 修复 |
| docs: | 文档更新 |
| style: | 代码格式（不影响逻辑） |
| refactor: | 重构 |
| test: | 测试相关 |
| chore: | 构建/工具相关 |

## 行为准则

请遵守 [行为准则](CODE_OF_CONDUCT.md)，保持友善和尊重。

## 问题反馈

如有疑问，欢迎在 Issues 中提问或联系项目维护者。