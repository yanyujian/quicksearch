from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QTabWidget, QTableWidget, QLineEdit, QPushButton,
                           QFileDialog, QMessageBox, QTableWidgetItem, QHeaderView,
                           QMenuBar, QMenu, QInputDialog, QDialog, QLabel,
                           QApplication, QCheckBox, QWidgetAction)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QClipboard, QFont, QAction, QPainter, QLinearGradient, QColor, QPalette, QActionGroup
import pandas as pd
import os
import json
from src.utils.excel_handler import ExcelHandler
from src.ui.toast import Toast  # 添加导入

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        # 添加作者信息，使用HTML格式使邮箱可点击
        info_text = """
        <h2>Excel智能检索系统</h2>
        <p><b>作者：</b>黄迎老公</p>
        <p><b>联系方式：</b></p>
        <p>邮箱：<a href="mailto:183722847@qq.com">183722847@qq.com</a></p>
        <p>微信：fzlzili</p>
        """
        
        info_label = QLabel(info_text)
        info_label.setOpenExternalLinks(True)  # 允许打开外部链接
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(info_label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel智能检索系统")
        
        # 初始化类属性
        self.search_inputs = {}
        self.search_input_used = {}  # 添加一个字典来记录搜索框是否被使用过
        self.excel_handler = ExcelHandler()
        
        # 加载配置
        self.config = self.load_config()
        
        # 设置窗口最小尺寸，保持16:9的比例
        self.setMinimumSize(300, int(300 * 9/16))
        
        # 设置全局字体和样式
        app = QApplication.instance()
        self.current_font_size = self.config.get('font_size', 12)
        default_font = QFont('Microsoft YaHei', self.current_font_size)
        app.setFont(default_font)
        
        # 设置窗口背景渐变色
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#f6f8fa"))
        gradient.setColorAt(1.0, QColor("#e9ecef"))
        palette.setBrush(QPalette.ColorRole.Window, gradient)
        self.setPalette(palette)
        
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                border: none;
            }
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a73e8, stop:1 #1557b0);
                color: white;
                border: none;
                padding: 8px;
                font-size: 13px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QMenuBar::item:selected {
                background: rgba(255, 255, 255, 0.1);
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px 8px 20px;
                border-radius: 4px;
                margin: 2px;
                color: #24292e;
            }
            QMenu::item:selected {
                background-color: #f1f8ff;
                color: #1a73e8;
            }
            QTabWidget::pane {
                border: 1px solid #e1e4e8;
                border-radius: 8px;
                background-color: white;
                margin-top: -1px;
            }
            QTabBar::tab {
                background: transparent;
                border: none;
                padding: 12px 20px;
                margin: 0 2px;
                color: #586069;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                color: #1a73e8;
                border-bottom: 2px solid #1a73e8;
                background-color: rgba(26, 115, 232, 0.1);
            }
            QTabBar::tab:hover:!selected {
                color: #24292e;
                background-color: rgba(0, 0, 0, 0.05);
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #e1e4e8;
                border-radius: 8px;
                gridline-color: #f6f8fa;
                selection-background-color: #f1f8ff;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f6f8fa;
            }
            QTableWidget::item:selected {
                background-color: #f1f8ff;
                color: #1a73e8;
            }
            QHeaderView::section {
                background-color: #f6f8fa;
                color: #24292e;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #e1e4e8;
                font-weight: bold;
                font-size: 13px;
            }
            QLineEdit {
                padding: 12px 20px;
                border: 2px solid #e1e4e8;
                border-radius: 25px;
                font-size: 13px;
                background: white;
                selection-background-color: #1a73e8;
            }
            QLineEdit:focus {
                border-color: #1a73e8;
                background: white;
            }
            QLineEdit:hover {
                border-color: #0366d6;
            }
            QScrollBar:vertical {
                border: none;
                background: #f6f8fa;
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #d1d5da;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #959da5;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
            QCheckBox {
                spacing: 8px;
                color: #24292e;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #d1d5da;
            }
            QCheckBox::indicator:checked {
                background-color: #1a73e8;
                border-color: #1a73e8;
            }
            QCheckBox::indicator:hover {
                border-color: #1a73e8;
            }
        """)
        
        # 初始化Toast（移到最前面）
        self.toast = Toast(self)
        
        # 创建菜单栏（包含 top_checkbox）
        self.create_menu_bar()
        
        # 从配置文件恢复窗口状态
        self.restore_window_state()
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.handle_tab_change)
        layout.addWidget(self.tab_widget)
        
        central_widget.setLayout(layout)
        
        # 加载Excel文件
        self.load_default_file()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 设置Excel路径
        set_path_action = QAction('设置Excel路径', self)
        set_path_action.triggered.connect(self.set_excel_path)
        file_menu.addAction(set_path_action)
        
        # 添加分隔线
        file_menu.addSeparator()
        
        # 添加退出按钮
        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut('Ctrl+Q')
        file_menu.addAction(exit_action)
        
        # 窗口菜单
        window_menu = menubar.addMenu('窗口')
        
        # 窗口大小预设
        size_menu = QMenu('窗口大小', self)
        
        # 大窗口 (1280x800)
        large_action = QAction('大', self)
        large_action.triggered.connect(lambda: self.set_window_size('large'))
        size_menu.addAction(large_action)
        
        # 中等窗口 (1024x768)
        medium_action = QAction('中', self)
        medium_action.triggered.connect(lambda: self.set_window_size('medium'))
        size_menu.addAction(medium_action)
        
        # 小窗口 (800x600)
        small_action = QAction('小', self)
        small_action.triggered.connect(lambda: self.set_window_size('small'))
        size_menu.addAction(small_action)
        
        window_menu.addMenu(size_menu)
        window_menu.addSeparator()
        
        # 创建一个QWidget作为菜单项的容器
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(10, 2, 10, 2)
        
        # 创建复选框
        self.top_checkbox = QCheckBox("窗口置顶")
        self.top_checkbox.stateChanged.connect(self.toggle_window_top)
        top_layout.addWidget(self.top_checkbox)
        
        # 创建QWidgetAction
        top_action = QWidgetAction(self)
        top_action.setDefaultWidget(top_widget)
        window_menu.addAction(top_action)
        
        # 设置菜单
        settings_menu = menubar.addMenu('设置')
        
        # 设置字体大小
        font_size_action = QAction('设置字体大小', self)
        font_size_action.triggered.connect(self.set_font_size)
        settings_menu.addAction(font_size_action)
        
        # 添加分隔线
        settings_menu.addSeparator()
        
        # 复制方式子菜单
        copy_menu = QMenu('复制方式', self)
        
        # 创建动作组，使选项互斥
        copy_mode_group = QActionGroup(self)
        copy_mode_group.setExclusive(True)
        
        # 单击复制选项
        self.single_click_action = QAction('单击复制', self)
        self.single_click_action.setCheckable(True)
        self.single_click_action.triggered.connect(lambda: self.set_copy_mode(False))
        copy_mode_group.addAction(self.single_click_action)
        copy_menu.addAction(self.single_click_action)
        
        # 双击复制选项
        self.double_click_action = QAction('双击复制', self)
        self.double_click_action.setCheckable(True)
        self.double_click_action.triggered.connect(lambda: self.set_copy_mode(True))
        copy_mode_group.addAction(self.double_click_action)
        copy_menu.addAction(self.double_click_action)
        
        # 根据配置设置默认选中状态
        is_double_click = self.config.get('double_click_copy', False)  # 默认单击
        self.single_click_action.setChecked(not is_double_click)
        self.double_click_action.setChecked(is_double_click)
        
        settings_menu.addMenu(copy_menu)
        
        # 关于按钮（直接添加到菜单栏）
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        menubar.addAction(about_action)
        
    def load_config(self):
        """加载配置文件"""
        config_path = 'config.json'
        default_config = {
            'excel_path': os.path.join('data', 'data.xlsx'),
            'font_size': 12,
            'window': {
                'pos_x': 100,
                'pos_y': 100,
                'width': 1024,
                'height': 768,
                'is_top': False
            },
            'double_click_copy': False  # 默认为单击复制
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default_config
        except:
            return default_config
            
    def save_config(self):
        """保存配置文件"""
        config_path = 'config.json'
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.warning(self, "警告", f"保存配置文件失败：{str(e)}")
            
    def set_excel_path(self):
        """设置Excel文件路径"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择Excel文件",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_name:
            self.config['excel_path'] = file_name
            self.save_config()
            self.load_default_file()  # 重新加载Excel文件
            
    def set_font_size(self):
        """设置字体大小"""
        size, ok = QInputDialog.getInt(
            self, 
            "设置字体大小",
            "请输入字体大小(8-50):",
            value=self.current_font_size,
            min=8,
            max=50
        )
        
        if ok:
            self.current_font_size = size
            self.config['font_size'] = size
            self.save_config()
            
            # 更新字体
            app = QApplication.instance()
            new_font = QFont('Microsoft YaHei', size)
            app.setFont(new_font)
            
            # 刷新所有标签页
            self.update_tabs()
            
            # 刷新菜单栏
            self.menuBar().setFont(new_font)
            
            # 显示提示
            self.toast.show_message("字体大小已更新")
            
    def show_about(self):
        """显示关于对话框"""
        dialog = AboutDialog(self)
        dialog.exec()
        
    def create_search_bar(self, tab_index):
        """为每个标签页创建搜索框"""
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("输入搜索内容...")
        search_input.textChanged.connect(lambda: self.handle_search(tab_index))
        
        # 设置光标闪烁
        search_input.setCursorPosition(0)  # 设置光标位置到开始
        search_input.setStyleSheet("""
            QLineEdit {
                padding: 5px 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
        """)
        
        # 添加焦点获得事件处理
        def handle_focus_in(event):
            if not self.search_input_used.get(tab_index, False):
                # 如果搜索框未被使用过，只设置焦点
                search_input.setCursorPosition(0)
                self.search_input_used[tab_index] = True
            else:
                # 如果搜索框被使用过，全选文本
                search_input.selectAll()
            
        search_input.focusInEvent = handle_focus_in
        
        # 设置搜索框样式
        search_input.setMinimumHeight(40)
        search_layout.addWidget(search_input)
        return search_layout, search_input
        
    def load_default_file(self):
        """加载默认的Excel文件"""
        default_file = self.config.get('excel_path', os.path.join('data', 'data.xlsx'))
        try:
            self.excel_handler.load_file(default_file)
            self.update_tabs()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开文件：{str(e)}")
                
    def update_tabs(self):
        # 清除现有标签页
        self.tab_widget.clear()
        self.search_inputs.clear()
        
        # 为每个工作表创建新的标签页
        for sheet_index, (sheet_name, df) in enumerate(self.excel_handler.sheets.items()):
            # 创建容器widget和布局
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setSpacing(10)
            
            # 创建并添加搜索框
            search_layout, search_input = self.create_search_bar(sheet_index)
            container_layout.addLayout(search_layout)
            self.search_inputs[sheet_index] = search_input
            
            # 创建表格
            table_widget = QTableWidget()
            container_layout.addWidget(table_widget)
            
            # 设置表格样式
            table_widget.setStyleSheet("""
                QTableWidget {
                    border: 1px solid #ddd;
                    gridline-color: #ddd;
                }
                QTableWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #eee;
                }
                QTableWidget::item:selected {
                    background-color: #0078d4;
                    color: white;
                }
                QHeaderView::section {
                    background-color: #f5f5f5;
                    padding: 8px 5px;
                    border: 1px solid #ddd;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            
            # 允许自动换行
            table_widget.setWordWrap(True)
            
            # 设置表格列数和固定标题
            table_widget.setColumnCount(2)  # 固定为2列
            table_widget.setHorizontalHeaderLabels(['标签', '提示语'])
            
            # 设置表头样式
            header = table_widget.horizontalHeader()
            header.setStyleSheet("""
                QHeaderView::section {
                    background-color: #f5f5f5;
                    padding: 8px 5px;
                    border: 1px solid #ddd;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            
            # 设置列宽
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # 标签列
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # 提示语列
            
            # 填充数据（添加容错处理）
            table_widget.setRowCount(len(df))
            for i, row in df.iterrows():
                # 处理第一列（标签）
                if len(df.columns) > 0:
                    value = str(row.iloc[0]) if not pd.isna(row.iloc[0]) else ""
                    item = QTableWidgetItem(value)
                else:
                    item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                table_widget.setItem(i, 0, item)
                
                # 处理第二列（提示语）
                if len(df.columns) > 1:
                    value = str(row.iloc[1]) if not pd.isna(row.iloc[1]) else ""
                else:
                    # 如果只有一列，将第一列的内容作为提示语
                    value = str(row.iloc[0]) if not pd.isna(row.iloc[0]) else ""
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                table_widget.setItem(i, 1, item)
                
                # 自动调整行高以适应内容
                table_widget.resizeRowToContents(i)
            
            # 设置最小行高
            table_widget.verticalHeader().setMinimumSectionSize(40)
            
            # 添加点击事件
            if self.config.get('double_click_copy', True):
                # 双击复制模式
                table_widget.cellDoubleClicked.connect(
                    lambda row, col: self.handle_cell_copy(row, col)
                    if col == 1 else None
                )
            else:
                # 单击复制模式
                table_widget.cellClicked.connect(
                    lambda row, col: self.handle_cell_copy(row, col)
                    if col == 1 else None
                )
            
            self.tab_widget.addTab(container, sheet_name)
            
    def handle_search(self, tab_index):
        """处理搜索"""
        # 标记搜索框已被使用
        self.search_input_used[tab_index] = True
        
        if tab_index != self.tab_widget.currentIndex():
            return
        
        search_text = self.search_inputs[tab_index].text().lower()
        container = self.tab_widget.widget(tab_index)
        table_widget = container.findChild(QTableWidget)
        
        if not search_text:
            # 显示所有行
            for row in range(table_widget.rowCount()):
                table_widget.setRowHidden(row, False)
            return
            
        # 在当前标签页中搜索
        for row in range(table_widget.rowCount()):
            # 只检查第一列（标签）
            item = table_widget.item(row, 0)
            row_visible = bool(item and search_text in item.text().lower())
            table_widget.setRowHidden(row, not row_visible)
            
    def handle_tab_change(self, index):
        """处理标签页切换"""
        if index in self.search_inputs:
            self.search_inputs[index].setFocus()
            # 只有在搜索框被使用过的情况下才全选文本
            if self.search_input_used.get(index, False):
                self.search_inputs[index].selectAll()
            
    def handle_cell_copy(self, row, col):
        """处理单元格复制事件"""
        current_tab = self.tab_widget.currentWidget()
        table_widget = current_tab.findChild(QTableWidget)
        item = table_widget.item(row, col)
        if item:
            # 设置选中状态
            table_widget.setCurrentItem(item)
            item.setSelected(True)
            
            # 将文本复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(item.text())
            
            # 确保 Toast 显示在最上层
            self.toast.setParent(None)
            self.toast.setParent(self)
            self.toast.show_message("已复制到剪贴板")
        
    def restore_window_state(self):
        """恢复窗口状态"""
        window_config = self.config.get('window', {})
        
        # 恢复窗口位置和大小
        x = window_config.get('pos_x', 100)
        y = window_config.get('pos_y', 100)
        width = window_config.get('width', 1024)
        height = window_config.get('height', 768)
        
        self.setGeometry(x, y, width, height)
        
        # 恢复置顶状态
        is_top = window_config.get('is_top', False)
        if is_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.top_checkbox.setChecked(True)
            
    def save_window_state(self):
        """保存窗口状态"""
        self.config['window'] = {
            'pos_x': self.x(),
            'pos_y': self.y(),
            'width': self.width(),
            'height': self.height(),
            'is_top': self.top_checkbox.isChecked()
        }
        self.save_config()
        
    def moveEvent(self, event):
        """窗口移动事件"""
        super().moveEvent(event)
        self.save_window_state()
        
    def resizeEvent(self, event):
        """窗口大小��变事件"""
        super().resizeEvent(event)
        self.save_window_state()
        
    def toggle_window_top(self, state):
        """切换窗口置顶状态"""
        if state == Qt.CheckState.Checked.value:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.toast.show_message("窗口已置顶")
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            self.toast.show_message("取消置顶")
        self.show()
        self.save_window_state()  # 保存置顶状态
        
    def set_window_size(self, size):
        """设置预定义的窗口大小"""
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen().geometry()
        
        # 预设尺寸（宽x高）
        sizes = {
            'large': (1280, 800),
            'medium': (1024, 768),
            'small': (800, 600)
        }
        
        if size in sizes:
            width, height = sizes[size]
            
            # 确保窗口不会超出屏幕
            width = min(width, screen.width())
            height = min(height, screen.height())
            
            # 计算居中位置
            x = (screen.width() - width) // 2
            y = (screen.height() - height) // 2
            
            # 设置窗口大小和位置
            self.setGeometry(x, y, width, height)
            
            # 保存配置
            self.save_window_state()
            
            # 显示提示
            self.toast.show_message(f"已调整为{size}窗口")
        
    def set_copy_mode(self, is_double_click):
        """设置复制模式"""
        self.config['double_click_copy'] = is_double_click
        self.save_config()
        self.update_tabs()  # 重新创建表格以更新事件绑定
        mode_text = "双击" if is_double_click else "单击"
        self.toast.show_message(f"已切换为{mode_text}复制模式")