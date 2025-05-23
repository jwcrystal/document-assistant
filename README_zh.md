# 文件助手 (Document Assistant)

## 專案描述

這是一個基於 NiceGUI 的文件處理應用程式，支援多種文件格式的預覽和 OCR 文字辨識。應用程式提供直觀的用戶界面，方便用戶上傳、預覽文件，並將文件內容轉換為可編輯的文字格式。

## 功能特點

- **多格式支援**：支援 PDF、Word (DOCX/DOC)、PowerPoint (PPTX/PPT)、Excel (XLSX/XLS)、圖片 (PNG/JPG/JPEG)、Markdown 和 HTML 文件
- **即時預覽**：上傳後可立即預覽文件內容
- **OCR 文字辨識**：從圖片和 PDF 中提取文字內容
- **Markdown 輸出**：將辨識結果格式化為 Markdown 格式
- **下載功能**：將處理結果下載為 Markdown 文件
- **響應式設計**：自適應不同螢幕尺寸

## 安裝

1. **克隆存儲庫**

    ```bash
    git clone <repository_url>
    cd document-assistant
    ```

2. **建立虛擬環境（建議）**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows 系統使用 `venv\Scripts\activate`
    ```

3. **安裝依賴套件**

    ```bash
    pip install -r requirements.txt
    ```

## 使用說明

1. **啟動應用程式**

    ```bash
    python app_new.py
    ```

2. 打開網頁瀏覽器，訪問顯示的本地網址（通常是 `http://localhost:8080`）

3. 點擊「選擇文件」按鈕或直接拖放文件到上傳區域

4. 上傳完成後，可以在頁面上預覽文件內容

5. 點擊「執行 OCR 辨識」按鈕開始處理文件

6. 處理完成後，可以查看文字辨識結果並使用「下載 Markdown」按鈕保存結果

## 支援的文件格式

| 文件類型 | 副檔名 | 預覽支援 | OCR 支援 |
|---------|-------|---------|---------|
| PDF 文件（純文字） | .pdf  | 是   | 是   |
| Word 文件 | .docx, .doc | 是 | 是 |
| PowerPoint | .pptx, .ppt | 是 | 是 |
| Excel 文件 | .xlsx, .xls | 是 | 是 |
| CSV 文件 | .csv | 是 | 是 |
| 圖片文件 | .png, .jpg, .jpeg | 是 | 是 |
| Markdown | .md, .markdown | 是 | 是 |
| HTML 文件 | .html, .htm | 是 | 是 |


## 專案結構

```sh
document-assistant/
├── app_new.py          # 主應用程式 (NiceGUI)
├── app.py             # 舊版 Streamlit 應用程式
├── test_docling.py     # Docling 測試腳本
├── test_docling_llm.py # Docling 與 LM Studio 整合測試
├── temp_uploads/       # 臨時上傳文件目錄
├── output/             # 輸出目錄
├── requirements.txt    # 依賴套件列表
└── README.md          # 專案說明文件
```

## 技術棧

- **前端框架**: [NiceGUI](https://nicegui.io/)
- **PDF 處理**: PyMuPDF (fitz)
- **Office 文件處理**: 
  - python-docx (Word)
  - openpyxl (Excel)
  - python-pptx (PowerPoint)
- **文字處理**: Python 標準庫

## 授權

本專案採用 MIT 授權條款。

## 貢獻

歡迎提交 Pull Request 或回報問題。

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
