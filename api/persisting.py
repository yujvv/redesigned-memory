import faiss
import numpy as np

class Persisting:
    def __init__(self, embeddings=None, chunk_ids=None, chunks=None, index_file=None):
        self.embeddings = embeddings
        self.chunk_ids = chunk_ids
        self.chunks = chunks
        self.index = None
        if index_file:
            self.load_index(index_file)
        elif embeddings is not None:
            self.index = self._create_faiss_index()

    def _create_faiss_index(self):
        d = self.embeddings.shape[1]  # 向量维度
        index = faiss.IndexFlatL2(d)  # 使用 FlatL2 索引
        index.add(self.embeddings.astype(np.float32))  # 添加向量到索引中
        return index

    def load_index(self, index_file):
        self.index = faiss.read_index(index_file)

    def save_index(self, index_file):
        faiss.write_index(self.index, index_file)

    def search_similar_chunks(self, query_embedding, k=5):
        similar_chunk_ids, distances = self._search_faiss_index(query_embedding, k)
        similar_chunks = [self.chunks[chunk_id] for chunk_id in similar_chunk_ids]
        return similar_chunk_ids, similar_chunks, distances

    def _search_faiss_index(self, query_embedding, k):
        D, I = self.index.search(query_embedding.reshape(1, -1).astype(np.float32), k)  # 执行查询
        return [self.chunk_ids[i] for i in I.flatten()], D.flatten()


if __name__ == "__main__":

    # 假设 sentence_embeddings 是你的句子向量列表，chunk_ids 是你的 chunk 唯一标识列表，chunks 是 chunk 内容列表
    Persisting_api = ChunkSearchAPI(sentence_embeddings, chunk_ids, chunks)
    Persisting_api.save_index("faiss_index.index")

    # 查询示例
    query_vector = np.random.rand(sentence_embeddings.shape[1])  # 假设这是你的查询向量
    similar_chunk_ids, similar_chunks, distances = Persisting_api.search_similar_chunks(query_vector, k=5)

    # 输出结果
    print("Similar Chunk IDs:", similar_chunk_ids)
    print("Similar Chunks:", similar_chunks)
    print("Distances:", distances)
