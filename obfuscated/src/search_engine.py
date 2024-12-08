from typing import List, Dict
from .data_manager import ExcelDataManager

class SearchEngine:
    def __init__(self, data_manager: ExcelDataManager):
        self.data_manager = data_manager
    
    def search(self, sheet_name: str, keyword: str, max_results: int = 10) -> List[Dict]:
        """执行搜索"""
        if not keyword:
            return []
        return self.data_manager.search(sheet_name, keyword, max_results)
    
    def get_suggestions(self, sheet_name: str, prefix: str, max_suggestions: int = 10) -> List[str]:
        """获取搜索建议"""
        if not prefix or len(prefix) < 2:
            return []
        return self.data_manager.get_suggestions(sheet_name, prefix, max_suggestions) 