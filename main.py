from pathlib import Path
from src.config import EXCEL_FILE
from src.data_manager import ExcelDataManager
from src.search_engine import SearchEngine
from src.ui import UI

def main():
    # 初始化数据管理器
    data_manager = ExcelDataManager(EXCEL_FILE)
    
    # 初始化搜索引擎
    search_engine = SearchEngine(data_manager)
    
    # 创建UI
    ui = UI(search_engine)
    interface = ui.create_interface()
    
    # 启动应用
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
    )

if __name__ == "__main__":
    main() 