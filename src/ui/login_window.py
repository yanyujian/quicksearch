from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from src.ui.main_window import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel智能检索系统 - 登录")
        self.setFixedSize(400, 300)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # 添加标题
        title = QLabel("Excel智能检索系统")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # 用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.username_input.returnPressed.connect(self.handle_return_pressed)
        layout.addWidget(self.username_input)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.handle_return_pressed)
        layout.addWidget(self.password_input)
        
        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        central_widget.setLayout(layout)
        
    def handle_return_pressed(self):
        """处理回车键事件"""
        self.login_button.click()  # 模拟点击登录按钮
        
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "admin" and password == "admin123":
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "错误", "用户名或密码错误！") 