# Uncomment the following line if you need to initialize FAISS with no AVX2 optimization
# os.environ['FAISS_NO_AVX2'] = '1'
# https://python.langchain.com/docs/integrations/vectorstores/faiss

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

loader = TextLoader("../../modules/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(docs, embeddings)
print(db.index.ntotal)


query = "What did the president say about Ketanji Brown Jackson"

# docs = db.similarity_search(query)
# print(docs[0].page_content)

# easily use it in other LangChain methods
retriever = db.as_retriever()
docs = retriever.invoke(query)
print(docs[0].page_content)

# The returned distance score is L2 distance
docs_and_scores = db.similarity_search_with_score(query)
print(docs_and_scores[0])

# Search with a given embedding vector
embedding_vector = embeddings.embed_query(query)
docs_and_scores = db.similarity_search_by_vector(embedding_vector)

# Save and load a FAISS index
db.save_local("faiss_index")
new_db = FAISS.load_local("faiss_index", embeddings)
docs = new_db.similarity_search(query)
# docs[0]

# todo, filtering, Merging, Delete