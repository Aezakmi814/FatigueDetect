"""
程序入口 - 驾驶员疲劳检测系统
环境检查 + 启动主窗口

注意：
- 使用 .pyw 后缀运行时无控制台窗口
- 所有导入都在 main() 内部进行，确保错误能弹出消息框
"""
import sys


def warn_missing(msg):
    """用多样方式提示用户（不阻塞）"""
    import warnings
    warnings.warn(msg)
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("环境提示", msg)
        root.destroy()
    except Exception:
        print(f"[提示] {msg}", file=sys.stderr)


def main():
    """主函数 - 程序入口"""
    # === 第一步：检查核心依赖（缺了 PyQt5 就真没法用） ===
    try:
        import PyQt5  # noqa: F401
    except ImportError:
        msg = (
            "缺少 PyQt5，无法启动图形界面。\n\n"
            "请运行：pip install PyQt5>=5.15.0"
        )
        print(msg, file=sys.stderr)
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("无法启动", msg)
            root.destroy()
        except Exception:
            pass
        input("\n按 Enter 键退出...")
        sys.exit(1)

    # 现在可以安全使用 PyQt5 了
    from PyQt5.QtWidgets import QApplication, QMessageBox
    app = QApplication(sys.argv)

    # === 第二步：检查可选依赖（仅警告，不阻塞） ===
    optional_checks = {
        "cv2 (opencv-python)": "opencv-python>=4.8.0",
        "ultralytics": "ultralytics>=8.0.0",
        "mediapipe": "mediapipe>=0.10.0",
        "numpy": "numpy>=1.24.0",
    }
    for pkg_name, pip_name in optional_checks.items():
        mod_name = pkg_name.split(" ")[0]
        try:
            __import__(mod_name)
        except ImportError:
            warn_missing(
                f"未检测到 {pkg_name}。\n"
                f"请运行：pip install {pip_name}\n"
                f"缺少该库将导致部分功能不可用，但不影响界面展示。"
            )

    # === 第三步：启动主窗口 ===
    try:
        from ui.main_window import MainWindow
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "启动失败", f"程序启动时发生错误：\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
