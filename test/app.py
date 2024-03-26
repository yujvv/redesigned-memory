from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain import VectorDBQA, DocQuery
from langchain.document_loaders import UnstructuredPDFLoader, UnstructuredFileLoader
from langchain.docstore.document import Document
from PIL import Image
import pytesseract
import os
from sentence_transformers import SentenceTransformer
from api.chatglm import ChatGLMInterface

EMBEDDING_MODEL_PATH = "D:/Yu/rag/bge-large-zh-v1.5"

# Set up OCR
pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'  # Replace with your Tesseract installation path

# Load and process data
embeddings = SentenceTransformer(EMBEDDING_MODEL_PATH)
text_splitter = CharacterTextSplitter()

def load_text_data(file_path):
    loader = UnstructuredFileLoader(file_path)
    data = loader.load()
    texts = data.split("\n\n")
    docs = [text_splitter.split_documents(text) for text in texts]
    docs = [doc for sub_docs in docs for doc in sub_docs]
    return docs

def load_pdf_data(file_path):
    loader = UnstructuredPDFLoader(file_path)
    data = loader.load()
    docs = [text_splitter.split_documents(doc.page_content) for doc in data]
    docs = [doc for sub_docs in docs for doc in sub_docs]
    return docs

def load_image_data(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    docs = text_splitter.split_documents(text)
    return docs

def create_vector_db(text_files, pdf_files, image_files):
    docs = []
    for text_file in text_files:
        docs.extend(load_text_data(text_file))
    for pdf_file in pdf_files:
        docs.extend(load_pdf_data(pdf_file))
    for image_file in image_files:
        docs.extend(load_image_data(image_file))

    db = FAISS.from_documents(docs, embeddings)
    return db

def setup_qa_chain(vector_db):
    qa = VectorDBQA.from_chain_type(
        llm=None,
        chain_type="stuff",
        vectorstore=vector_db,
        return_source_documents=True,
    )
    return qa


def generate_response(qa, prompt):
    language_model_interface = ChatGLMInterface()
    result = qa({"query": prompt})
    response = language_model_interface.generate_response(result, False)
    # result["result"]
    return response

# Example usage
text_files = ["f50.txt"]
pdf_files = []
image_files = ["1.png", "2.png", "3.png"]

vector_db = create_vector_db(text_files, pdf_files, image_files)
qa_chain = setup_qa_chain(vector_db)

prompt = "What is the OptiXsense f50?"
response = generate_response(qa_chain, prompt)
print(response)