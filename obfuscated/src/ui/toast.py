from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt6.QtGui import QColor, QPainter

class Toast(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置样式
        self.setStyleSheet("""
            QLabel {
                color: #ff0000;  /* 红色文字 */
                padding: 12px 30px;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.95);
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #cccccc;
            }
        """)
        
        # 设置窗口标志，确保显示在最上层
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                          Qt.WindowType.SubWindow |
                          Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 初始化计时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.hide)
        
    def show_message(self, message, duration=500):  # 修改为0.5秒
        """显示消息"""
        self.setText(message)
        self.adjustSize()
        
        # 计算位置（在父窗口中居中偏上）
        parent_rect = self.parent().rect()
        x = (parent_rect.width() - self.width()) // 2
        y = parent_rect.height() // 3
        self.move(x, y)
        
        # 显示并设置定时器
        self.show()
        self.raise_()  # 确保显示在最上层
        self.timer.start(duration)