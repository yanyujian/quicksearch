from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QTabWidget, QTableWidget, QLineEdit, QPushButton,
                           QFileDialog, QMessageBox, QTableWidgetItem, QHeaderView,
                           QMenuBar, QMenu, QInputDialog, QDialog, QLabel,
                           QApplication, QCheckBox, QWidgetAction)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard, QFont, QAction
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
        
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QMenuBar {
                background-color: #f5f5f5;
                border-bottom: 1px solid #ddd;
            }
            QMenuBar::item {
                padding: 5px 10px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
            }
            QMenu::item {
                padding: 5px 30px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 5px 10px;
                min-width: 80px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QWidget {
                background-color: white;
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
        
        # 窗口菜单
        window_menu = menubar.addMenu('窗口')
        
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
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        # 关于
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
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
            }
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
        
        # 设置搜索框样式
        search_input.setMinimumHeight(40)  # 增大搜索框高度
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
        
        # 当获得焦点时全选文本
        search_input.focusInEvent = lambda e: search_input.selectAll()
        
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
                    padding: 5px;
                }
                QHeaderView::section {
                    background-color: #f5f5f5;
                    padding: 5px;
                    border: 1px solid #ddd;
                    font-weight: bold;
                }
            """)
            
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
            
            # 设置行高
            table_widget.verticalHeader().setDefaultSectionSize(40)
            
            # 添加双击事件
            table_widget.cellDoubleClicked.connect(
                lambda row, col: self.handle_cell_double_click(row, col)
                if col == 1 else None  # 只有提示语列（第二列）支持双击复制
            )
            
            self.tab_widget.addTab(container, sheet_name)
            
    def handle_search(self, tab_index):
        """处理搜索"""
        if tab_index != self.tab_widget.currentIndex():
            return
            
        search_text = self.search_inputs[tab_index].text().lower()  # 转换为小写
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
            
        # 添加搜索结果计数
        visible_count = sum(1 for row in range(table_widget.rowCount()) 
                          if not table_widget.isRowHidden(row))
        self.toast.show_message(f"找到 {visible_count} 条匹配结果")
        
    def handle_tab_change(self, index):
        """处理标签页切换"""
        if index in self.search_inputs:
            self.search_inputs[index].setFocus()
            self.search_inputs[index].selectAll()
            
    def handle_cell_double_click(self, row, col):
        """处理单元格双击事件"""
        current_tab = self.tab_widget.currentWidget()
        table_widget = current_tab.findChild(QTableWidget)
        item = table_widget.item(row, col)
        if item:
            # 将文本复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(item.text())
            
            # 确保 Toast 显示在最上层
            self.toast.setParent(None)  # 临时移除父窗口
            self.toast.setParent(self)  # 重新设置父窗口
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
        """窗口大小改变事件"""
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