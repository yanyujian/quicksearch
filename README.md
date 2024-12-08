# Excel智能检索系统

## 项目简介
一个轻量级的单机Excel智能检索工具，基于PyQt6开发，支持多页签查询和智能联想功能。本系统专门设计用于快速检索和复制Excel中的数据，特别适合需要频繁查询参考数据的场景。

## 功能特点
- 多Tab页面对应Excel页签
- 智能实时搜索
- 双击快速复制
- 窗口位置记忆
- 字体大小自定义
- 窗口置顶功能
- 简单登录验证
- 美观的桌面GUI界面

## 数据格式说明
Excel文件要求：
- 文件默认位置：data/data.xlsx
- 可包含多个工作表（页签）
- 每个工作表的数据格式：
  - 第一列：标签（可选）
  - 第二列：提示语（支持双击复制）
  - 如果只有一列数据，将作为提示语显示
  - 如果有更多列，只读取前两列
- 数据从第一行开始，无需表头

## 技术栈
- Python 3.8+
- PyQt6
- Pandas
- SQLite

## 安装说明

### 环境要求
- Python 3.8或更高版本
- pip包管理器

### 安装步骤
1. 克隆项目
2. 安装依赖: `pip install -r requirements.txt`
3. 运行程序: `python src/main.py`

## 默认登录信息
- 用户名：admin
- 密码：admin123

## 使用说明

### 基本操作
1. 使用默认账号密码登录
2. 程序自动加载 data/data.xlsx 文件
3. 在搜索框输入关键字进行实时搜索
4. 双击提示语可快速复制到剪贴板

### 高级功能
1. 窗口管理
   - 窗口位置和大小会自动保存
   - 可以通过窗口菜单设置窗口置顶
   - 支持最小宽度300px的紧凑显示

2. 搜索功能
   - 支持实时搜索
   - 每个标签页有独立的搜索框
   - 切换标签页时自动聚焦搜索框
   - 搜索框获得焦点时自动全选

3. 数据操作
   - 双击提示语列可快速复制
   - 复制时显示轻量级提示
   - 表格自动调整列宽

4. 个性化设置
   - 可调整字体大小(8-50)
   - 可修改Excel文件路径
   - 所有设置自动保存

### 配置文件说明
配置文件 (config.json) 保存以下信息：
- Excel文件路径
- 字体大小
- 窗口位置和大小
- 窗口置顶状态

所有配置在修改后自动保存，下次启动时自动恢复。

## 联系方式
- 作者：黄迎老公
- 邮箱：183722847@qq.com
- 微信：fzlzili

## 注意事项
1. 这是一个单机版应用，登录功能仅作为基础访问控制使用
2. 确保Excel文件格式符合要求
3. 建议将常用数据放在前几列以获得最佳显示效果

## 更新日志
### v1.0.0
- 初始版本发布
- 支持基础的Excel文件检索功能
- 实现窗口状态保存
- 添加置顶功能
- 优化用户界面