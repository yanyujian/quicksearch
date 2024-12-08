from pathlib import Path
import pandas as pd
from typing import Dict, List, Optional

class ExcelDataManager:
    def __init__(self, excel_file: Path):
        self.excel_file = excel_file
        self.data_cache: Dict[str, pd.DataFrame] = {}
        self.load_excel()
    
    def load_excel(self) -> None:
        """加载Excel文件到缓存"""
        try:
            # 读取所有sheet页
            excel = pd.ExcelFile(self.excel_file)
            for sheet_name in excel.sheet_names:
                df = pd.read_excel(excel, sheet_name)
                if len(df.columns) >= 2:  # 确保至少有两列
                    # 只保留前两列，并设置列名
                    df = df.iloc[:, :2]
                    df.columns = ['keyword', 'content']
                    self.data_cache[sheet_name] = df
        except Exception as e:
            raise Exception(f"Excel文件加载失败: {str(e)}")
    
    def get_sheet_names(self) -> List[str]:
        """获取所有sheet页名称"""
        return list(self.data_cache.keys())
    
    def search(self, sheet_name: str, keyword: str, max_suggestions: int = 10) -> List[Dict]:
        """在指定sheet页中搜索关键词"""
        if sheet_name not in self.data_cache:
            return []
        
        df = self.data_cache[sheet_name]
        # 模糊匹配搜索
        matches = df[df['keyword'].str.contains(keyword, case=False, na=False)]
        results = matches.head(max_suggestions).to_dict('records')
        return results
    
    def get_suggestions(self, sheet_name: str, prefix: str, max_suggestions: int = 10) -> List[str]:
        """获取搜索建议"""
        if sheet_name not in self.data_cache:
            return []
        
        df = self.data_cache[sheet_name]
        matches = df[df['keyword'].str.startswith(prefix, case=False, na=False)]
        suggestions = matches['keyword'].head(max_suggestions).tolist()
        return suggestions 