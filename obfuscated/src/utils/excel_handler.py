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
            self.sheets = {}
            
            for sheet_name in excel_file.sheet_names:
                # 读取工作表
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                
                # 处理列数
                if len(df.columns) == 0:
                    # 如果没有列，创建两个空列
                    df = pd.DataFrame(columns=['标签', '提示语'])
                elif len(df.columns) == 1:
                    # 如果只有一列，将其作为提示语，添加空的标签列
                    df.columns = ['提示语']
                    df.insert(0, '标签', '')
                else:
                    # 如果有多列，只取前两列
                    df = df.iloc[:, :2]
                    df.columns = ['标签', '提示语']
                
                # 处理空值
                df = df.fillna('')
                
                self.sheets[sheet_name] = df
                
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