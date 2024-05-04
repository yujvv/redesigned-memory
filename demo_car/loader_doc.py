from api.faiss_api import Faiss_GPU
import docx
from docx.shared import Pt

def get_text_and_objects(docx_file):
    doc = docx.Document(docx_file)
    data = {}
    current_chunk = None
    current_text = []
    tables = {}
    images = {}

    for element in doc.element.body:
        if isinstance(element, docx.text.paragraph.Paragraph):
            if element.style.font.size == Pt(12):  # Assuming size 3 font is 12pt
                if current_chunk is not None:
                    data[current_chunk] = "\n".join(current_text)
                    current_text = []
                current_chunk = element.text
                print("text:____", element.text)
            else:
                current_text.append(element.text)
        elif isinstance(element, docx.table.Table):
            table_id = len(tables)
            tables[table_id] = {"chunk": current_chunk}
        elif isinstance(element, docx.shape.InlineShape):
            image_id = len(images)
            images[image_id] = {"chunk": current_chunk}

    if current_chunk is not None:
        data[current_chunk] = "\n".join(current_text)

    return data, tables, images


faiss_gpu = Faiss_GPU("my_index", "/text/index")
# Usage example
docx_file = "./2test.docx"
data, tables, images = get_text_and_objects(docx_file)

# Add the text data to the index
for chunk, text in data.items():
    faiss_gpu.add({chunk: text})

print("over:____")
# Print the tables and images with their associated chunks
for table_id, table_data in tables.items():
    print(f"Table {table_id} belongs to chunk: {table_data['chunk']}")

for image_id, image_data in images.items():
    print(f"Image {image_id} belongs to chunk: {image_data['chunk']}")

# faiss_gpu = Faiss_GPU("my_index", "./index")

# # Add some data
# faiss_gpu.add({"apple": 0, "banana": 1, "orange": 2})
# # Query for similar items
# results = faiss_gpu.query("orange")
# print(results)  # [(0.8, 0), (0.7, 1), (0.6, 2)]
# # Delete an item
# faiss_gpu.delete("apple")


# faiss_gpu.add(data)