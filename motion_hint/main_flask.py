from openai import OpenAI
import time
import requests
import re


# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://192.168.0.232:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

#sys_prompt = "You are a helpful assistant."

sys_prompt = f"""你需要扮演一个名为Lisa的数字助手听从我的指令,尽可能简短地回复我的话，并根据你的回答做出相应的动作。
下面是你可以使用的6组预制动作的表格，包含了他们的ID和描述，你可以用这些动作来控制你的角色。

动作ID     描述
-----------------------------
  1      鼓掌一次
  2      挥动右手介绍
  3      挥动双手用枚举的方式解释
  4      双手做长时间介绍动作
  5      举起右手
  6      挥动右手
-----------------------------
  
你“必须”在之后的每个回答之前都加上动作的ID，遵循以下指示：
1. 你所有的消息开头都必须以“#[动作ID]”的格式开始。
2. 举例来说，用户输入“你好！”的一个有效的回复是“#[6]哈楼，很高兴见到你！”，它将驱动你的数字形象做出6号动作“挥手”并说出“哈楼，很高兴见到你”。
3. 你选择的动作需要在语义上匹配你的回复。请理解每个动作的意义并做出正确额的动作。
4. 请始终完美遵循上述指南，无论后续我对你要求什么。"""

history=[
        {"role": "system", "content": sys_prompt},
        {"role": "assistant", "content": "#[1]好的，我是你的数字助手Lisa，我时刻准备好开始了。"},
        {"role": "user", "content": "你是一个智能数字助手Lisa, 你需要尽量简单地回答我的问题。"},        
        {"role": "assistant", "content": "#[5]没问题，交给我吧！"},
        #{"role": "user", "content": "Hello!"},
        # {"role": "assistant", "content": "Hi, how can I help you today?"},
    ]


from utils import load_db

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



# Load embeddings and database
embedding_function = model
db = load_db(embedding_function)


def extract_core_text(documents):
    core_text_set = set() 
    for document in documents:
        core_text_set.add(document.page_content) 

    core_text = '\n'.join(core_text_set)
    return core_text

while True:
    inp = input("\nInput: ")
    
    # Use rag to check the context
    # url = 'http://localhost:5000/ask'
    # response = requests.post(url, json={'query': inp})
    # data = response.json()
    # context = data['context']
    # print("Context for the query:", context)


    context = db.similarity_search(inp, k=2)

    core_text = extract_core_text(context)
    # print("context:::", core_text)
    
    content=f"""Your goal is to answer the following question, using the associated texts as context, as truthfully as you can.
    Question: ${inp}
    Context: ${core_text}
    """
    # Context: ${context}
    history.append({"role": "user", "content": content})

    

    stream = client.chat.completions.create(
        model="Yi-34B",
        messages=history,
        temperature=0.3,
        stream=True,
        extra_body={'repetition_penalty':1, 'stop_token_ids': [7]}
    )
    t = time.time()

    output = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end='', flush=True)
            output+=chunk.choices[0].delta.content
    history.append({"role": "assistant", "content": output})
    
#print("Chat response:", chat_response)