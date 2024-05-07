from api.faiss_api import Faiss_GPU
from api.loader_docx import Loader
from api.chatglm import ChatGLMInterface

def build_dict(content_list):
    result_dict = {}
    for item in content_list:
        result_dict[item["content"]] = item["index"]
    return result_dict


loader = Loader()
docx_file = 'M9.docx'
content_list = loader.extract_content(docx_file)

result_dict = build_dict(content_list)
# print(result_dict)

faiss_gpu = Faiss_GPU("M9", "./demo")
faiss_gpu.add(result_dict)



language_model_interface = ChatGLMInterface()


# while True:
#     query = input("\n用户：")
#     if query.strip() == "stop":
#         break
#     if query.strip() == "clear":
#         os.system(language_model_interface.clear_command)
#         continue


while True:
    qa = input("Ask your QA: ")
    results = faiss_gpu.query_index(qa, result_dict)

    # for action, semantic, score in results:
    #     print(f'Action: {action}, Semantic: {semantic}, Score: {score}')
    top = results[0][0]

    prompt = f"你好，你是我的车内助手。请基于背景，帮我温柔地回答问题。\nContext:{top}\nQ: {qa}\nA:"

    response = language_model_interface.generate_response(prompt, False)
    print("\n助手的回复：", response)

# Add some data
# faiss_gpu.add(actions_semantics)