from docling.document_converter import DocumentConverter

source = "./test/test.pdf"  # document per local path or URL
output_path = "./output/docling.md" 

converter = DocumentConverter()
result = converter.convert(source)

markdown_text = result.document.export_to_markdown()

with open(output_path, "w", encoding="utf-8") as f:
    f.write(markdown_text)

print(f"Markdown 已保存到：{output_path}")
