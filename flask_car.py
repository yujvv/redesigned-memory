from flask import Flask, request, jsonify
from api.faiss_api import Faiss_GPU
from api.loader_docx import Loader
from datetime import datetime
import random
from api.reranker_index import RerankerIndex
from openai import OpenAI
# from api.chatglm import ChatGLMInterface

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
# hdl.docx
docx_file = 'M9Z.docx'
content_list = loader.extract_content(docx_file)
result_dict, title_dict = build_dict(content_list)
faiss_gpu = Faiss_GPU("demox85z4z1z", "./index")
faiss_gpu.add(result_dict)

reranker = RerankerIndex()

history = []

# language_model_interface = ChatGLMInterface()

def chatgpt(user_input, background_info, history):
    # Set your OpenAI API key

    client = OpenAI(api_key='')


    if len(history) > 3:
        history = history[-3:]

    prompt = (
        f"请你扮演一个专业的车辆助手，基于以下背景信息，简短且真实地回答我的问题。\n\n"
        f"### 背景信息:\n{background_info}\n\n"
        f"### 用户问题:\n{user_input}\n\n"
        f"### 请注意：要确保用户问题与提供的背景信息相关。如果背景信息无法完美解答用户问题，请促使用户提供更清晰的问题描述并基于背景信息猜测用户真正想要询问的问题（请不要提及背景信息与问题不一致的情况）。\n\n"
    )


    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "请你扮演一个专业的车辆助手，基于背景信息，简短且真实地回答用户问题。"},
            {"role": "user", "content": f"{prompt}"}
        ] + history  # 添加历史消息
    )

    # reply = response.choices[0].text.strip()
    reply = completion.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": f"{reply}"})

    return reply


def get_random_response():
    # responses = [
    #     "对不起，我无法找到相关信息。您是否可以提供更多详细信息或尝试其他查询？",
    #     "抱歉，我没有找到您需要的信息。也许可以尝试不同的关键词或进一步描述您的需求。",
    #     "很抱歉，没有找到相关内容。请您提供更多具体的细节或尝试另一个问题。",
    #     "我很遗憾没有找到目标信息。如果您有其他问题或需要更多帮助，请随时告诉我。",
    #     "对不起，我无法获取到您需要的资料。如果您有其他问题或需要特定的帮助，请告知，我会尽力帮您找到答案。"
    # ]
    responses = [    
        "[NOT FOUND]哎呀，对不起哦，我找不到相关信息。你可以给我更多细节吗？或者试试别的查询呢？",    
        "[NOT FOUND]抱抱~我没找到你需要的信息。要不要换个关键词或者再详细描述一下你的需求呢？",    
        "[NOT FOUND]呜呜，对不起，我没找到相关内容。你能不能提供更多具体的细节？或者问我其他问题也可以哦~",    
        "[NOT FOUND]很抱歉，我没找到你要的信息。如果还有其他问题或者需要更多帮助，随时告诉我哦~",    
        "[NOT FOUND]哦不，我没能找到你需要的资料。如果有其他问题或者需要特别的帮助，告诉我吧，我会尽力帮你的~"]

    
    return random.choice(responses)

# Function to process input and return response
def process_input(user_input):
    results = faiss_gpu.query_index(user_input, result_dict, title_dict)

    # if not results:
    #     return get_random_response(), False
    
    chunkingList = [row[0] for row in results]
    reIndex = reranker.find_most_similar_index(user_input, chunkingList)
    context = results[reIndex][0]
    title = results[reIndex][3]
    score = results[reIndex][2]

    
    prompt = chatgpt(user_input, context, history)

    # output = language_model_interface.generate_response(prompt, False)
    print("Score_________", score)
    if score < 0.45:
        prompt = get_random_response()
        title = "提供的背景中没有相关的知识。"

    return prompt, title

# Route for receiving text input and returning processed text and image name
@app.route('/process_text', methods=['POST'])
def process_text():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    data = request.get_json()
    user_input = data['input']

    print("Time_________", formatted_time)
    print("Input______", user_input)
    prompt, title = process_input(user_input)
    print("prompt_________", prompt, "\nTitle_________", title)


    return jsonify({'context': prompt, 'title': title})

if __name__ == '__main__':
    # app.run(debug=True)
    # 192.168.0.66
    app.run(debug=False, host='0.0.0.0', port=8080)


