# Helper functions (file handling, logging)
import logging
import os
import functools

# Ensure logs folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_logger(name):
    """
    Returns a logger instance for the given module.
    
    Args:
        name (str): Module name.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    return logger

# Create logger instance
logger = get_logger(__name__)

def exception_handler(func):
    """
    Decorator to handle exceptions and log errors.

    Args:
        func (function): Function to wrap.

    Returns:
        function: Wrapped function with error handling.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return None  # Return None in case of failure
    return wrapper


import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_document:
            for page in pdf_document:
                text += page.get_text("text")  # Extract text from each page
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text.strip()
