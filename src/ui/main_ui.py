"""
主用戶界面模組

此模組包含應用的主用戶界面。
"""
import os
import logging
from pathlib import Path
from typing import Optional

from nicegui import ui

from src.config import settings
from src.utils.file_utils import save_uploaded_file, get_file_info, sanitize_filename
from src.ui.components.preview import get_preview_handler
from src.ui.components.ocr_result_dialog import OCRResultDialog
from src.services.ocr.ocr_service import ocr_service

# 配置日誌
logger = logging.getLogger(__name__)

class MainUI:
    """主用戶界面類"""
    
    def __init__(self):
        """初始化主界面"""
        self.current_file_path = None
        self.preview_container = None
        self.ocr_dialog = None
    
    async def init_ui(self):
        """初始化用戶界面"""
        # 設置頁面標題和圖標
        ui.page_title("文件助手 - 文檔 OCR 處理工具")
        
        # 添加自定義 CSS 樣式
        self._add_custom_styles()
        
        # 創建主佈局
        with ui.column().classes('w-full items-center p-4'):
            # 左側的 info 按鈕
            # 支援的檔案格式和大小限制
            with ui.button(icon='info', color='primary').classes('q-mr-auto').props('flat dense'):
                with ui.menu() as menu:
                    with ui.card().classes('q-pa-md bg-blue-1'):
                        with ui.column().classes('w-full'):
                            ui.label('📝 支援的檔案格式與限制').classes('text-subtitle2 text-weight-bold')
                            with ui.row().classes('w-full'):
                                ui.label('📷 圖片格式:').classes('text-weight-medium')
                                ui.label('JPEG, PNG, GIF, BMP, TIFF')
                            with ui.row().classes('w-full'):
                                ui.label('📄 文件格式:').classes('text-weight-medium')
                                ui.label('PDF, DOCX, DOC, MD, HTML, PPTX, PPT, XLSX, XLS, CSV')
                            with ui.row().classes('w-full'):
                                ui.label('📏 檔案大小限制:').classes('text-weight-medium')
                                ui.label(f'{int(settings.MAX_FILE_SIZE/1_000_000)} MB')
    
            # 標題區域
            with ui.row().classes('w-full justify-center items-center'):
                ui.icon('description', size='2rem', color='primary')
                ui.label('文件助手').classes('text-h4 text-primary')
            
            ui.label('上傳文件進行 OCR 處理或預覽').classes('text-subtitle1 text-grey-8')
            
            # 上傳區域
            with ui.card().classes('w-full max-w-3xl q-mt-md'):
                with ui.column().classes('w-full items-center'):
                    ui.upload(
                        label='點擊或拖放文件到此處',
                        on_upload=self._handle_upload,
                        max_file_size=settings.MAX_FILE_SIZE
                    ).classes('w-full')
            
            # 預覽區域
            self.preview_container = ui.column().classes('w-full max-w-5xl q-mt-lg')
    
    def _add_custom_styles(self):
        """添加自定義 CSS 樣式"""
        ui.add_head_html('''
            <style>
                :root {
                    --q-primary: #1976D2;
                    --q-secondary: #26A69A;
                    --q-accent: #9C27B0;
                    --q-positive: #21BA45;
                    --q-negative: #C10015;
                    --q-info: #31CCEC;
                    --q-warning: #F2C037;
                }
                
                body {
                    background-color: #f5f5f5;
                    font-family: 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
                }
                
                .q-uploader__file {
                    max-width: 100%;
                }
                
                .preview-container {
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 16px;
                    margin-top: 16px;
                    background-color: white;
                }
                
                .ocr-button {
                    margin-top: 16px;
                }
            </style>
        ''')
    
    async def _handle_upload(self, e):
        """處理文件上傳事件"""
        # 清空預覽區域
        self.preview_container.clear()
        
        # 保存上傳的文件
        file_path, error = save_uploaded_file(e)
        if error:
            ui.notify(error, type='negative')
            return
        
        # 更新當前文件路徑
        self.current_file_path = file_path
        
        # 獲取文件訊息
        file_info = get_file_info(file_path)
        
        # 顯示文件訊息
        with self.preview_container:
            with ui.card().classes('w-full'):
                with ui.column().classes('w-full'):
                    ui.label('文件訊息').classes('text-h6')
                    ui.separator()
                    
                    with ui.grid(columns=2).classes('w-full'):
                        ui.label('文件名:')
                        ui.label(file_info['name'])
                        
                        ui.label('大小:')
                        ui.label(f"{file_info['size_mb']:.2f} MB")
                        
                        ui.label('類型:')
                        ui.label(file_info['type'])
                
                # 添加 OCR 按鈕
                with ui.row().classes('w-full justify-center q-mt-md'):
                    ui.button(
                        '執行 OCR 辨識', 
                        on_click=lambda: self._run_ocr(file_path, file_info['name']),
                        icon='image_search'
                    ).props('color=primary')
                
                # 顯示文件預覽
                ui.separator().classes('q-my-md')
                ui.label('文件預覽').classes('text-h6')
                
                # 根據文件類型顯示預覽
                preview_handler = get_preview_handler(file_path, e.type)
                if preview_handler:
                    await preview_handler.show()
                else:
                    ui.label(f"不支援預覽 {file_info['type']} 類型的文件")
    
    async def _run_ocr(self, file_path: Path, original_filename: str):
        """
        執行 OCR 處理
        
        Args:
            file_path: 文件路徑
            original_filename: 原始文件名
        """
        # 創建 OCR 結果對話框
        self.ocr_dialog = OCRResultDialog(original_filename)
        
        # 顯示處理中的對話框
        self.ocr_dialog.show_processing_dialog(on_cancel=self._cancel_ocr)
        
        # 定義進度回調函數
        async def progress_callback(progress: int, status: str):
            if hasattr(self, 'ocr_dialog') and self.ocr_dialog:
                self.ocr_dialog.update_progress(progress, status)
        
        # 執行 OCR 處理
        try:
            success, message, result = await ocr_service.process_document(
                file_path,
                progress_callback=progress_callback
            )
        except asyncio.CancelledError:
            logger.info("OCR 處理已被取消")
            return
        except Exception as e:
            logger.error(f"OCR 處理出錯: {str(e)}", exc_info=True)
            self.ocr_dialog.show_error(f"處理過程中發生錯誤: {str(e)}")
            return
        
        if success and result:
            # 顯示處理結果
            self.ocr_dialog.show_result(
                content=result if isinstance(result, str) else result.get('content', ''),
                on_download=self._download_markdown
            )
        else:
            # 顯示錯誤訊息
            self.ocr_dialog.show_error(message)
    
    async def _cancel_ocr(self, dialog):
        """取消正在進行的 OCR 處理"""
        await ocr_service.cancel_processing()
        dialog.close()
    
    async def _download_markdown(self, content: str, original_filename: str):
        """
        下載 Markdown 文件
        
        Args:
            content: Markdown 內容
            original_filename: 原始文件名
        """
        try:
            # 生成下載文件名
            base_name = os.path.splitext(original_filename)[0]
            safe_name = sanitize_filename(base_name)
            download_filename = f"{safe_name}_ocr_result.md"
            
            # 確保內容是字節類型
            if isinstance(content, str):
                logger.debug("內容是字符串，進行編碼")
                content_bytes = content.encode('utf-8')
            
            logger.debug(f"內容字節長度: {len(content_bytes) if content_bytes else 0}")
            
            # 使用 JavaScript 處理下載
            js = f"""
            try {{
                // 將 Python 字節轉換為 JavaScript Uint8Array
                const content = new TextDecoder().decode(new Uint8Array({list(content_bytes)}));
                const blob = new Blob([content], {{ type: 'text/markdown;charset=utf-8' }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = '{download_filename}';
                document.body.appendChild(a);
                a.click();
                // 清理
                setTimeout(() => {{
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                }}, 100);
            }} catch (e) {{
                console.error('下載錯誤:', e);
                throw e;
            }}
            """
            ui.run_javascript(js)
            ui.notify(f"已開始下載: {safe_name}", type='positive')
        except Exception as e:
            logger.error(f"下載 Markdown 文件時出錯: {str(e)}", exc_info=True)
            ui.notify(f"下載文件時出錯: {str(e)}", type='negative')
