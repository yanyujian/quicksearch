import sys
import os
# 添加这行来禁用 libpng 警告
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

from PyQt6.QtWidgets import QApplication
from src.ui.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 创建并显示登录窗口
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 