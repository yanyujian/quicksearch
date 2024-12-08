import sys
import traceback
from datetime import datetime

def log_error(error_msg):
    """记录错误信息到文件"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}]\n")
            f.write(error_msg)
            f.write("\n" + "="*50 + "\n")
    except:
        pass

try:
    from src.main import main
    main()
except Exception as e:
    error_msg = f"错误类型: {type(e).__name__}\n"
    error_msg += f"错误信息: {str(e)}\n"
    error_msg += "详细堆栈:\n"
    error_msg += traceback.format_exc()
    
    # 记录错误到文件
    log_error(error_msg)
    
    # 打印错误信息
    print("\n" + "="*50)
    print("程序运行出错:")
    print(error_msg)
    print("错误信息已保存到 error.log")
    print("="*50 + "\n")
    
    # 等待用户确认
    input("按回车键退出...")
    sys.exit(1) 