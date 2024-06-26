# app/utils.py
import faiss
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the SentenceTransformer model and FAISS index
model = SentenceTransformer('all-MiniLM-L6-v2')
documents = []
index = None

def embed_documents(docs: List[str]) -> np.ndarray:
    global model
    vectors = model.encode(docs)
    logging.info(f"Embedding dimension: {vectors.shape[1]}")
    return vectors.astype('float32')

def add_documents_to_index(docs: List[str]) -> List[int]:
    global documents, index
    document_ids = []
    embeddings = embed_documents(docs)
    dimension = embeddings.shape[1]

    # Initialize the FAISS index with the correct dimension if it's not already initialized
    if index is None or index.d != dimension:
        index = faiss.IndexFlatL2(dimension)
        logging.info(f"Initialized FAISS index with dimension: {dimension}")

    # Add documents and update the global index and documents list
    index.add(embeddings)
    for doc in docs:
        documents.append(doc)
        document_id = len(documents) - 1
        document_ids.append(document_id)
    
    logging.info(f"Added {len(embeddings)} documents to the index")
    return document_ids

def retrieve_documents(query: str, k: int = 5) -> List[int]:
    global model, index
    query_vec = model.encode([query]).astype('float32')
    logging.info(f"Query vector dimension: {query_vec.shape[1]}")
    D, I = index.search(query_vec, k)
    valid_ids = [int(doc_id) for doc_id in I[0] if doc_id != -1]
    logging.info(f"Retrieved valid document IDs: {valid_ids}")
    return valid_ids
