from flask import Flask, request, jsonify
from utils import load_db
from langchain.embeddings import HuggingFaceBgeEmbeddings
from motion_hint import ActionSemanticRetriever

app = Flask(__name__)

model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为这个句子生成表示以用于检索相关文章："
)


actions_semantics = {
    1: "这一点需要特别强调和解释。",
    2: "我会详细解释给你听。",
    3: "很高兴长时间问候你。",
    4: "我用左手指向前方给你指引。",
    5: "我用右手指向前方给你指引。",
    6: "暂时不做任何动作。",
    7: "交给我来处理。",
    8: "我指向并引用这一点。",
    9: "我会展示并指引你。",
    10: "这里有一些选择给你。",
    11: "我用右手指向右侧呈现给你。",
    12: "我双手举起欢迎你。",
    13: "我用右手指向右侧，逐点解释给你。",
    14: "我摇头表示否定。",
    15: "我表示尊重。",
    16: "我交叉双臂表示拒绝。",
    17: "我挥动右手表示确认。",
    18: "我点头表示同意。",
    19: "暂时不做任何动作，等待25秒。",
    20: "暂时不做任何动作，等待46秒。"
}



# Load embeddings and database
embedding_function = model
db = load_db(embedding_function)


def extract_core_text(documents):
    core_text_set = set() 
    for document in documents:
        core_text_set.add(document.page_content) 

    core_text = '\n'.join(core_text_set)
    return core_text



@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        print("start!")
        data = request.get_json()
        print("get query:", data)
        # Check if 'query' key exists in JSON data
        if 'query' not in data:
            return jsonify({"error": "Missing 'query' parameter"}), 400

        query = data['query']
        # Perform similarity search
        context = db.similarity_search(query, k=2)
        core_text = extract_core_text(context)
        return jsonify({"context": core_text})

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500
    
@app.route('/motionHint', methods=['POST'])
def ask_motion():
    try:
        print("start!")
        data = request.get_json()
        print("get response:", data)
        # Check if 'query' key exists in JSON data
        if 'response' not in data:
            return jsonify({"error": "Missing 'response' parameter"}), 400

        response = data['response']
        # Perform similarity search
        embedding_model = model

        retriever = ActionSemanticRetriever(embedding_model, actions_semantics)

        relevant_actions = retriever.query_actions(response)
        for action, semantic, score in relevant_actions:
            print(f'Action: {action}, Semantic: {semantic}, Score: {score}')

        return relevant_actions[0][action]
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run Flask app using a production-ready WSGI server
    app.run(host='0.0.0.0', port=5000)



# import requests

# url = 'http://<flask_app_ip>:5000/ask'
# question = 'Your question goes here'

# response = requests.post(url, json={'query': query})
# data = response.json()

# print("context:", data['context'])
