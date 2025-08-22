# from fastapi import FastAPI, File, Form, UploadFile
# import pdfplumber

# app = FastAPI()

# @app.post("/unlock")
# async def unlock(password: str = Form(...), pdf: UploadFile = File(...)):
#     with pdfplumber.open(pdf.file, password=password) as pdf_doc:
#         text = ""
#         for page in pdf_doc.pages:
#             text += page.extract_text() + "\n"
#     return {"text": text}


from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd
import pdfplumber
import os

app = FastAPI()

PDF_PASSWORD = "900001"  # default, can be overridden by request


# --- Dummy helpers (replace with your real ones) ---
def extract_payment_date(text):
    # TODO: replace with your regex logic
    return "2025-08-22"

def clean_dataframe(df):
    # TODO: replace with your cleaning logic
    return df

def parse_text_to_dataframe(text):
    # TODO: replace with your custom parsing logic
    return pd.DataFrame({"Text": [text]})


# --- Your original extraction function ---
def extract_pdf_table_to_dataframe(file_path, password=PDF_PASSWORD):
    try:
        with pdfplumber.open(file_path, password=password) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            tables = page.extract_tables()

            payment_date = extract_payment_date(text)

            if tables:
                df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
                df = clean_dataframe(df)
            else:
                df = parse_text_to_dataframe(text)

            df["Filename"] = os.path.basename(file_path)
            df["Payment_Date"] = payment_date
            return df

    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})


# --- API endpoint ---
@app.post("/unlock")
async def unlock(password: str = Form(...), pdf: UploadFile = File(...)):
    # Save uploaded PDF temporarily
    temp_path = f"/tmp/{pdf.filename}"
    with open(temp_path, "wb") as f:
        f.write(await pdf.read())

    # Extract dataframe
    df = extract_pdf_table_to_dataframe(temp_path, password)

    # Convert dataframe to JSON and return
    return {"data": df.to_dict(orient="records")}
