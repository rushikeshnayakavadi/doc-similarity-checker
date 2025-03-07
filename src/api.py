from flask import Flask, render_template, request, jsonify
import os
import pdfplumber
import sqlite3
from src.similarity import compute_similarity
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


# Explicitly set template folder
app = Flask(__name__, template_folder="../templates")

UPLOAD_FOLDER = "data/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database connection function
def get_db_connection():
    conn = sqlite3.connect("src/database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Ensure database and table exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize database
init_db()

@app.route("/")
def home():
    return render_template("index.html")  # Ensure "templates/index.html" exists

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

    # Store in SQLite
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (file.filename, extracted_text))
    conn.commit()
    conn.close()

    return jsonify({
        "message": f"File '{file.filename}' uploaded and stored successfully!",
        "extracted_text": extracted_text if extracted_text else "No text extracted!"
    }), 200

@app.route("/documents", methods=["GET"])
def get_documents():
    """Fetch all stored documents from the database."""
    conn = sqlite3.connect("src/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename FROM documents")  # Get only IDs & filenames
    documents = cursor.fetchall()
    conn.close()

    return jsonify({"documents": [{"id": doc[0], "filename": doc[1]} for doc in documents]})

@app.route("/match", methods=["POST"])
def match_document():
    """Compare uploaded document against stored documents and return similar matches."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)
    
    extracted_text = extract_text_from_pdf(file_path)

    # Fetch stored documents
    conn = sqlite3.connect("src/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, content FROM documents")
    stored_docs = cursor.fetchall()
    conn.close()

    # Compute similarities
    results = []
    for doc_id, filename, content in stored_docs:
        similarity_score = compute_similarity(extracted_text, content)
        results.append((filename, similarity_score))

    # Sort by similarity
    results.sort(key=lambda x: x[1], reverse=True)

    return jsonify({
        "matches": results[:5]  # Return top 5 similar documents
    })

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

if __name__ == "__main__":
    app.run(debug=True)
