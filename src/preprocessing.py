import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
from src.utils import logger, exception_handler  # Import logging & exception handling

# Download stopwords if not already present
nltk.download('stopwords')

# Define stopwords set
STOPWORDS = set(stopwords.words('english'))

@exception_handler
def clean_text(text):
    """
    Cleans text by removing punctuation and stopwords.
    
    Args:
        text (str): Input document text.
    
    Returns:
        str: Cleaned text.
    """
    text = text.lower()  # Convert to lowercase
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    words = text.split()
    words = [word for word in words if word not in STOPWORDS]  # Remove stopwords
    return " ".join(words)

@exception_handler
def process_documents(documents):
    """
    Applies TF-IDF vectorization to the list of documents.

    Args:
        documents (list of str): List of document texts.

    Returns:
        tuple: (TF-IDF matrix, vectorizer)
    """
    if not documents:
        raise ValueError("Document list is empty!")

    vectorizer = TfidfVectorizer(preprocessor=clean_text)
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    logger.info("TF-IDF vectorization completed.")
    return tfidf_matrix, vectorizer
