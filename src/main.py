import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from src.ui.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 设置应用程序图标
    icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'icon.ico')
    app.setWindowIcon(QIcon(icon_path))
    
    # 创建并显示登录窗口
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 