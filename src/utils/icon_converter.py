from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path, sizes=None):
    """
    将PNG图片转换为ICO文件
    
    Args:
        png_path: PNG文件路径
        ico_path: 输出的ICO文件路径
        sizes: 需要的图标尺寸列表，默认为[16, 32, 48, 64, 128, 256]
    """
    if sizes is None:
        sizes = [16, 32, 48, 64, 128, 256]
    
    try:
        # 打开PNG图片
        img = Image.open(png_path)
        
        # 转换为RGBA模式（如果不是的话）
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建不同尺寸的图标
        icon_sizes = []
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            icon_sizes.append(resized)
        
        # 保存为ICO文件
        icon_sizes[0].save(
            ico_path,
            format='ICO',
            sizes=[(size, size) for size in sizes],
            append_images=icon_sizes[1:]
        )
        return True
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return False 