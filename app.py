import streamlit as st
import tempfile
import os
from docling.document_converter import DocumentConverter
import fitz  # PyMuPDF
import unicodedata
from docx import Document as DocxDocument  # python-docx

def main():
    # 初始化Streamlit應用
    st.set_page_config(page_title="Document Assistant", layout="wide")

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
    </style>
    """, unsafe_allow_html=True)

    # 應用主界面
    st.title("📄 Document Assistant")

    # 拖曳上傳區域
    uploaded_file = st.file_uploader("拖曳文件至此", type=["pdf", "png", "jpg", "jpeg", "docx"], label_visibility="collapsed")

    # 即時預覽面板
    if uploaded_file:
        st.subheader("📄 即時預覽")
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        # 顯示預覽
        if uploaded_file.type.startswith("image/"):
            st.image(tmp_path, caption="即時預覽", use_container_width=True)
        elif uploaded_file.type == "application/pdf":
            # 使用 PyMuPDF 顯示 PDF 預覽
            with fitz.open(tmp_path) as pdf:
                for page_num in range(len(pdf)):
                    page = pdf.load_page(page_num)
                    pix = page.get_pixmap(dpi=150)  # 提高解析度
                    st.image(pix.tobytes(), caption=f"PDF 頁面 {page_num + 1}", use_container_width=True)
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
                # 初始化Docling轉換器
                converter = DocumentConverter()
                # 執行文件轉換
                result = converter.convert(tmp_path)
                
                # 顯示OCR結果
                st.markdown("### 📝 OCR 結果")
                markdown_result = result.document.export_to_markdown()
                st.markdown(markdown_result, unsafe_allow_html=True)
                
                # 下載結果功能
                # 使用sanitize_filename處理中文檔名問題
                def sanitize_filename(filename):
                    normalized = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
                    return normalized.replace(" ", "_")
                
                st.download_button(
                    label="下載結果",
                    data=markdown_result,
                    file_name=f"ocr_result_{sanitize_filename(uploaded_file.name)}.md",
                    mime="text/markdown"
                )
            except FileNotFoundError:
                st.error("找不到指定的文件，請確認文件路徑是否正確")
            except PermissionError:
                st.error("沒有文件存取權限，請確認文件是否被其他程序使用")
            except Exception as e:
                st.error(f"發生未知錯誤: {str(e)}")
            finally:
                # 確保臨時文件清理
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)


if __name__ == "__main__":
    main()