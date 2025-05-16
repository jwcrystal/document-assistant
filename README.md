# Document OCR Assistant

## Project Description

This project provides a simple Streamlit application for performing OCR on various document types, including PDF, PNG, JPG, JPEG, and DOCX. It utilizes the `docling` library for document conversion and OCR processing.

## Features

- **File Upload:** Easily upload PDF, image (PNG, JPG, JPEG), and DOCX files.
- **Real-time Preview:** View a preview of the uploaded document directly in the application.
- **OCR Processing:** Extract text content from the uploaded documents using OCR.
- **Markdown Output:** Get the OCR results formatted in Markdown.
- **Download Results:** Download the OCR results as a Markdown file.

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd document-assistant
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install LM Studio (if using the LLM feature):**
    If you plan to use the LLM-based OCR processing (`test_docling_llm.py`), you will need to install and run LM Studio and load a compatible model (e.g., `internvl3-8b-instruct` or `internvl3-2b`). Refer to the LM Studio documentation for installation and usage details.

## Usage

1. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to the provided local URL (usually `http://localhost:8501`).

3. Drag and drop your document file into the designated area.

4. Click the "執行 OCR" (Execute OCR) button to start the process.

5. View the OCR results in the application and use the "下載結果" (Download Result) button to save the Markdown output.

## Project Structure

```sh
ocr_extension/
├── .gitignore
├── app.py          # Streamlit application
├── output/         # Output directory for results
├── test/           # Test files
│   ├── BBG-How to Deploy Services.jpg
│   └── 伺服器現況概述.pdf
├── test_docling.py # Example using basic docling conversion
├── test_docling_llm.py # Example using docling with LM Studio VLM
└── README.md       # Project README file
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or report issues.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [docling library](https://github.com/docling/docling)
- [Streamlit](https://streamlit.io/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [python-docx](https://python-docx.readthedocs.io/)
- [LM Studio](https://lmstudio.ai/)
