import sqlite3
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import os

EMBEDDING_MODEL_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
# SQLite for local storage
DATABASE_PATH = "local_db.sqlite3"

# def clear_database():
#     cursor.execute("DELETE FROM Documents")
#     conn.commit()


# Initialize SentenceTransformer model
model = SentenceTransformer(EMBEDDING_MODEL_PATH)

# Initialize SQLite database connection
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Documents
                      (id TEXT PRIMARY KEY, content TEXT, embedding BLOB)''')
    conn.commit()

def add_document(id: str, content: str, embedding: bytes):
    cursor.execute("INSERT INTO Documents (id, content, embedding) VALUES (?, ?, ?)",
                   (id, content, embedding))
    conn.commit()


def cosine_similarity(embedding1, embedding2):
    dot_product = np.dot(embedding1, embedding2)
    norm_emb1 = np.linalg.norm(embedding1)
    norm_emb2 = np.linalg.norm(embedding2)
    return dot_product / (norm_emb1 * norm_emb2)

def search_local(query_embedding: List[float], n_results=1):
    cursor.execute("SELECT id, content, embedding FROM Documents")
    results = cursor.fetchall()
    relevant_documents = []

    for doc_id, content, stored_embedding in results:
        stored_embedding = np.frombuffer(stored_embedding, dtype=np.float32)  # Convert bytes to NumPy array
        
        # Adjust the dimensionality of the query embedding to match the stored embedding
        query_embedding_adjusted = np.resize(query_embedding, stored_embedding.shape)
        
        similarity = cosine_similarity(query_embedding_adjusted, stored_embedding)
        relevant_documents.append((doc_id, content, similarity))

    relevant_documents.sort(key=lambda x: x[2], reverse=True)
    return relevant_documents[:n_results]



def process_document(doc_id: str, content: str):
    embedding = model.encode([content])[0]
    embedding_bytes = b"".join(float_to_bytes(value) for value in embedding)
    add_document(doc_id, content, embedding_bytes)

def float_to_bytes(float_value):
    scaled_value = int(float_value * 255)
    clamped_value = max(0, min(scaled_value, 255))  # Clamp the value to the range [0, 255]
    return bytes([clamped_value])


def optimize_and_store_documents(file_path: str, chunk_size: int, overlap_size: int, delimiters: List[str]):
    with open(file_path, 'r', encoding='utf-8') as f:
        buffer = ""
        chunk_id = 1

        for line in f:
            buffer += line

            if len(buffer) >= chunk_size:
                end_index = chunk_size

                for delimiter in delimiters:
                    pos = buffer.rfind(delimiter, 0, end_index)
                    if pos != -1:
                        end_index = pos + len(delimiter)
                        break

                chunk = buffer[:end_index]
                process_document(f"id{chunk_id}", chunk)

                buffer = buffer[end_index - overlap_size:]
                chunk_id += 1

        # Handle the last remaining part if any
        if buffer:
            process_document(f"id{chunk_id}", buffer)

# Create the table if not exists
create_table()

# Example usage
if __name__ == '__main__':
    example_docs = "example.txt"
    chunk_size = 500
    overlap_size = 200
    delimiters = ["\n\n", "\n", ""]

    optimize_and_store_documents(example_docs, chunk_size, overlap_size, delimiters)

    query = "What is 华为HG8346M?"
    query_embedding = model.encode([query])[0].tolist()
    search_results = search_local(query_embedding)
    
    for idx, (doc_id, content, similarity) in enumerate(search_results, 1):
        print(f"Document {idx}:")
        print(f"ID: {doc_id}")
        print(f"Content: {content}")
        print(f"Similarity: {similarity}")
        print("---")
