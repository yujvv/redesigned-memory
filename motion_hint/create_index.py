from langchain_community.vectorstores import FAISS
from utils import load_documents, save_db
from langchain.embeddings import HuggingFaceBgeEmbeddings
model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为这个句子生成表示以用于检索相关文章："
)
# model.query_instruction = "为这个句子生成表示以用于检索相关文章："
embedding_function = model
# embedding_function = load_embeddings()

documents = load_documents("data/")

db = FAISS.from_documents(documents, embedding_function)
print("Index Created")
save_db(db)

print(db.similarity_search("huawei f50"))
