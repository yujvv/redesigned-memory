# pip install langchain faiss-cpu python-magic-bin
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain import VectorDBQA, DocQuery
from langchain.document_loaders import UnstructuredPDFLoader, UnstructuredFileLoader
from PIL import Image
import os
# from api.embedding import TextEmbeddingAPI 
from api.chatglm import ChatGLMInterface

# Load the data and split the text into smaller chunks for efficient embedding.

# Load text data
text_file = UnstructuredFileLoader("1.txt").load()
texts = text_file.split("\n\n")

# Load PDF data
pdf_loader = UnstructuredPDFLoader("1.pdf")
pdf_data = pdf_loader.load()

# Load image data
images = [Image.open(f) for f in ["1.png", "2.png"]]

# Split text into chunks
text_splitter = CharacterTextSplitter()
docs = []
for pdf in pdf_data:
    docs.extend(text_splitter.split_documents(pdf.page_content))
for text in texts:
    docs.extend(text_splitter.split_documents(text))

# Create embedding model
from sentence_transformers import SentenceTransformer
EMBEDDING_MODEL_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
embeddings = SentenceTransformer(EMBEDDING_MODEL_PATH)


# Create and store the vector database
# Generate embeddings and store in FAISS
db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_db")  # Save the database to a local file

# Create the question-answering pipeline
qa = VectorDBQA.from_chain_type(
    llm=None,
    chain_type="stuff",
    vectorstore=db,
    return_source_documents=True,
)

def generate_response(prompt):
    language_model_interface = ChatGLMInterface()
    response = language_model_interface.generate_response(prompt, False)
    return response

# def generate_embeddings(texts):
#     embedding_api = TextEmbeddingAPI()
#     embeddings = embedding_api.generate_embeddings(texts)
#     return embeddings


print(generate_response("What is the main topic of the text?"))