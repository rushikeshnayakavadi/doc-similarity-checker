import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# Now call the function
print(extract_text_from_pdf("data/Rushikesh_Nayakavadi_Resume.pdf"))
