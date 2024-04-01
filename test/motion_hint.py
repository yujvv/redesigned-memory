import faiss
from sentence_transformers import SentenceTransformer

EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
model = SentenceTransformer(EMBEDDING_PATH)
# sentence_embeddings = model.encode(split_data)

class ActionSemanticRetriever:
    def __init__(self, embedding_model, actions_semantics):
        self.embedding_model = embedding_model
        self.actions_semantics = actions_semantics
        self.index = self._build_index()

    def _build_index(self):
        # Compute embeddings for semantics
        semantics = list(self.actions_semantics.values())
        embeddings = self.embedding_model.encode(semantics)

        # Build FAISS index
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        return index

    def query_actions(self, query, k=1):
        # Compute embedding for the query
        query_embedding = self.embedding_model.encode([query])[0]

        # Search for similar vectors in the index
        scores, indices = self.index.search(query_embedding.reshape(1, -1), k)

        # Return relevant actions
        relevant_actions = []
        for score, idx in zip(scores[0], indices[0]):
            action = list(self.actions_semantics.keys())[idx]
            semantic = self.actions_semantics[action]
            relevant_actions.append((action, semantic, score))

        return relevant_actions

# Example usage
actions_semantics = {
    'open_file': 'Open a file in the current directory',
    'save_file': 'Save the current file with a new name',
    'search_text': 'Search for specific text within the file',
    'replace_text': 'Replace text in the file with new text',
    # Add more actions and semantics here
}

# Assume you have an embedding model instance
embedding_model = model

retriever = ActionSemanticRetriever(embedding_model, actions_semantics)

query = 'Find and replace specific text in a file'
relevant_actions = retriever.query_actions(query)
for action, semantic, score in relevant_actions:
    print(f'Action: {action}, Semantic: {semantic}, Score: {score}')