# !pip install accelerate==0.21.0 transformers==4.31.0 tokenizers==0.13.3
# !pip install bitsandbytes==0.40.0 einops==0.6.1
# !pip install xformers==0.0.22.post7
# !pip install langchain==0.1.4
# !pip install faiss-gpu==1.7.1.post3
# !pip install sentence_transformers


# from langchain.document_loaders import WebBaseLoader

# web_links = ["https://www.databricks.com/","https://help.databricks.com","https://databricks.com/try-databricks","https://help.databricks.com/s/","https://docs.databricks.com","https://kb.databricks.com/","http://docs.databricks.com/getting-started/index.html","http://docs.databricks.com/introduction/index.html","http://docs.databricks.com/getting-started/tutorials/index.html","http://docs.databricks.com/release-notes/index.html","http://docs.databricks.com/ingestion/index.html","http://docs.databricks.com/exploratory-data-analysis/index.html","http://docs.databricks.com/data-preparation/index.html","http://docs.databricks.com/data-sharing/index.html","http://docs.databricks.com/marketplace/index.html","http://docs.databricks.com/workspace-index.html","http://docs.databricks.com/machine-learning/index.html","http://docs.databricks.com/sql/index.html","http://docs.databricks.com/delta/index.html","http://docs.databricks.com/dev-tools/index.html","http://docs.databricks.com/integrations/index.html","http://docs.databricks.com/administration-guide/index.html","http://docs.databricks.com/security/index.html","http://docs.databricks.com/data-governance/index.html","http://docs.databricks.com/lakehouse-architecture/index.html","http://docs.databricks.com/reference/api.html","http://docs.databricks.com/resources/index.html","http://docs.databricks.com/whats-coming.html","http://docs.databricks.com/archive/index.html","http://docs.databricks.com/lakehouse/index.html","http://docs.databricks.com/getting-started/quick-start.html","http://docs.databricks.com/getting-started/etl-quick-start.html","http://docs.databricks.com/getting-started/lakehouse-e2e.html","http://docs.databricks.com/getting-started/free-training.html","http://docs.databricks.com/sql/language-manual/index.html","http://docs.databricks.com/error-messages/index.html","http://www.apache.org/","https://databricks.com/privacy-policy","https://databricks.com/terms-of-use"]

# 华为光产品公开安装文档
# https://support.huawei.com/enterprise/zh/optical-access/smartax-ma5600t-pid-18133

# loader = WebBaseLoader(web_links)
# documents = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
# https://python.langchain.com/docs/modules/data_connection/document_transformers/

# 从文件中读取文本
file_path = "hg8346m-olt.txt"

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# 将文本加载到 documents 中
# documents.append(text)

# Splitting in Chunks using Text Splitters

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
# all_splits = text_splitter.split_documents(text)

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=0
)
all_splits = text_splitter.split_text(text)

print("------------", all_splits)

# Creating Embeddings and Storing in Vector Store
# You have to create embeddings for each small chunk of text and store them in the vector store (i.e. FAISS). You will be using `all-mpnet-base-v2` Sentence Transformer to convert all pieces of text in vectors while storing them in the vector store.

# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"

# model_name = "sentence-transformers/all-mpnet-base-v2"
# model_kwargs = {"device": "cuda"}

# embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

bge_embedding_model = SentenceTransformer(EMBEDDING_PATH)


embeddings = bge_embedding_model.encode(all_splits, normalize_embeddings=True)



# storing embeddings in the vector store
vectorstore = FAISS.from_documents(all_splits, embeddings)


from langchain.chains import ConversationalRetrievalChain

chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), return_source_documents=True)


chat_history = []

query = "What is Data lakehouse architecture in Databricks?"
result = chain({"question": query, "chat_history": chat_history})

print(result['answer'])

print(result['source_documents'])
