import os
from typing import List, Tuple

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

class DocumentSearchAPI:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.faiss_index = None

    def load_documents(self, file_path: str) -> List[str]:
        loader = TextLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        split_documents = text_splitter.split_documents(documents)
        return split_documents

    def create_index(self, split_documents: List[str]) -> None:
        # Uncomment the following line if you need to initialize FAISS with no AVX2 optimization
        # os.environ['FAISS_NO_AVX2'] = '1'
        self.faiss_index = FAISS.from_documents(split_documents, self.embedding_model)

    def search(self, query: str) -> List[Tuple[str, float]]:
        if self.faiss_index is None:
            raise ValueError("Index not created. Call create_index() first.")

        docs_and_scores = self.faiss_index.similarity_search_with_score(query)
        return [(doc.page_content, score) for doc, score in docs_and_scores]

    def save_index(self, file_path: str) -> None:
        if self.faiss_index is None:
            raise ValueError("Index not created. Call create_index() first.")

        self.faiss_index.save_local(file_path)

    def load_index(self, file_path: str) -> None:
        self.faiss_index = FAISS.load_local(file_path, self.embedding_model)
        # docs = self.faiss_index.similarity_search(query)

# # Initialize the embedding model
# embedding_model = OpenAIEmbeddings()
# # Create an instance of the DocumentSearchAPI
# api = DocumentSearchAPI(embedding_model)
# # Load documents from a file
# split_documents = api.load_documents("../../modules/state_of_the_union.txt")
# # Create the FAISS index
# api.create_index(split_documents)
# # Search for a query
# query = "What did the president say about Ketanji Brown Jackson"
# results = api.search(query)
# print(results[0][0])  # Print the top result's content
# # Save the index
# api.save_index("faiss_index")
# # Load the index from the saved file
# api.load_index("faiss_index")
# # Search again after loading the index
# results = api.search(query)
# print(results[0][0])
        

# Easily use it in other LangChain methods
# retriever = db.as_retriever()
# docs = retriever.invoke(query)
# print(docs[0].page_content)