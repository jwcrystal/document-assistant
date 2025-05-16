import streamlit as st
import tempfile
import os
from docling.document_converter import DocumentConverter
import fitz  # PyMuPDF
import unicodedata
from docx import Document as DocxDocument  # python-docx
import re # 引入 re 模組

# 檔名標準化函數
def sanitize_filename(filename):
    # 使用 NFKD 標準化並編碼為 UTF-8，忽略無法處理的字元
    normalized = unicodedata.normalize('NFKD', filename).encode('utf-8', 'ignore').decode('utf-8')
    # 將空格替換為底線
    sanitized = normalized.replace(" ", "_")
    # 移除所有非字母、數字、底線、連字號和點的字元
    # \w 匹配字母、數字、底線，. 匹配點，- 匹配連字號
    sanitized = re.sub(r'[^\w.-]', '', sanitized)
    return sanitized

def main():
    # 初始化Streamlit應用
    st.set_page_config(page_title="Document Assistant", layout="wide")

    # 初始化 session state 中的 PDF 頁碼
    if 'pdf_page' not in st.session_state:
        st.session_state.pdf_page = 0 # 頁碼從 0 開始

    # 樣式設定
    st.markdown("""
    <style>
        .stFileUploader {
            border: 2px dashed #4CAF50;
            padding: 20px;
            text-align: center;
        }
        .stFileUploader label {
            color: #4CAF50;
            font-weight: bold;
        }
        /* 新增樣式來居中頁碼文字 */
        .centered-text {
            text-align: center;
            vertical-align: middle; /* 嘗試垂直對齊 */
            line-height: 2.5em; /* 根據按鈕高度調整行高 */
        }
    </style>
    """, unsafe_allow_html=True)

    # 應用主界面
    st.title("📄 Document Assistant")

    # 拖曳上傳區域
    uploaded_file = st.file_uploader("拖曳文件至此", type=["pdf", "png", "jpg", "jpeg", "docx"], label_visibility="collapsed")
    # 即時預覽面板
    if uploaded_file:
        st.subheader("📄 即時預覽")
        with tempfile.NamedTemporaryFile(delete=False, suffix=sanitize_filename(os.path.splitext(uploaded_file.name)[1])) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        # 顯示預覽
        if uploaded_file.type.startswith("image/"):
            st.image(tmp_path, caption="即時預覽", use_container_width=True)
        elif uploaded_file.type == "application/pdf":
            # 使用 PyMuPDF 顯示 PDF 預覽
            try:
                with fitz.open(tmp_path) as pdf:
                    total_pages = len(pdf)

                    # 確保當前頁碼在有效範圍內
                    if st.session_state.pdf_page >= total_pages:
                        st.session_state.pdf_page = total_pages - 1
                    if st.session_state.pdf_page < 0:
                        st.session_state.pdf_page = 0

                    # 顯示當前頁面圖片
                    page = pdf.load_page(st.session_state.pdf_page)
                    pix = page.get_pixmap(dpi=150)  # 提高解析度
                    st.image(pix.tobytes(), use_container_width=True)

                    # 頁面切換按鈕和頁碼文字
                    # 創建三欄：左邊按鈕，中間頁碼，右邊按鈕
                    col1, col2, col3 = st.columns([1, 2, 1]) # 調整比例使中間欄寬度更大

                    with col1:
                        if st.session_state.pdf_page > 0: # 只有當不是第一頁時才顯示上一頁按鈕
                            if st.button("上一頁"):
                                st.session_state.pdf_page -= 1
                                st.rerun() # 重新運行以更新顯示
                        else:
                            st.empty() # 在第一頁時留空，保持佈局一致

                    with col2:
                        # 顯示頁碼文字並居中
                        st.markdown(f"<div class='centered-text'>PDF 頁面 {st.session_state.pdf_page + 1} / {total_pages}</div>", unsafe_allow_html=True)

                    with col3:
                        if st.session_state.pdf_page < total_pages - 1: # 只有當不是最後一頁時才顯示下一頁按鈕
                            if st.button("下一頁"):
                                st.session_state.pdf_page += 1
                                st.rerun() # 重新運行以更新顯示
                        else:
                            st.empty() # 在最後一頁時留空，保持佈局一致


            except Exception as e:
                 st.error(f"無法預覽 PDF: {str(e)}")

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # 使用 python-docx 顯示 Word 預覽
            doc = DocxDocument(tmp_path)
            for para in doc.paragraphs:
                st.markdown(f"> {para.text}")

        # OCR 處理
        if st.button("執行 OCR"):
            # 顯示處理進度
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # 更新狀態文字和進度條，表示處理開始
                status_text.text("正在處理文件...")
                progress_bar.progress(10) # 設定一個初始進度值

                # 初始化Docling轉換器
                converter = DocumentConverter()
                # 執行文件轉換 (這是同步操作，會阻塞直到完成)
                result = converter.convert(tmp_path)
                
                # 如果轉換成功，更新狀態文字和進度條
                status_text.text("文件處理完成！")
                progress_bar.progress(100) # 設定進度為 100%

                # 顯示OCR結果 (只顯示前幾行作為摘要)
                st.markdown("### 📝 OCR 結果 (摘要)")
                markdown_result = result.document.export_to_markdown()
                
                # 將 markdown 結果按行分割，只取前 10 行顯示
                summary_lines = markdown_result.splitlines()[:10]
                # 如果結果超過 10 行，加上省略號
                summary_text = "\n".join(summary_lines) + ("\n...\n請下載完整結果" if len(summary_lines) < markdown_result.count('\n') + 1 else "")

                st.markdown(summary_text, unsafe_allow_html=True) # 顯示摘要

                # 下載結果功能 
                st.download_button(
                    label="下載結果",
                    data=markdown_result,
                    file_name=f"ocr_result_{sanitize_filename(uploaded_file.name)}.md",
                    mime="text/markdown"
                )
            except FileNotFoundError:
                status_text.text("處理失敗：找不到文件")
                progress_bar.progress(0) # 處理失敗，進度條歸零
                st.error("找不到指定的文件，請確認文件路徑是否正確")
            except PermissionError:
                status_text.text("處理失敗：文件權限問題")
                progress_bar.progress(0) # 處理失敗，進度條歸零
                st.error("沒有文件存取權限，請確認文件是否被其他程序使用")
            except Exception as e:
                status_text.text("處理失敗：發生未知錯誤")
                progress_bar.progress(0) # 處理失敗，進度條歸零
                st.error(f"發生未知錯誤: {str(e)}")
            finally:
                # 確保臨時文件清理
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                # 可以在這裡選擇是否清除進度條和狀態文字
                # status_text.empty()
                # progress_bar.empty()


if __name__ == "__main__":
    main()
