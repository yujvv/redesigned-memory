# pip install langchain
# pip install unstructured
# pip install pypdf
# pip install tiktoken
# pip install chromadb
# pip install openai
# https://abvijaykumar.medium.com/prompt-engineering-retrieval-augmented-generation-rag-cd63cdc6b00

import os
# import openai
import tiktoken
import chromadb

from langchain.document_loaders import OnlinePDFLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.memory import ConversationBufferMemory
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
# from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from sentence_transformers import SentenceTransformer
import os
import platform
from transformers import AutoTokenizer, AutoModel

# D:\Yu\rag\chatglm3-6b
# THUDM/chatglm3-6b
PATH = "D:/Yu/rag/chatglm3-6b"
tokenizer = AutoTokenizer.from_pretrained(PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(PATH, trust_remote_code=True).half().cuda()
model = model.eval()

# Create Vector Embeddings from the User Manual PDF and store it in ChromaDB

loader = PyPDFLoader("test.pdf")
pdfData = loader.load()

text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
splitData = text_splitter.split_documents(pdfData)

# Create a chroma collection, a local directory to store the chroma db.

collection_name = "clarett_collection"
local_directory = "clarett_vect_embedding"
persist_directory = os.path.join(os.getcwd(), local_directory)

openai_key=os.environ.get('OPENAI_API_KEY')
# embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
embeddings = SentenceTransformer(EMBEDDING_PATH)
# sentence_embeddings = model.encode(split_data)

vectDB = Chroma.from_documents(splitData,
                      embeddings,
                      collection_name=collection_name,
                      persist_directory=persist_directory
                      )
vectDB.persist()


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chatQA = ConversationalRetrievalChain.from_llm(
            # OpenAI(openai_api_key=openai_key,
            #    temperature=0, model_name="gpt-3.5-turbo"), 
            model,
            vectDB.as_retriever(), 
            memory=memory)

chat_history = []
qry = ""
while qry != 'done':
    qry = input('Question: ')
    if qry != exit:
        response = chatQA({"question": qry, "chat_history": chat_history})
        print(response["answer"])