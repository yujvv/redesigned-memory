from langchain.embeddings import HuggingFaceBgeEmbeddings
model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为这个句子生成表示以用于检索相关文章："
)
model.query_instruction = "为这个句子生成表示以用于检索相关文章："




# from langchain.embeddings import HuggingFaceBgeEmbeddings
 
# bge_embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-zh-v1.5")
 
# vectordb = DocArrayInMemorySearch.from_texts(
#     ["青蛙是食草动物",
#      "人是由恐龙进化而来的。",
#      "熊猫喜欢吃天鹅肉。",
#      "1+1=5",
#      "2+2=8",
#      "3+3=9",
#     "Gemini Pro is a Large Language Model was made by GoogleDeepMind",
#      "A Language model is trained by predicting the next token"
#     ],
#     embedding=bge_embeddings 
# )
 
# # #创建检索器
# bge_retriever = vectordb.as_retriever(search_kwargs={"k": 1})


# bge_retriever.get_relavant_documents()