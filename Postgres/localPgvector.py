import psycopg2
from sentence_transformers import SentenceTransformer

# Initialize the SentenceTransformer model
EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
model = SentenceTransformer(EMBEDDING_PATH)

# Connect to Local PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="your_database",
    user="your_username",
    password="your_password"
)
cur = conn.cursor()

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

    # Store embeddings in Local PostgreSQL
    for i in range(len(chunk_ids)):
        cur.execute("INSERT INTO documents (id, text, vector) VALUES (%s, %s, %s)",
                    (chunk_ids[i], split_data[i], psycopg2.Binary(sentence_embeddings[i])))

    conn.commit()

def get_relevant_documents(query):
    # Load and split the document
    example_docs = "example.txt"
    chunk_ids, split_data = split_document_with_overlap(example_docs, chunk_size=100, overlap_size=10, delimiters=["\n\n", "\n", ""])

    # Generate sentence embeddings for the query
    query_embedding = model.encode([query])[0]

    # Perform similarity search in Local PostgreSQL
    cur.execute("SELECT id, text, vector, pgv_cosim(vector, %s) AS similarity FROM documents ORDER BY similarity DESC LIMIT 5", (psycopg2.Binary(query_embedding),))
    results = cur.fetchall()

    return results

# Testing the function
if __name__ == '__main__':
    query = "What is 华为HG8346M?"

    # Build vector database
    build_vector_database("example.txt")

    # Retrieve relevant documents
    results = get_relevant_documents(query)
    if results:
        for idx, result in enumerate(results, 1):  
            print(f"Document {idx}:")
            print(result[1])  # Assuming the text is in the second column
            print("---")
    else:
        print("No relevant documents found.")

# Close the cursor and connection
cur.close()
conn.close()
