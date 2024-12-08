import gradio as gr
from typing import Dict, List
from .config import DEFAULT_USERNAME, DEFAULT_PASSWORD
from .search_engine import SearchEngine

class UI:
    def __init__(self, search_engine: SearchEngine):
        self.search_engine = search_engine
        self.sheet_names = search_engine.data_manager.get_sheet_names()
    
    def check_login(self, username: str, password: str) -> bool:
        """验证登录"""
        return username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD
    
    def create_interface(self) -> gr.Blocks:
        """创建Gradio界面"""
        with gr.Blocks(title="Excel智能检索系统", css="""
            #login-container { 
                max-width: 300px; 
                margin: 200px auto;
                padding: 20px;
                border: 1px solid #eee;
                border-radius: 8px;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            #login-title { 
                text-align: center; 
                margin-bottom: 20px;
                color: #333;
                font-size: 18px;
            }
            .result-row {
                display: flex;
                padding: 12px;
                margin: 8px 0;
                border: 1px solid #eee;
                border-radius: 4px;
            }
            .result-keyword {
                flex: 0 0 150px;
                font-weight: bold;
                padding-right: 16px;
                border-right: 1px solid #eee;
            }
            .result-content {
                flex: 1;
                padding-left: 16px;
            }
        """) as interface:
            # 登录界面
            with gr.Column(visible=True, elem_id="login-container") as login_interface:
                gr.Markdown("Excel智能检索系统", elem_id="login-title")
                username = gr.Textbox(label="用户名", placeholder="请输入用户名", container=False)
                password = gr.Textbox(label="密码", type="password", placeholder="请输入密码", container=False)
                login_button = gr.Button("登录", variant="primary", size="sm")

            # 主界面
            with gr.Column(visible=False) as main_interface:
                with gr.Tabs() as tabs:
                    for sheet_name in self.sheet_names:
                        with gr.TabItem(label=sheet_name):
                            search_input = gr.Textbox(
                                label="搜索关键词",
                                placeholder=f"在 {sheet_name} 中搜索...",
                                show_label=False
                            )
                            results = gr.HTML(value="", label="搜索结果")

                            def create_search_fn(sheet):
                                def search_fn(keyword):
                                    if not keyword or not keyword.strip():
                                        return ""
                                    
                                    search_results = self.search_engine.search(sheet, keyword.strip())
                                    if not search_results:
                                        return "<div>无搜索结果</div>"
                                    
                                    html_results = ["<div class='search-results'>"]
                                    for r in search_results:
                                        keyword = r['keyword'].replace('<', '&lt;').replace('>', '&gt;')
                                        content = r['content'].replace('<', '&lt;').replace('>', '&gt;')
                                        html_results.append(f"""
                                            <div class='result-row'>
                                                <div class='result-keyword'>{keyword}</div>
                                                <div class='result-content'>{content}</div>
                                            </div>
                                        """)
                                    html_results.append("</div>")
                                    
                                    return "".join(html_results)
                                return search_fn

                            # 绑定搜索事件
                            search_input.change(
                                create_search_fn(sheet_name),
                                inputs=[search_input],
                                outputs=[results]
                            )

            # 登录逻辑
            def login(username, password):
                if self.check_login(username, password):
                    return {
                        login_interface: gr.Column(visible=False),
                        main_interface: gr.Column(visible=True)
                    }
                return {
                    login_interface: gr.Column(visible=True),
                    main_interface: gr.Column(visible=False)
                }

            # 绑定登录事件
            login_button.click(
                login,
                inputs=[username, password],
                outputs=[login_interface, main_interface]
            )

        return interface 