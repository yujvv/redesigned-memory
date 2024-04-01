from flask import Flask, request, jsonify
from utils import load_embeddings, load_db

app = Flask(__name__)

embedding_function = load_embeddings()

db = load_db(embedding_function)


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    query = data['query']
    context = db.similarity_search(query, k=3)
    return jsonify({"context": context})

if __name__ == "__main__":
    # my ip
    app.run(host='0.0.0.0', port=5000)



# import requests

# url = 'http://<flask_app_ip>:5000/ask'
# question = 'Your question goes here'

# response = requests.post(url, json={'query': query})
# data = response.json()

# print("context:", data['context'])
