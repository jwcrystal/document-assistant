# Document Assistant

[中文版](README_zh.md)

## Project Description

A modern document processing application built with NiceGUI that supports preview and OCR text recognition for various file formats. The application provides an intuitive user interface for uploading, previewing documents, and converting document content into editable text format.

## Features

- **Multiple Format Support**: PDF, Word (DOCX/DOC), PowerPoint (PPTX/PPT), Excel (XLSX/XLS), Images (PNG/JPG/JPEG), Markdown, and HTML files
- **Real-time Preview**: Instantly preview uploaded documents
- **OCR Text Recognition**: Extract text content from images and PDFs
- **Markdown Output**: Format recognition results in Markdown
- **Download Functionality**: Save processed results as Markdown files
- **Responsive Design**: Adapts to different screen sizes

## Installation

1. **Clone the repository**

    ```bash
    git clone <repository_url>
    cd document-assistant
    ```

2. **Create a virtual environment (recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**

    ```bash
    python app_new.py
    ```

2. Open your web browser and navigate to the displayed local URL (typically `http://localhost:8080`)

3. Click the "Select File" button or drag and drop a file into the upload area

4. After uploading, you can preview the document content on the page

5. Click the "Run OCR Recognition" button to start processing the document

6. After processing is complete, view the text recognition results and use the "Download Markdown" button to save the results

## Supported File Formats

| File Type           | Extensions         | Preview Supported | OCR Supported |
|---------------------|--------------------|-------------------|---------------|
| PDF File (Text-based)| .pdf              | Yes               | Yes           |
| Word Document       | .docx, .doc        | Yes               | Yes           |
| PowerPoint          | .pptx, .ppt        | Yes               | Yes           |
| Excel File          | .xlsx, .xls        | Yes               | Yes           |
| CSV File            | .csv               | Yes               | Yes           |
| Image File          | .png, .jpg, .jpeg  | Yes               | Yes           |
| Markdown            | .md, .markdown     | Yes               | Yes           |
| HTML File           | .html, .htm        | Yes               | Yes           |

## Project Structure

```sh
document-assistant/
├── app_new.py          # Main application (NiceGUI)
├── app.py             # Legacy Streamlit application
├── test_docling.py     # Docling test script
├── test_docling_llm.py # Docling with LM Studio integration test
├── temp_uploads/       # Temporary upload directory
├── output/             # Output directory
├── requirements.txt    # Dependencies list
└── README.md          # Project documentation
```

## Technology Stack

- **Frontend Framework**: [NiceGUI](https://nicegui.io/)
- **PDF Processing**: PyMuPDF (fitz)
- **Office Document Processing**:
  - python-docx (Word)
  - openpyxl (Excel)
  - python-pptx (PowerPoint)
  - pandas (CSV)
- **Text Processing**: Python Standard Library

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or report issues.

## Todo List

- [ ] Support more file formats
- [ ] Improve handling of non-English documents
- [ ] Add LLM integration for document analysis
- [ ] Optimize performance for large files
- [ ] Add batch processing functionality

## Notes

- Uploaded files are temporarily stored in the `temp_uploads` directory and will be automatically cleared when the application is closed
- Maximum single file size is limited to 200MB
- Recommended to use in a stable network environment, especially when processing large files