from flask import Flask, request, jsonify
import time
from api.faiss_api import Faiss_GPU
from api.loader_docx import Loader
from api.chatglm import ChatGLMInterface

app = Flask(__name__)

# Function to build dictionary from content list
def build_dict(content_list):
    result_dict = {}
    title_dict = {}
    for item in content_list:
        result_dict[item["content"]] = item["index"]
        title_dict[item["content"]] = item["title"]
    return result_dict, title_dict


# Initialize models
loader = Loader()
docx_file = '2test.docx'
content_list = loader.extract_content(docx_file)
result_dict, title_dict = build_dict(content_list)
faiss_gpu = Faiss_GPU("2test.docx", "./index")
faiss_gpu.add(result_dict)
# language_model_interface = ChatGLMInterface()


# Function to process input and return response
def process_input(user_input):
    results = faiss_gpu.query_index(user_input, result_dict, title_dict)
    top = results[0][0]
    title = results[0][3]
    # prompt = f"你好，你是我的车内助手。请基于背景，帮我温柔地回答问题。\nContext:{top}\nQ: {user_input}\nA:"
    # output = language_model_interface.generate_response(prompt, False)

    # score = results[0][2]
    # if score > 0.4:
    #     hint = "(知识来源于《" + title + "》章节)"
    # else:
    #     hint = "(提供的背景中没有相关的知识)"
    # bot = output + hint

    return top, title

# Route for receiving text input and returning processed text and image name
@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    user_input = data['user_input']
    top, title = process_input(user_input)
    bot_response, image_name = top, title

    return jsonify({'bot_response': bot_response, 'image_name': image_name})

if __name__ == '__main__':
    app.run(debug=True)
