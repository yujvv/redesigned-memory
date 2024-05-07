from api.faiss_api import Faiss_GPU
from api.loader_docx import Loader

def build_dict(content_list):
    result_dict = {}
    for item in content_list:
        result_dict[item["content"]] = item["content"]
    return result_dict


docx_file = '2test.docx'
content_list = Loader.extract_content(docx_file)

result_dict = build_dict(content_list)

faiss_gpu = Faiss_GPU("my_index", "./text/test")

results = faiss_gpu.query_index("你好，我将用右手为您指路。", result_dict)

for action, semantic, score in results:
    print(f'Action: {action}, Semantic: {semantic}, Score: {score}')

# Add some data
# faiss_gpu.add(actions_semantics)