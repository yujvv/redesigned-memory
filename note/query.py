import os
import platform
from transformers import AutoTokenizer, AutoModel
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser


PATH = "D:/Yu/rag/chatglm3-6b"
tokenizer = AutoTokenizer.from_pretrained(PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(PATH, trust_remote_code=True).half().cuda()
model = model.eval()

# response, history = model.chat(tokenizer, "你好", history=[])
# print(response)
# response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
# print(response)



#创建model
# model = ChatGoogleGenerativeAI(model="gemini-pro")
 
#创建prompt模板
template = """Answer the question a full sentence, 
based only on the following context:
{context}
Question: {question}
"""
 
#由模板生成prompt
prompt = ChatPromptTemplate.from_template(template)
 
#创建chain
chain = RunnableMap({
    "context": lambda x: bge_retriever.get_relevant_documents(x["question"]),
    "question": lambda x: x["question"]
}) | prompt | model | StrOutputParser()


