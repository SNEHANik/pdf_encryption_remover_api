from fastapi import FastAPI, UploadFile, Form
import pikepdf
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/unlock")
async def unlock(pdf: UploadFile, password: str = Form(...)):
    # Save uploaded file
    with open("temp.pdf", "wb") as f:
        f.write(await pdf.read())

    # Unlock with password
    with pikepdf.open("temp.pdf", password=password) as pdf_file:
        pdf_file.save("unlocked.pdf")

    # Return unlocked file
    return StreamingResponse(open("unlocked.pdf", "rb"), media_type="application/pdf")
