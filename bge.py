from transformers import AutoTokenizer, AutoModel
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.schema import Document
from langchain.indexes import VectorstoreIndexCreator
from sentence_transformers import SentenceTransformer

# EMBEDDING_PATH = r"D:/Yu/rag/bge-large-zh-v1.5"
EMBEDDING_PATH = "D:/Yu/rag/bge-large-zh-v1.5"
# tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_PATH)
# model = AutoModel.from_pretrained(EMBEDDING_PATH).half().cuda()
# bge_embedding_model = model.eval()

# tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_PATH, trust_remote_code=True)
# model = AutoModel.from_pretrained(EMBEDDING_PATH, trust_remote_code=True).half().cuda()
# bge_embedding_model = model.eval()

# encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

# with torch.no_grad():
#     model_output = model(**encoded_input)
#     # Perform pooling. In this case, cls pooling.
#     sentence_embeddings = model_output[0][:, 0]
# # normalize embeddings
# sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
# print("Sentence embeddings:", sentence_embeddings)

bge_embedding_model = SentenceTransformer(EMBEDDING_PATH)

sentences_1 = ["样例数据-1", "样例数据-2"]
sentences_2 = ["样例数据-3", "样例数据-4"]

embeddings_1 = bge_embedding_model.encode(sentences_1, normalize_embeddings=True)
embeddings_2 = bge_embedding_model.encode(sentences_2, normalize_embeddings=True)

similarity = embeddings_1 @ embeddings_2.T
print(similarity)



# For s2p(short query to long passage) retrieval task, each short query should start with an instruction (instructions see Model List). But the instruction is not needed for passages.