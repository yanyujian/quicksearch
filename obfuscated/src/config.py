from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# 用户认证配置
DEFAULT_USERNAME = "hy"
DEFAULT_PASSWORD = "hy1235"

# Excel配置
EXCEL_FILE = DATA_DIR / "data.xlsx"

# 搜索配置
MIN_SEARCH_CHARS = 2  # 最小搜索字符数
MAX_SUGGESTIONS = 10  # 最大联想建议数 