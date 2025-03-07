from flask import Flask, request, jsonify
import os
import pdfplumber

app = Flask(__name__)

UPLOAD_FOLDER = "data/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ Error extracting text from {pdf_path}: {e}")
        return None  # Return None if an error occurs

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the file
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    print(f"✅ File saved at: {file_path}")  # Debugging print

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # Debugging print
    if extracted_text:
        print(f"✅ Extracted text (first 100 chars): {extracted_text[:100]}...")
    else:
        print(f"⚠️ No text extracted from: {file_path}")

    return jsonify({
        "message": f"File {file.filename} uploaded successfully!",
        "extracted_text": extracted_text if extracted_text else "No text extracted!"
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
