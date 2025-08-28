from fastapi import FastAPI, UploadFile, Form
from pypdf import PdfReader
import os
import shutil

app = FastAPI()

def decrypt_pdf(pdf_path, password):
    reader = PdfReader(pdf_path)

    if reader.is_encrypted:
        reader.decrypt(password)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # Save decrypted text file
    base_name = os.path.splitext(pdf_path)[0]
    txt_filename = f"{base_name}_decrypted.txt"

    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(text)

    return txt_filename

@app.post("/decrypt")
async def decrypt_endpoint(file: UploadFile, password: str = Form(...)):
    # Save uploaded file
    temp_pdf_path = file.filename
    with open(temp_pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        txt_file = decrypt_pdf(temp_pdf_path, password)

        # Read decrypted text back for API response
        with open(txt_file, "r", encoding="utf-8") as f:
            content = f.read()

        return {"decrypted_text": content}

    finally:
        # Clean up temp files
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        if os.path.exists(txt_file):
            os.remove(txt_file)
