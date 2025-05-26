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
├── app.py (old)           # Legacy main application (before refactoring)
├── src/                   # Source code directory
│   ├── config/            # Configuration modules and settings
│   ├── services/          # Business logic services
│   │   └── ocr/           # OCR-related service modules
│   │       └── ocr_service.py
│   ├── ui/                # User interface modules
│   │   ├── components/    # Reusable UI components
│   │   │   ├── ocr_result_dialog.py  # Dialog for displaying OCR results
│   │   │   └── preview.py            # Document preview component
│   │   └── main_ui.py     # Main user interface
│   └── utils/             # Utility functions and helper modules
│       ├── __init__.py
│       ├── file_utils.py  # File handling utility functions
│       └── app.py         # Main application entry point (after refactoring)
│
├── static/                # Static resources (e.g., CSS, images)
├── temp_uploads/          # Temporary storage directory for uploaded files
├── test/                  # Test code directory
├── output/                # Output results storage directory
├── .gitignore             # Git ignore list
├── README.md              # Project description (English)
├── README_zh.md           # Project description (Chinese)
└── requirements.txt       # Python dependency list

```

## Tech Stack

- **Frontend Framework**: NiceGUI  
- **PDF Processing**: PyMuPDF (fitz)  
- **Office Document Processing**:
  - python-docx (Word)  
  - openpyxl (Excel)  
  - python-pptx (PowerPoint)  
- **Text Processing**: Python Standard Library

## License

This project is licensed under the MIT License.

## Todo List

- [x] Support more file formats
- [x] Improve handling of non-English documents
- [ ] Add LLM integration for document analysis
- [ ] Optimize performance for large files
- [ ] Add batch processing functionality

## Notes

- Uploaded files are temporarily stored in the `temp_uploads` directory and will be automatically cleared when the application is closed
- Maximum single file size is limited to 200MB
- Recommended to use in a stable network environment, especially when processing large files