"""
OCR 服務模組

此模組提供文檔 OCR 處理功能。
"""
import asyncio
import logging
from pathlib import Path
from typing import Optional, Callable, Dict, Any, Tuple

from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)

class OCRService:
    """OCR 服務類，處理文檔的 OCR 轉換"""
    
    def __init__(self):
        self.converter = DocumentConverter()
        self.is_processing = False
        self.current_task = None
    
    async def process_document(
        self, 
        file_path: Path, 
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        處理文檔並執行 OCR
        
        Args:
            file_path: 要處理的文件路徑
            progress_callback: 進度回調函數，接收 (進度百分比, 狀態訊息)
            
        Returns:
            Tuple[是否成功, 結果訊息, 處理結果]
        """
        if self.is_processing:
            return False, "已有處理任務正在進行中", None
            
        self.is_processing = True
        
        try:
            # 更新進度
            if progress_callback:
                await progress_callback(10, "正在初始化...")
            
            # 檢查文件是否存在
            if not file_path.exists():
                return False, f"文件不存在: {file_path}", None
            
            # 更新進度
            if progress_callback:
                await progress_callback(30, "正在處理文件...")
            
            try:
                # 執行轉換（在執行器中運行同步代碼）
                logger.info(f"開始處理文件: {file_path}")
                
                # 使用 run_in_executor 執行同步的 convert 方法
                result = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.converter.convert(str(file_path))
                )
                
                logger.info(f"文件處理完成: {file_path}")
                
                # 檢查結果是否有效
                if not result or not hasattr(result, 'document'):
                    return False, "OCR 處理失敗，未返回有效結果", None
                
                # 更新進度
                if progress_callback:
                    await progress_callback(90, "正在生成 Markdown...")
                
                # 導出為 Markdown 格式
                markdown_content = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: result.document.export_to_markdown()
                )
                
                # 更新進度
                if progress_callback:
                    await progress_callback(100, "處理完成")
                
                return True, "OCR 處理成功", markdown_content
                
            except Exception as e:
                logger.error(f"處理文件時發生錯誤: {str(e)}", exc_info=True)
                if progress_callback:
                    await progress_callback(0, f"處理出錯: {str(e)}")
                return False, f"OCR 處理出錯: {str(e)}", None
            
        except Exception as e:
            logger.error(f"OCR 處理出錯: {str(e)}", exc_info=True)
            return False, f"OCR 處理出錯: {str(e)}", None
            
        finally:
            self.is_processing = False
    
    async def cancel_processing(self) -> None:
        """取消正在進行的處理任務"""
        if self.is_processing and self.current_task:
            self.current_task.cancel()
            try:
                await self.current_task
            except asyncio.CancelledError:
                logger.info("OCR 處理已取消")
            self.is_processing = False
    
    async def _run_in_executor(self, func, *args, **kwargs):
        """在執行器中運行同步函數"""
        loop = asyncio.get_running_loop()
        try:
            # 如果是協程，直接等待
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            # 如果是同步函數，使用執行器運行
            self.current_task = loop.run_in_executor(None, lambda: func(*args, **kwargs))
            return await self.current_task
        except asyncio.CancelledError:
            if hasattr(self, 'current_task') and self.current_task:
                self.current_task.cancel()
            raise

# 創建全局 OCR 服務實例
ocr_service = OCRService()
