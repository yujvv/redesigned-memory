from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI
# from langchain.callbacks import get_openai_callback
from langchain.embeddings import HuggingFaceBgeEmbeddings
from ChatGLM3 import ChatGLM3


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 💬")
    
    # upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")
    
    # extract the text
    if pdf is not None:
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
        
      # split into chunks
      text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
      )
      chunks = text_splitter.split_text(text)
      
      # create embeddings
      # embeddings = OpenAIEmbeddings()

      model_name = "BAAI/bge-large-en-v1.5"
      model_kwargs = {'device': 'cuda'}
      encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
      embeddings = HuggingFaceBgeEmbeddings(
          model_name=model_name,
          model_kwargs=model_kwargs,
          encode_kwargs=encode_kwargs,
          query_instruction="为这个句子生成表示以用于检索相关文章："
      )
      knowledge_base = FAISS.from_texts(chunks, embeddings)
      
      # show user input
      user_question = st.text_input("Ask a question about your PDF:")
      if user_question:
        docs = knowledge_base.similarity_search(user_question)
        
        # llm = OpenAI()
        PATH = "D:/Yu/rag/chatglm3-6b"
        llm = ChatGLM3()
        llm.load_model(PATH)
        chain = load_qa_chain(llm, chain_type="stuff")

        response = chain.run(input_documents=docs, question=user_question)
        print(response)
           
        st.write(response)
    

if __name__ == '__main__':
    main()
