from flask import Flask, request, send_file, jsonify
import tempfile
import pikepdf
import os

app = Flask(__name__)

@app.route("/unlock", methods=["POST"])
def unlock_pdf():
    # Expect password + file
    password = request.form.get("password")
    file = request.files.get("file")

    if not file or not password:
        return jsonify({"error": "Missing file or password"}), 400

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp_in:
            file.save(tmp_in.name)
            input_path = tmp_in.name

        output_path = input_path + "_unlocked.pdf"

        # Unlock with pikepdf
        with pikepdf.open(input_path, password=password) as pdf:
            pdf.save(output_path)

        return send_file(output_path, as_attachment=True, download_name="unlocked.pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except:
            pass

