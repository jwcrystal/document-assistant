"""
文件處理工具函數

此模組提供處理文件的工具函數，包括文件上傳、下載和預覽等功能。
"""
import os
import re
import unicodedata
from pathlib import Path
from typing import Optional, Tuple

from nicegui import ui

from src.config import settings


def sanitize_filename(filename: str) -> str:
    """
    將檔名標準化，移除特殊字元和空格
    
    Args:
        filename (str): 原始檔名
        
    Returns:
        str: 標準化後的檔名
    """
    # 使用 NFKD 標準化並編碼為 UTF-8，忽略無法處理的字元
    normalized = unicodedata.normalize('NFKD', filename).encode('utf-8', 'ignore').decode('utf-8')
    sanitized = normalized.replace(" ", "_")
    # 移除所有非字母、數字、底線、連字號和點的字元
    sanitized = re.sub(r'[^\w.-]', '', sanitized)
    return sanitized


def save_uploaded_file(uploaded_file) -> Tuple[Optional[Path], Optional[str]]:
    """
    保存上傳的文件到臨時目錄
    
    Args:
        uploaded_file: 上傳的文件對象
        
    Returns:
        Tuple[Optional[Path], Optional[str]]: (文件路徑, 錯誤訊息)
    """
    if not uploaded_file.content:
        return None, "未選擇文件"
    
    try:
        # 檢查檔案大小
        file_size = len(uploaded_file.content.read())
        uploaded_file.content.seek(0)  # 重置文件指針
        
        if file_size > settings.MAX_FILE_SIZE:
            return None, f"檔案大小超過限制 (最大 {settings.MAX_FILE_SIZE/1_000_000}MB)"
        
        # 檢查文件類型
        if uploaded_file.type not in settings.SUPPORTED_FILE_TYPES:
            return None, "不支援的文件類型"

        # 生成安全檔名
        file_name = uploaded_file.name
        safe_name = sanitize_filename(file_name)
        file_path = settings.UPLOAD_DIR / safe_name
        
        # 保存文件
        with open(file_path, 'wb') as f:
            uploaded_file.content.seek(0)
            f.write(uploaded_file.content.read())
            
        return file_path, None
        
    except Exception as e:
        return None, f"保存文件時發生錯誤: {str(e)}"


def get_file_info(file_path: Path) -> dict:
    """
    獲取文件的基本訊息
    
    Args:
        file_path (Path): 文件路徑
        
    Returns:
        dict: 包含文件訊息的字典
    """
    if not file_path.exists():
        return {}
        
    file_size = file_path.stat().st_size
    file_type = file_path.suffix.lower()
    
    return {
        'name': file_path.name,
        'size': file_size,
        'size_mb': file_size / (1024 * 1024),
        'type': file_type,
        'path': str(file_path)
    }


def clear_upload_directory() -> None:
    """清空上傳目錄"""
    for file in settings.UPLOAD_DIR.glob('*'):
        try:
            if file.is_file():
                file.unlink()
        except Exception as e:
            print(f"無法刪除文件 {file}: {e}")


def is_supported_file_type(file_type: str) -> bool:
    """
    檢查文件類型是否受支援
    
    Args:
        file_type (str): 文件 MIME 類型
        
    Returns:
        bool: 如果支援返回 True，否則返回 False
    """
    return file_type in settings.SUPPORTED_IMAGE_TYPES + settings.SUPPORTED_FILE_TYPES
