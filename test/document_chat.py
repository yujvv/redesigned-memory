from langchain.chains import RetrievalQA
from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
from utils import load_embeddings, load_db
from ChatGLM3 import ChatGLM3

load_dotenv()

PATH = "D:/Yu/rag/chatglm3-6b"
llm = ChatGLM3()
llm.load_model(PATH)


class retrieval_chat():

    def __init__(self) -> None:
        
        embedding_function = load_embeddings()

        db = load_db(embedding_function)

        self.qa_model = RetrievalQA.from_llm(llm=llm, retriever=db.as_retriever(kwargs={"k": 3}), return_source_documents=True)

    def answer_question(self, question :str):
        output = self.qa_model.invoke({"query": question})
        #print("Source Documents: ")
        #print(output["source_documents"])
        return output["result"]

if __name__ == "__main__":
    qa_chat = retrieval_chat()
    while True:
        print("Whats Your Question:")
        query = input()
        if query == "exit":
            break
        print(qa_chat.answer_question(query))
