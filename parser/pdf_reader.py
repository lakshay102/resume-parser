# parser/pdf_reader.py

import pymupdf as fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts all text from the PDF file using PyMuPDF.
    
    :param file_path: Path to the PDF file.
    :return: Extracted text as a single string.
    """
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"[ERROR] Could not extract text: {e}")
    return text
