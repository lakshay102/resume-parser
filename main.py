# # main.py

# from parser.pdf_reader import extract_text_from_pdf

# if __name__ == "__main__":
#     file_path = "test.pdf"  # Replace with actual file
#     raw_text = extract_text_from_pdf(file_path)
    
#     print("=== Extracted Text ===")
#     print(raw_text[:])  # Show first 2000 characters for preview

# main.py

import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from parser.extractor import extract_basic_fields
from parser.docx_reader import extract_text_from_docx
from parser.pdf_reader import extract_text_from_pdf
import json

UPLOAD_DIR = "uploads"
JSON_OUTPUT_DIR = "parsed_jsons"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)

app = FastAPI()

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

@app.post("/parse-resume/")
async def parse_resume(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[-1].lower()
    
    if ext not in SUPPORTED_EXTENSIONS:
        return JSONResponse(status_code=400, content={"error": "Only PDF and DOCX files are supported."})

    file_id = str(uuid.uuid4())
    saved_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")

    # Save uploaded file
    with open(saved_path, "wb") as f:
        f.write(await file.read())

    # Extract text based on file type
    if ext == ".pdf":
        raw_text = extract_text_from_pdf(saved_path)
    elif ext == ".docx":
        raw_text = extract_text_from_docx(saved_path)
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type."})

    # TEMP: Save raw text to JSON (structured parsing comes later)
    # data = {
    #     "file_name": file.filename,
    #     "file_id": file_id,
    #     "raw_text": raw_text
    # }

    # For Structured Parsing
    structured_data = extract_basic_fields(raw_text)
    structured_data.update({
        "file_name": file.filename,
        "file_id": file_id
    })

    output_path = os.path.join(JSON_OUTPUT_DIR, f"{file_id}.json")
    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(structured_data, out_file, indent=4, ensure_ascii=False)

    return {"message": "Resume parsed successfully", "data": structured_data}
