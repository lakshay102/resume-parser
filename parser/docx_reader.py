# parser/docx_reader.py

from docx import Document

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts all text from a DOCX file.
    
    :param file_path: Path to the .docx file
    :return: Extracted text as a single string
    """
    text = []
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            if para.text.strip():
                text.append(para.text)
    except Exception as e:
        print(f"[ERROR] Failed to read DOCX file: {e}")
    return "\n".join(text)
