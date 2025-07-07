from flask import Flask, request, jsonify
import pdfplumber
import os

API_KEY = os.environ["API_KEY"]

app = Flask(__name__)

@app.route("/parse", methods=["POST"])
def parse_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        with pdfplumber.open(file) as pdf:
            all_text = ""
            all_tables = []
            for page in pdf.pages:
                all_text += page.extract_text() or ""
                tables = page.extract_tables()
                if tables:
                    all_tables.extend(tables)
        return jsonify({"text": all_text, "tables": all_tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
