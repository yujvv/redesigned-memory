# https://github.com/matsui528/faiss_tips

import faiss
import numpy as np
import os
import pickle
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

# Initialize the SentenceTransformer model
EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
model = SentenceTransformer(EMBEDDING_PATH)

# Initialize chromadb
client = chromadb.Client(settings=Settings(allow_reset=True))
collection_name = "AIAssistant"
collection = client.create_collection(name=collection_name)

def split_document_with_overlap(file_path, chunk_size, overlap_size, delimiters):
    chunks = []
    chunk_ids = []
    buffer = ""
    chunk_id = 1

    with open(file_path, 'r', encoding='utf-8') as f:
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
                chunks.append(chunk)
                chunk_ids.append(f"id{chunk_id}")

                buffer = buffer[end_index - overlap_size:]
                chunk_id += 1

    # Handle the last remaining part if there's any
    if buffer:
        chunks.append(buffer)
        chunk_ids.append(f"id{chunk_id}")

    return chunk_ids, chunks

def build_vector_database(example_docs):
    # Load and split the document
    chunk_ids, split_data = split_document_with_overlap(example_docs, chunk_size=100, overlap_size=10, delimiters=["\n\n", "\n", ""])

    # Generate sentence embeddings
    sentence_embeddings = model.encode(split_data)

    # Save embeddings to disk
    with open('embeddings.pkl', 'wb') as f:
        pickle.dump(sentence_embeddings, f)

    # Add documents to ChromaDB
    collection.add(embeddings=sentence_embeddings.tolist(),
                   documents=split_data,
                   ids=chunk_ids)

def offline_retrieval(query_embedding):
    # Load embeddings from disk
    with open('embeddings.pkl', 'rb') as f:
        sentence_embeddings = pickle.load(f)

    # Build Faiss index
    index = faiss.IndexFlatL2(sentence_embeddings.shape[1])
    index.add(sentence_embeddings)

    # Perform similarity search
    D, I = index.search(np.array(query_embedding).astype('float32'), k=5)

    return I[0]

def get_relevant_documents(query):
    # Load and split the document
    example_docs = "example.txt"
    chunk_ids, split_data = split_document_with_overlap(example_docs, chunk_size=100, overlap_size=10, delimiters=["\n\n", "\n", ""])

    # Generate sentence embeddings
    sentence_embeddings = model.encode(split_data)

    # Save embeddings to disk
    with open('embeddings.pkl', 'wb') as f:
        pickle.dump(sentence_embeddings, f)

    # Add documents to ChromaDB
    collection.add(embeddings=sentence_embeddings.tolist(),
                   documents=split_data,
                   ids=chunk_ids)

    # Generate query embedding
    query_embedding = model.encode([query])  # Note: query needs to be a list

    # Perform offline retrieval
    relevant_indices = offline_retrieval(query_embedding)

    # Fetch relevant documents from ChromaDB
    relevant_documents = [split_data[idx] for idx in relevant_indices]

    return relevant_documents

# Testing the function
if __name__ == '__main__':
    query = "What is 华为HG8346M?"
    results = get_relevant_documents(query)
    if results:
        for idx, result in enumerate(results, 1):  
            print(f"Document {idx}:")
            print(result)
            print("---")
    else:
        print("No relevant documents found.")
