import os

def create_project_structure():
    folders = [
        "data", "models", "src", "logs"
    ]
    files = {
        "src/preprocessing.py": "# TF-IDF vectorization logic\n",
        "src/similarity.py": "# Cosine similarity logic\n",
        "src/api.py": "# Flask API for document uploads & matching\n",
        "src/utils.py": "# Helper functions (file handling, logging)\n",
        "app.py": "# Main entry point for Flask application\n",
        "requirements.txt": "# List dependencies here\n",
        "README.md": "# Project Documentation\n"
    }
    
    # Create subfolders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    # Create files with default content
    for file, content in files.items():
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
    
    print("Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()
