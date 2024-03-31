import faiss
import pickle
import numpy as np

class VectorDatabase:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.index = None
        self.data = []

    # Adds text data and its embedding to the database.
    def add_data(self, text):
        embedding = self.embedding_model.encode(text)
        self.data.append((text, embedding))

    # Builds the vector index using the Faiss library.
    def build_index(self):
        embeddings = [d[1] for d in self.data]
        embeddings_np = np.array(embeddings).astype('float32')
        self.index = faiss.IndexFlatL2(embeddings_np.shape[1])
        self.index.add(embeddings_np)

    # Searches the vector index for the most similar texts given a query.
    def search(self, query, k=5):
        query_embedding = self.embedding_model.encode(query)
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
        results = [(self.data[idx][0], distance) for idx, distance in zip(indices[0], distances[0])]
        return results

    # Saves the vector index to a file using pickle.
    def save_index(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.index, f)

    # Loads the vector index from a file using pickle.
    def load_index(self, path):
        with open(path, 'rb') as f:
            self.index = pickle.load(f)