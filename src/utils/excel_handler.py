import pandas as pd
from typing import Dict

class ExcelHandler:
    def __init__(self):
        self.sheets: Dict[str, pd.DataFrame] = {}
        self.current_file: str = ""
        
    def load_file(self, file_path: str) -> None:
        """加载Excel文件并存储所有工作表"""
        try:
            excel_file = pd.ExcelFile(file_path)
            self.sheets = {
                sheet_name: pd.read_excel(excel_file, sheet_name=sheet_name)
                for sheet_name in excel_file.sheet_names
            }
            self.current_file = file_path
        except Exception as e:
            raise Exception(f"加载Excel文件失败: {str(e)}")
            
    def search_in_sheet(self, sheet_name: str, search_text: str) -> pd.DataFrame:
        """在指定工作表中搜索内容"""
        if sheet_name not in self.sheets:
            return pd.DataFrame()
            
        df = self.sheets[sheet_name]
        mask = df.astype(str).apply(
            lambda x: x.str.contains(search_text, case=False, na=False)
        ).any(axis=1)
        
        return df[mask] 