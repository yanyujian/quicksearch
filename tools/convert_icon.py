import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.icon_converter import convert_png_to_ico

def main():
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 设置默认的输入输出路径
    default_png = os.path.join(project_root, 'resources', 'icon.png')
    default_ico = os.path.join(project_root, 'resources', 'icon.ico')
    
    # 检查resources目录是否存在，不存在则创建
    resources_dir = os.path.join(project_root, 'resources')
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)
    
    print("PNG转ICO工具")
    print("=" * 50)
    
    # 获取输入文件路径
    png_path = input(f"请输入PNG文件路径 (直接回车使用默认路径: {default_png}):\n").strip()
    if not png_path:
        png_path = default_png
    
    # 获取输出文件路径
    ico_path = input(f"请输入ICO文件保存路径 (直接回车使用默认路径: {default_ico}):\n").strip()
    if not ico_path:
        ico_path = default_ico
    
    # 检查输入文件是否存在
    if not os.path.exists(png_path):
        print(f"错误: 找不到PNG文件: {png_path}")
        return
    
    # 检查输入文件是否为PNG
    if not png_path.lower().endswith('.png'):
        print("错误: 输入文件必须是PNG格式")
        return
    
    # 检查输出路径是否有效
    try:
        output_dir = os.path.dirname(ico_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except Exception as e:
        print(f"错误: 无法创建输出目录: {str(e)}")
        return
    
    print("\n开始转换...")
    if convert_png_to_ico(png_path, ico_path):
        print("\n转换完成！")
        print(f"ICO文件已保存到: {ico_path}")
    else:
        print("\n转换失败！")

if __name__ == '__main__':
    main() 