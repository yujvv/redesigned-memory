from sentence_transformers import SentenceTransformer

# Initialize the SentenceTransformer model
# EMBEDDING_MODEL_PATH = "D:/Yu/rag/bge-large-zh-v1.5"

class TextEmbeddingAPI:
    def __init__(self):
        self.path = "D:/Yu/rag/bge-large-zh-v1.5"
        self.model = SentenceTransformer(self.path)

    def generate_embeddings(self, text_list):
        embeddings = self.model.encode(text_list)
        return embeddings


if __name__ == "__main__":
        
    # from embedding import TextEmbeddingAPI
    embedding_api = TextEmbeddingAPI()
    split_data = ["文本1", "文本2", "文本3"]
    embeddings = embedding_api.generate_embeddings(split_data)
