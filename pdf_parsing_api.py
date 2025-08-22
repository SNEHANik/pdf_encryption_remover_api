from fastapi import FastAPI, File, Form, UploadFile
import pdfplumber

app = FastAPI()

@app.post("/unlock")
async def unlock(password: str = Form(...), pdf: UploadFile = File(...)):
    with pdfplumber.open(pdf.file, password=password) as pdf_doc:
        text = ""
        for page in pdf_doc.pages:
            text += page.extract_text() + "\n"
    return {"text": text}
