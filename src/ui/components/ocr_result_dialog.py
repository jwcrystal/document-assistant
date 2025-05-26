"""
OCR 結果對話框組件

此模組提供顯示 OCR 處理結果的對話框組件。
"""
import os
import time
from pathlib import Path
from typing import Optional, Callable, Dict, Any

from nicegui import ui

from src.config import settings


class OCRResultDialog:
    """OCR 結果對話框"""
    
    def __init__(self, original_filename: str):
        """
        初始化 OCR 結果對話框
        
        Args:
            original_filename: 原始文件名
        """
        self.original_filename = original_filename
        self.dialog = None
        self.progress = 0
        self.status = "準備中..."
        self.result_content = ""
        self.is_processing = False
        self.on_cancel = None
        self.on_download = None
    
    def show_processing_dialog(self, on_cancel: Optional[Callable] = None) -> None:
        """
        顯示處理中的對話框
        
        Args:
            on_cancel: 取消按鈕的回調函數
        """
        self.on_cancel = on_cancel
        self.is_processing = True
        
        with ui.dialog() as self.dialog, ui.card().classes('w-full max-w-2xl'):
            with ui.column().classes('w-full items-stretch'):
                ui.label('OCR 處理中...').classes('text-h6')
                ui.linear_progress().bind_value(self, 'progress')
                ui.label().bind_text_from(self, 'status')
                
                with ui.row().classes('w-full justify-end'):
                    ui.button('取消', on_click=self._handle_cancel, color='negative')
        
        self.dialog.open()
    
    def update_progress(self, progress: int, status: str) -> None:
        """
        更新處理進度
        
        Args:
            progress: 進度百分比 (0-100)
            status: 狀態訊息
        """
        self.progress = progress
        self.status = status
        ui.update(self.dialog)
    
    def show_result(self, content: str, on_download: Optional[Callable] = None) -> None:
        """
        顯示處理結果
        
        Args:
            content: 處理結果內容
            on_download: 下載按鈕的回調函數
        """
        self.is_processing = False
        self.result_content = content
        self.on_download = on_download
        
        # 關閉處理中的對話框
        if self.dialog:
            self.dialog.close()
        
        # 顯示結果對話框
        with ui.dialog() as self.dialog, ui.card().classes('w-full max-w-6xl'):
            with ui.column().classes('w-full h-[70vh]'):
                # 標題和工具欄
                with ui.row().classes('w-full items-center justify-between'):
                    ui.label('OCR 處理結果').classes('text-h6')
                    with ui.row():
                        # ui.button('複製到剪貼板', on_click=lambda: self._copy_to_clipboard(), 
                        #          icon='content_copy').props('flat')
                        ui.button('下載', on_click=lambda: self._handle_download(), 
                                 icon='download').props('flat color=primary')
                
                # 內容區域
                with ui.scroll_area().classes('w-full flex-grow border rounded'):
                    self.content_display = ui.markdown(content).classes('p-4')
                
                # 底部按鈕
                with ui.row().classes('w-full justify-end'):
                    ui.button('關閉', on_click=self.dialog.close, color='primary')
        
        self.dialog.open()
    
    def show_error(self, error_message: str) -> None:
        """
        顯示錯誤訊息
        
        Args:
            error_message: 錯誤訊息
        """
        self.is_processing = False
        
        # 關閉處理中的對話框
        if self.dialog:
            self.dialog.close()
        
        # 顯示錯誤對話框
        with ui.dialog() as self.dialog, ui.card().classes('w-full max-w-2xl'):
            with ui.column().classes('w-full items-center text-center'):
                ui.icon('error', color='red', size='48px')
                ui.label('處理出錯').classes('text-h6')
                ui.label(error_message).classes('text-body1')
                
                with ui.row().classes('w-full justify-end'):
                    ui.button('關閉', on_click=self.dialog.close, color='primary')
        
        self.dialog.open()
    
    def _handle_cancel(self) -> None:
        """處理取消按鈕點擊"""
        if self.on_cancel:
            self.on_cancel(self.dialog)
        if self.dialog:
            self.dialog.close()
    
    async def _handle_download(self) -> None:
        """處理下載按鈕點擊"""
        if self.on_download:
            await self.on_download(self.result_content, self.original_filename)
    
    async def _copy_to_clipboard(self) -> None:
        """複製內容到剪貼板"""
        try:
            # 使用更可靠的 JavaScript 實現剪貼簿功能
            js = f"""
            try {{
                const content = {self.result_content!r};
                // 創建一個不可見的 textarea 元素
                const textarea = document.createElement('textarea');
                textarea.value = content;
                // 設置樣式確保元素不可見
                textarea.style.position = 'fixed';
                textarea.style.left = '0';
                textarea.style.top = '0';
                textarea.style.opacity = '0';
                // 將 textarea 添加到文檔中
                document.body.appendChild(textarea);
                // 選擇所有文本
                textarea.select();
                textarea.setSelectionRange(0, 99999); // 確保選擇所有內容
                // 執行複製命令
                const success = document.execCommand('copy');
                // 清理
                document.body.removeChild(textarea);
                return success;
            }} catch (e) {{
                console.error('複製到剪貼板錯誤:', e);
                return false;
            }}
            """
            
            # 執行 JavaScript 並顯示結果
            success = ui.run_javascript(js)
            
            if success:
                ui.notify('已複製到剪貼板', type='positive')
            else:
                ui.notify('複製到剪貼板失敗，請手動複製', type='negative')
                
        except Exception as e:
            ui.notify(f'複製到剪貼板時發生錯誤: {str(e)}', type='negative')
