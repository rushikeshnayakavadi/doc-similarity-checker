import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocessing import process_documents
from src.utils import logger, exception_handler  # Importing logging & exception handling
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@exception_handler
def find_similar_documents(query_text, stored_texts, top_n=5):
    """
    Finds the most similar documents to the given query_text using Cosine Similarity.
    """
    if not query_text.strip():
        raise ValueError("Query text is empty!")

    if not stored_texts:
        raise ValueError("Stored document list is empty!")

    # Process stored documents + query text using TF-IDF
    tfidf_matrix, vectorizer = process_documents(stored_texts + [query_text])

    # Extract vectors: Last vector is the query, rest are stored docs
    stored_vectors = tfidf_matrix[:-1]
    query_vector = tfidf_matrix[-1]

    # Compute cosine similarity between query and stored documents
    similarities = cosine_similarity(query_vector, stored_vectors)[0]

    # Get top N most similar document indices
    top_indices = np.argsort(similarities)[::-1][:top_n]
    results = [(idx, round(similarities[idx], 4)) for idx in top_indices]

    logger.info("Successfully found similar documents for query.")
    return results

def compute_similarity(text1, text2):
    """Compute cosine similarity between two texts."""
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]

# Example usage
if __name__ == "__main__":
    stored_docs = [
        "This is a sample document about machine learning.",
        "Natural language processing is a branch of AI.",
        "Flask is a lightweight Python web framework.",
        "Deep learning is a subset of machine learning."
    ]
    query_doc = "I want to learn about AI and NLP."

    results = find_similar_documents(query_doc, stored_docs)
    print("Top Similar Documents:", results)
