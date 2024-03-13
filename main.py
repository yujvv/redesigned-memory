import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain
from langchain.chains import RetrievalQAWithSourcesChain

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
  ChatPromptTemplate,
  SystemMessagePromptTemplate,
  HumanMessagePromptTemplate
)


os.environ["OPENAI_API_KEY"] = 'sk-'

embeddings = OpenAIEmbeddings()

# # 持久化数据
# docsearch = Chroma.from_documents(documents, embeddings, persist_directory="D:/vector_store")
# docsearch.persist()

# 加载数据
docsearch = Chroma(persist_directory="D:\github\langchain-debug\Chroma", embedding_function=embeddings)

# 通过向量存储初始化检索器
retriever = docsearch.as_retriever()

# query = "德国举行的科隆游戏展中，米哈游的绝零区的实机演示有多久？"
# docs = docsearch.similarity_search(query, include_metadata=True)

# llm = OpenAI(temperature=0)
# chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
# chain.run(input_documents=docs, question=query)

# with the tone and personality of the protagonist as described in the context
# Pretend you are the character in the following context description. 
# todo 
# 增加角色扮演，解决token数量限制。
# https://github.com/langchain-ai/langchain/issues/2333
system_template = """
Use the following context to answer the user's question.
If you don't know the answer, say you don't, don't try to make it up. And answer in Chinese.
-----------
{question}
-----------
{chat_history}
"""

# 构建初始 messages 列表，这里可以理解为是 openai 传入的 messages 参数
messages = [
  SystemMessagePromptTemplate.from_template(system_template),
  HumanMessagePromptTemplate.from_template('{question}')
]

# 初始化 prompt 对象
prompt = ChatPromptTemplate.from_messages(messages)

# def get_chain(store):
#     chain_type_kwargs = {"prompt": prompt}
#     chain = RetrievalQAWithSourcesChain.from_chain_type(
#         ChatOpenAI(temperature=0), 
#         chain_type="stuff", 
#         retriever=store.as_retriever(),
#         chain_type_kwargs=chain_type_kwargs,
#         reduce_k_below_max_tokens=True
#     )
#     return chain

# 初始化问答链
qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.1,max_tokens=2048),retriever,condense_question_prompt=prompt,reduce_k_below_max_tokens=True)

chat_history = []
while True:
  question = input('问题：')
  # 开始发送问题 chat_history 为必须参数,用于存储对话历史
  result = qa({'question': question, 'chat_history': chat_history})
  chat_history.append((question, result['answer']))
  print(result['answer'])

