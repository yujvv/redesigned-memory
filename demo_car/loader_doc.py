import docx
from api.faiss_api import Faiss_GPU

def get_text_under_headings(docx_file):
    doc = docx.Document(docx_file)
    data = {}
    current_heading = None
    current_text = []

    for paragraph in doc.paragraphs:
        if paragraph.style.name == "Heading 3":
            if current_heading is not None:
                data[current_heading] = "\n".join(current_text)
            current_heading = paragraph.text
            current_text = []
        else:
            current_text.append(paragraph.text)

    if current_heading is not None:
        data[current_heading] = "\n".join(current_text)

    return data

# Usage example
docx_file = "path/to/your/file.docx"
data = get_text_under_headings(docx_file)


faiss_gpu = Faiss_GPU("my_index", "./index")

# # Add some data
# faiss_gpu.add({"apple": 0, "banana": 1, "orange": 2})
# # Query for similar items
# results = faiss_gpu.query("orange")
# print(results)  # [(0.8, 0), (0.7, 1), (0.6, 2)]
# # Delete an item
# faiss_gpu.delete("apple")

# Add the data to the index
faiss_gpu.add(data)