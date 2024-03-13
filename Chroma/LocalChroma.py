import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings


os.environ["OPENAI_API_KEY"] = 'sk-'

# loader = DirectoryLoader('../', glob='**/*.txt')
loader = DirectoryLoader('./', glob='data.txt')
# 将数据转成 document 对象
documents = loader.load()

# 初始化加载器
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
# 切割加载的 document
split_docs = text_splitter.split_documents(documents)

index_name="localMemory"

# embeddings = OpenAIEmbeddings()

from sentence_transformers import SentenceTransformer

EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
model = SentenceTransformer(EMBEDDING_PATH)
embeddings = model.encode(split_docs, normalize_embeddings=True)


# 持久化数据
docsearch = Chroma.from_documents(documents, embeddings, persist_directory="./ChromaIndex")
docsearch.persist()

# 加载数据
# docsearch = Chroma(persist_directory="D:/vector_store", embedding_function=embeddings)
