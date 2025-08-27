from flask import Flask, request, send_file
import tempfile
import pikepdf
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "PDF Unlock API is running. Use POST /unlock with a file + password."}

@app.route("/unlock", methods=["POST"])
def unlock():
    pdf_file = request.files.get("file")
    password = request.form.get("password")

    if not pdf_file or not password:
        return {"error": "file and password are required"}, 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
        pdf_file.save(tmp_in.name)
        tmp_in.flush()

        try:
            with pikepdf.open(tmp_in.name, password=password) as pdf:
                tmp_out = tmp_in.name.replace(".pdf", "_unlocked.pdf")
                pdf.save(tmp_out)

            return send_file(tmp_out, as_attachment=True, download_name="unlocked.pdf")

        except Exception as e:
            return {"error": str(e)}, 400
        finally:
            try:
                os.remove(tmp_in.name)
            except:
                pass
