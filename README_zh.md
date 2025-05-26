# 文件助手

## 專案描述

一個基於 NiceGUI 構建的現代化文件處理應用程序，支援多種文件格式的預覽和 OCR 文字辨識。應用程序提供直觀的用戶介面，用於上傳、預覽文檔，並將文檔內容轉換為可編輯的文字格式。

## 功能特點

- **多格式支援**：PDF、Word (DOCX/DOC)、PowerPoint (PPTX/PPT)、Excel (XLSX/XLS)、圖片 (PNG/JPG/JPEG)、Markdown 和 HTML 文件
- **即時預覽**：即時預覽上傳的文檔
- **OCR 文字辨識**：從圖片和 PDF 中提取文字內容
- **Markdown 輸出**：將辨識結果格式化為 Markdown
- **下載功能**：將處理結果保存為 Markdown 文件
- **響應式設計**：適配不同螢幕尺寸

## 安裝指南

1. **克隆存儲庫**

    ```bash
    git clone <repository_url>
    cd document-assistant
    ```

2. **創建虛擬環境（推薦）**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows 使用 `venv\Scripts\activate`
    ```

3. **安裝依賴**

    ```bash
    pip install -r requirements.txt
    ```

## 使用說明

1. **運行應用程序**

    ```bash
    python -m src.app
    ```

2. 打開網頁瀏覽器，訪問顯示的本地 URL（通常是 `http://localhost:8080`）

3. 點擊「選擇文件」按鈕或將文件拖放到上傳區域

4. 預覽或是辨識文件

## 支援的文件格式

| 文件類型           | 副檔名            | 預覽支援 | OCR 支援 |
| ------------------ | ----------------- | -------- | -------- |
| PDF 文件（純文字） | .pdf              | 是       | 是       |
| Word 文件          | .docx, .doc       | 是       | 是       |
| PowerPoint         | .pptx, .ppt       | 是       | 是       |
| Excel 文件         | .xlsx, .xls       | 是       | 是       |
| CSV 文件           | .csv              | 是       | 是       |
| 圖片文件           | .png, .jpg, .jpeg | 是       | 是       |
| Markdown           | .md, .markdown    | 是       | 是       |
| HTML 文件          | .html, .htm       | 是       | 是       |

## 專案結構

```sh
document-assistant/
├── app.py (old)           # 重構前的主應用程式入口
├── src/                   # 源代碼目錄
│   ├── config/            # 配置相關模組與設定檔
│   ├── services/          # 業務邏輯模組
│   │   └── ocr/           # OCR 相關服務邏輯
│   │       └── ocr_service.py
│   ├── ui/                # 用戶介面模組
│   │   ├── components/    # 可重用的 UI 組件
│   │   │   ├── ocr_result_dialog.py  # OCR 結果顯示對話框
│   │   │   └── preview.py            # 文件預覽組件
│   │   └── main_ui.py     # 主用戶介面程式
│   └── utils/             # 工具函數與輔助模組
│   │   ├── __init__.py
│   │   └── file_utils.py  # 文件處理相關工具函數
│   └── app.py         		 # 主應用程式入口（重構後）
│
├── static/                # 靜態資源（如 CSS、圖片等）
├── temp_uploads/          # 上傳文件的臨時存儲目錄
├── test/                  # 測試程式碼目錄
├── output/                # 輸出結果存放目錄
├── .gitignore             # Git 版控忽略清單
├── README.md              # 專案英文說明文件
├── README_zh.md           # 專案中文說明文件
└── requirements.txt       # Python 依賴套件列表
```

## 技術棧

- **前端框架**: NiceGUI
- **PDF 處理**: PyMuPDF (fitz)
- **Office 文件處理**: 
  - python-docx (Word)
  - openpyxl (Excel)
  - python-pptx (PowerPoint)
- **文字處理**: Python 標準庫

## 授權

本專案採用 MIT 授權條款。

## 待辦事項

- [x] 支援更多文件格式
- [x] 改進非英文文件的處理
- [ ] 整合 LLM 辨識
- [ ] 優化大型文件的處理效能
- [ ] 添加批次處理功能

## 注意事項

- 上傳的文件會暫存在 `temp_uploads` 目錄，應用程式關閉後會自動清除
- 單一文件大小限制為 200MB
- 建議在穩定網路環境下使用，特別是處理大型文件時
