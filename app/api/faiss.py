import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

PATH = "D:/Yu/rag/bge-large-zh-v1.5"

class Faiss_GPU:
    def __init__(self, name, path, embedding_model=PATH):
        self.name = name
        self.path = path
        self.embedder = SentenceTransformer(embedding_model)
        self.load_or_create_index()

    # The load_or_create_index method loads the faiss index from a pickle file if it exists, or creates a new index if it doesn't.
    def load_or_create_index(self):
        try:
            with open(f"{self.path}/{self.name}.pkl", "rb") as f:
                self.index = pickle.load(f)
        except FileNotFoundError:
            self.index = faiss.IndexFlatIP(self.embedder.get_sentence_embeddings("").shape[0])

    # The add method embeds the keys using the sentence transformer, checks if any of the embeddings already exist in the index, and adds the new embeddings to the index along with their corresponding indices.
    def add(self, data):
        keys = list(data.keys())
        embeddings = self.embedder.encode(keys)
        ids = np.arange(len(keys))
        indices_to_add = []
        for i, emb in zip(ids, embeddings):
            if not np.any(np.all(self.index.vector_data == emb, axis=1)):
                indices_to_add.append(i)
        if indices_to_add:
            self.index.add(np.array([embeddings[i] for i in indices_to_add]))
            for i, idx in zip(indices_to_add, self.index.ntotal - len(indices_to_add) + np.array(indices_to_add)):
                data[keys[i]] = idx
            with open(f"{self.path}/{self.name}.pkl", "wb") as f:
                pickle.dump(self.index, f)

    # The query method takes a query string as input and returns the top k most similar embeddings and their corresponding indices, along with their similarity scores.
    def query(self, query_text, k=5):
        query_embedding = self.embedder.encode([query_text])[0]
        distances, indices = self.index.search(np.array([query_embedding]), k)
        return [(1 - distances[0][i], indices[0][i]) for i in range(k)]

    # The delete method takes a key string as input, embeds it, checks if the embedding exists in the index, and if so, removes it from the index and saves the updated index to a pickle file.
    def delete(self, key):
        key_embedding = self.embedder.encode([key])[0]
        indices_to_delete = np.flatnonzero(np.all(self.index.vector_data == key_embedding, axis=1))
        if indices_to_delete.size > 0:
            self.index.remove_ids(indices_to_delete)
            with open(f"{self.path}/{self.name}.pkl", "wb") as f:
                pickle.dump(self.index, f)
        else:
            return None
        


# faiss_gpu = Faiss_GPU("my_index", "path/to/index/directory")

# # Add some data
# faiss_gpu.add({"apple": 0, "banana": 1, "orange": 2})

# # Query for similar items
# results = faiss_gpu.query("fruit")
# print(results)  # [(0.8, 0), (0.7, 1), (0.6, 2)]

# # Delete an item
# faiss_gpu.delete("apple")
        



# 我认为你很熟悉faiss-gpu，对吗？
# 我希望你能仔细学习faiss的开发指示，帮助我构建一系列python的api，关于faiss-gpu。
# 具体有如下函数功能：
# 传入两个参数，name和path，维护一个本地的pkl的faiss向量数据库，如果对应path的{name}.pkl不存在，就新建一个faiss向量数据库，否则加载为类变量。
# 添加：传入一个字典，key是一串字符串，而velue是一个index。调用作为参数传入的embedding模型（SentenceTransformer初始化后的），将key进行embedding处理后得到embedding key，将其更新到faiss向量数据库中；如果已经有了完全一致的embedding key，那么返回null，否则加到原有的faiss向量数据库。
# 查询：传入一个query（字符串类型），通过embedding处理后，在faiss的向量数据库中寻找最相近的前k个embedding key，返回这k个的相似分数以及其对应index。
# 删除：传入一个key，是一串字符串，经过embedding处理后，得到embedding key，查询faiss向量数据库中是否有完全相似的embedding key，若有，则删除这个item并更新faiss向量数据库，否则返回null。