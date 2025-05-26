"""
文件助手 - 文檔 OCR 處理工具

此模組是應用的主入口點，負責初始化並啟動應用。
"""
import logging
import os
from pathlib import Path

from nicegui import app, ui

from src.config import settings
from src.ui.main_ui import MainUI
from src.utils.file_utils import clear_upload_directory

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 設置日誌級別
logging.getLogger('docling').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# 初始化應用
main_ui = MainUI()
app.on_startup(main_ui.init_ui)

# 添加靜態文件目錄
app.add_static_files('/temp_uploads', str(settings.UPLOAD_DIR))
# 清空上傳目錄
clear_upload_directory()

if __name__ in ["__main__", "__mp_main__"]:
    ui.run(
        title="Document Assistant",
        host="0.0.0.0",
        port=8080,
        reload=True,
        show=False
    )
