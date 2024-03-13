from sentence_transformers import SentenceTransformer


EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
# model = SentenceTransformer(EMBEDDING_PATH)

queries = ['query_1', 'query_2']
passages = ["样例文档-1", "样例文档-2"]
instruction = "为这个句子生成表示以用于检索相关文章："

model = SentenceTransformer(EMBEDDING_PATH)
q_embeddings = model.encode([instruction+q for q in queries], normalize_embeddings=True)
p_embeddings = model.encode(passages, normalize_embeddings=True)
scores = q_embeddings @ p_embeddings.T


print(scores)