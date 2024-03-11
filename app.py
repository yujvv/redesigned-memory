
from transformers import AutoTokenizer, AutoModel
from langchain.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer

from langchain import PromptTemplate, LLMChain
from langchain.llms import CTransformers
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceBgeEmbeddings
from io import BytesIO
from langchain.document_loaders import PyPDFLoader
import gradio as gr

# --------------- LLM model

PATH = "D:/Yu/rag/chatglm3-6b"
tokenizer = AutoTokenizer.from_pretrained(PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(PATH, trust_remote_code=True).half().cuda()
model = model.eval()

prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

prompt = ChatPromptTemplate.from_template(template)


# --------------- embedding model

# EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
# queries = ['query_1', 'query_2']
# passages = ["样例文档-1", "样例文档-2"]
# instruction = "为这个句子生成表示以用于检索相关文章："

# model = SentenceTransformer(EMBEDDING_PATH)
# q_embeddings = model.encode([instruction+q for q in queries], normalize_embeddings=True)
# p_embeddings = model.encode(passages, normalize_embeddings=True)
# scores = q_embeddings @ p_embeddings.T


# print(scores)


model_name = "D:/Yu/rag/bge-large-zh-v1.5"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
load_vector_store = Chroma(persist_directory="stores/pet_cosine", embedding_function=embeddings)
retriever = load_vector_store.as_retriever(search_kwargs={"k":1})



# langchain prompt chain

# chain = RunnableMap({
#     "context": lambda x: bge_retriever.get_relevant_documents(x["question"]),
#     "question": lambda x: x["question"]
# }) | prompt | model | StrOutputParser()


sample_prompts = ["what is the fastest speed for a greyhound dog?", "Why should we not feed chocolates to the dogs?", "Name two factors which might contribute to why some dogs might get scared?"]

def get_response(input):
    query = input
    chain_type_kwargs = {"prompt": prompt}
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs=chain_type_kwargs, verbose=True)
    response = qa(query)
    return response