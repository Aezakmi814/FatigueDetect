"""
主界面模块 - 驾驶员疲劳检测系统
简洁清晰UI，上下分栏布局
"""
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTextEdit, QFileDialog,
                             QMessageBox, QSplitter, QFrame, QApplication, QGridLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage, QFont, QColor, QPalette

from core.fatigue_detector import FatigueDetector, CLASS_NAMES_CN
from config.settings import WindowConfig, UIColor, FatigueThreshold
from utils.messages import *

class MainWindow(QMainWindow):
    """主窗口类 - 驾驶员疲劳检测系统界面"""

    def __init__(self):
        super().__init__()
        self.current_image = None
        self.detector = None
        self.win_cfg = WindowConfig()
        self.ui_color = UIColor()
        self.init_ui()

    def init_ui(self):
        """初始化界面 - 上下分栏布局（与旧项目左右分栏区分）"""
        self.setWindowTitle(self.win_cfg.title)
        self.setGeometry(100, 100, self.win_cfg.width, self.win_cfg.height)

        # 简洁主题
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {self.ui_color.bg_dark}; }}
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # ============ 上区：图像显示 ============
        image_widget = QWidget()
        image_widget.setStyleSheet(f"background-color: {self.ui_color.bg_panel}; border: 1px solid #ddd; border-radius: 4px;")
        image_layout = QHBoxLayout()
        image_widget.setLayout(image_layout)

        # 原图显示
        self.original_label = QLabel(MSG_PLEASE_SELECT)
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(520, 440)
        self.original_label.setStyleSheet(f"""
            border: 1px solid #ccc;
            background-color: #fafafa;
            color: #666;
            border-radius: 2px;
            font-size: 14px;
        """)
        image_layout.addWidget(self.original_label)

        # 结果图显示
        self.result_label = QLabel(MSG_RESULT_PLACEHOLDER)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setMinimumSize(520, 440)
        self.result_label.setStyleSheet(f"""
            border: 1px solid #ccc;
            background-color: #fafafa;
            color: #666;
            border-radius: 2px;
            font-size: 14px;
        """)
        image_layout.addWidget(self.result_label)

        main_layout.addWidget(image_widget)

        # ============ 下区：控制面板 + 状态 + 结果 ============
        bottom_widget = QWidget()
        bottom_widget.setStyleSheet(f"background-color: {self.ui_color.bg_panel}; border: 1px solid #ddd; border-radius: 4px;")
        bottom_layout = QHBoxLayout()
        bottom_widget.setLayout(bottom_layout)

        # --- 下区左：操作按钮 ---
        btn_widget = QWidget()
        btn_widget.setStyleSheet("background-color: transparent;")
        btn_layout = QVBoxLayout()
        btn_widget.setLayout(btn_layout)

        self.select_btn = QPushButton("选择图片")
        self.select_btn.setMinimumHeight(40)
        self.select_btn.setMinimumWidth(140)
        self.select_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.ui_color.accent_cyan};
                color: white;
                border: none; border-radius: 4px;
                font-size: 13px; padding: 6px;
            }}
            QPushButton:hover {{ background-color: #1976D2; }}
        """)
        self.select_btn.clicked.connect(self.select_image)
        btn_layout.addWidget(self.select_btn)

        btn_layout.addSpacing(10)

        self.detect_btn = QPushButton("开始检测")
        self.detect_btn.setMinimumHeight(40)
        self.detect_btn.setMinimumWidth(140)
        self.detect_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.ui_color.accent_orange};
                color: white;
                border: none; border-radius: 4px;
                font-size: 13px; padding: 6px;
            }}
            QPushButton:hover {{ background-color: #F57C00; }}
            QPushButton:disabled {{ background-color: #ccc; color: #999; }}
        """)
        self.detect_btn.clicked.connect(self.start_detect)
        btn_layout.addWidget(self.detect_btn)

        btn_layout.addStretch()
        bottom_layout.addWidget(btn_widget)

        # --- 下区中：疲劳状态大字体显示 ---
        status_widget = QWidget()
        status_widget.setStyleSheet("background-color: transparent;")
        status_layout = QVBoxLayout()
        status_widget.setLayout(status_layout)

        status_layout.addSpacing(5)
        status_label = QLabel("驾驶员状态")
        status_label.setStyleSheet("color: #333; font-size: 12px; font-weight: bold; background: transparent;")
        status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(status_label)

        self.status_display = QLabel(MSG_WAITING)
        self.status_display.setAlignment(Qt.AlignCenter)
        self.status_display.setMinimumHeight(60)
        self.status_display.setStyleSheet("""
            color: #333;
            font-size: 24px;
            font-weight: bold;
            background-color: #fafafa;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 8px;
        """)
        status_layout.addWidget(self.status_display)

        # 参数详情
        self.param_text = QTextEdit()
        self.param_text.setReadOnly(True)
        self.param_text.setMaximumHeight(100)
        self.param_text.setMinimumWidth(200)
        self.param_text.setStyleSheet("""
            background-color: #fafafa;
            color: #333;
            border: 1px solid #ccc;
            border-radius: 2px;
            font-size: 12px;
            padding: 4px;
        """)
        self.param_text.setPlainText("检测目标: --\nEFV: --  MFV: --\n头部姿态: --\n眼部疲劳: --\n嘴部疲劳: --")
        status_layout.addWidget(self.param_text)

        bottom_layout.addWidget(status_widget)

        main_layout.addWidget(bottom_widget)

    def select_image(self):
        """选择图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "",
            "图片文件 (*.jpg *.jpeg *.png *.bmp)"
        )
        if not file_path:
            return

        self.current_image = cv2.imread(file_path)
        if self.current_image is None:
            QMessageBox.warning(self, "错误", MSG_LOAD_FAIL.replace("模型", "图片"))
            return

        # 显示原图
        self.display_image(self.current_image, self.original_label)
        # 清空结果
        self.result_label.clear()
        self.result_label.setText(MSG_RESULT_PLACEHOLDER)
        self.status_display.setText(MSG_WAITING)
        self.status_display.setStyleSheet("""
            color: #333; font-size: 24px; font-weight: bold;
            background-color: #fafafa; border: 1px solid #ccc;
            border-radius: 4px; padding: 8px;
        """)
        self.param_text.setPlainText("检测目标: --\nEFV: --  MFV: --\n头部姿态: --\n眼部疲劳: --\n嘴部疲劳: --")

    def start_detect(self):
        """开始检测"""
        if self.current_image is None:
            QMessageBox.warning(self, "提示", MSG_NO_IMAGE)
            return

        # 延迟初始化检测器
        if self.detector is None:
            try:
                self.param_text.setPlainText(MSG_LOADING)
                QApplication.processEvents()
                self.detector = FatigueDetector()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"{MSG_LOAD_FAIL}: {str(e)}\n\n请确保:\n1. 已安装 ultralytics 和 mediapipe\n2. eyesyawn.pt 在项目根目录下\n3. models/face_landmarker.task 在 models 目录下")
                return

        try:
            self.param_text.setPlainText(MSG_DETECTING)
            QApplication.processEvents()

            # 执行检测
            result = self.detector.detect(self.current_image)

            # 显示检测结果图像
            result_image = self.detector.draw_result(self.current_image, result)
            self.display_image(result_image, self.result_label)

            # 更新状态显示
            if result.fatigue_level == "正常":
                color = self.ui_color.status_normal
            elif result.fatigue_level == "疲劳":
                color = self.ui_color.status_fatigue
            else:
                color = self.ui_color.accent_orange

            self.status_display.setText(f"{result.fatigue_level}")
            self.status_display.setStyleSheet(f"""
                color: {color}; font-size: 28px; font-weight: bold;
                background-color: #fff; border: 2px solid {color};
                border-radius: 4px; padding: 8px;
            """)

            # 更新检测结果详情
            det_text = ""
            # 检测目标
            if result.detections:
                name_to_id = {v: k for k, v in self.detector.detector.class_names.items()}
                targets = []
                for cls_name, conf, bbox in result.detections:
                    cls_id = name_to_id.get(cls_name, -1)
                    cn_name = CLASS_NAMES_CN.get(cls_id, cls_name)
                    targets.append(f"{cn_name}({conf:.2f})")
                det_text += "检测目标: " + ", ".join(targets[:4])
                if len(targets) > 4:
                    det_text += f" ...共{len(targets)}个"
                det_text += "\n"
            else:
                det_text += "检测目标: 无\n"

            # EFV / MFV
            thr = FatigueThreshold()
            det_text += f"EFV: {result.efv:.4f}  MFV: {result.mfv:.4f}\n"
            pitch, yaw, roll = result.head_pose
            det_text += f"头部姿态: pitch={pitch:.1f} yaw={yaw:.1f} roll={roll:.1f}\n"
            det_text += f"眼部疲劳: {'是' if result.is_eye_fatigue else '否'}\n"
            det_text += f"嘴部疲劳: {'是' if result.is_mouth_fatigue else '否'}"
            self.param_text.setPlainText(det_text)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"检测失败: {str(e)}")

    def display_image(self, image, label):
        """在QLabel上显示OpenCV图像"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(scaled)
        label.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        """窗口缩放时自适应图片"""
        super().resizeEvent(event)
        if self.current_image is not None:
            self.display_image(self.current_image, self.original_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())