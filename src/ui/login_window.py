from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QLineEdit, QPushButton, QLabel, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPalette, QFont
from src.ui.main_window import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel智能检索系统 - 登录")
        self.setFixedSize(400, 450)
        
        # 设置窗口背景渐变色
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#ffffff"))
        gradient.setColorAt(1.0, QColor("#f8f9fa"))
        palette.setBrush(QPalette.ColorRole.Window, gradient)
        self.setPalette(palette)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 30, 50, 30)
        
        # 添加Logo标题
        title = QLabel("Excel智能检索系统")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #1a73e8;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        layout.addWidget(title)
        
        # 添加副标题
        subtitle = QLabel("欢迎使用")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: #5f6368;
                font-size: 16px;
                margin-bottom: 15px;
            }
        """)
        layout.addWidget(subtitle)
        
        # 用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.username_input.returnPressed.connect(self.handle_return_pressed)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 20px;
                border: 2px solid #e1e4e8;
                border-radius: 25px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #1a73e8;
                background: white;
            }
            QLineEdit:hover {
                border-color: #0366d6;
            }
        """)
        layout.addWidget(self.username_input)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.handle_return_pressed)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        layout.addWidget(self.password_input)
        
        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a73e8, stop:1 #1557b0);
                border: none;
                border-radius: 25px;
                color: white;
                font-size: 15px;
                font-weight: bold;
                margin-top: 10px;
                min-height: 40px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1557b0, stop:1 #1a73e8);
            }
            QPushButton:pressed {
                background: #1557b0;
            }
        """)
        layout.addWidget(self.login_button)
        
        # 添加联系作者链接
        contact_link = QLabel("<a href='#' style='text-decoration: none;'>联系作者</a>")
        contact_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contact_link.setOpenExternalLinks(False)
        contact_link.linkActivated.connect(self.show_contact)
        contact_link.setStyleSheet("""
            QLabel {
                color: #1a73e8;
                font-size: 12px;
                margin-top: 10px;
            }
            QLabel:hover {
                color: #1557b0;
            }
        """)
        layout.addWidget(contact_link)
        
        # 添加版权信息
        copyright = QLabel("© 2024 Excel智能检索系统")
        copyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright.setStyleSheet("""
            QLabel {
                color: #5f6368;
                font-size: 12px;
                margin-top: 5px;
                opacity: 0.8;
            }
        """)
        layout.addWidget(copyright)
        
        central_widget.setLayout(layout)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
                border: 1px solid #e1e4e8;
                border-radius: 10px;
            }
        """)
        
    def handle_return_pressed(self):
        """处理回车键事件"""
        self.login_button.click()
        
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "hy" and password == "hy1235":
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(
                self, 
                "错误", 
                "用户名或密码错误！",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            ) 
        
    def show_contact(self):
        """显示联系方式对话框"""
        contact_dialog = QDialog(self)
        contact_dialog.setWindowTitle("联系作者")
        contact_dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加联系信息
        info_text = QLabel("""
            <p style='margin-bottom: 10px;'><b>邮箱：</b><a href='mailto:183722847@qq.com'>183722847@qq.com</a></p>
            <p><b>微信：</b>fzlzili</p>
        """)
        info_text.setOpenExternalLinks(True)  # 允许点击邮箱链接
        info_text.setTextFormat(Qt.TextFormat.RichText)
        
        layout.addWidget(info_text)
        
        # 添加确定按钮
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(contact_dialog.accept)
        ok_button.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background: #1a73e8;
                border: none;
                border-radius: 4px;
                color: white;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #1557b0;
            }
        """)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        contact_dialog.setLayout(layout)
        contact_dialog.exec() 