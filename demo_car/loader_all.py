from api.faiss_api import Faiss_GPU
import docx
import os

def get_text_and_objects(docx_file):
    if not os.path.isfile(docx_file):
        raise ValueError(f"Invalid file path: {docx_file}")

    doc = docx.Document(docx_file)
    chunks = {}
    current_chunk = None
    current_text = []
    tables = {}
    images = {}

    for element in doc.element.body:
        if isinstance(element, docx.text.paragraph.Paragraph):
            if element.style.name.startswith("Heading 1"):
                if current_chunk is not None and current_text:
                    chunks[current_chunk] = {
                        "text": "\n".join(current_text),
                        "tables": tables,
                        "images": images
                    }
                    current_text = []
                    tables = {}
                    images = {}
                current_chunk = element.text
            else:
                current_text.append(element.text)
        elif isinstance(element, docx.table.Table):
            table_id = len(tables)
            tables[table_id] = element
        elif isinstance(element, docx.shape.InlineShape):
            image_id = len(images)
            images[image_id] = element

    if current_chunk is not None and current_text:
        chunks[current_chunk] = {
            "text": "\n".join(current_text),
            "tables": tables,
            "images": images
        }

    return chunks

faiss_gpu = Faiss_GPU("my_index", "/text/index")
docx_file = "./2test.docx"

if os.path.isfile(docx_file):
    chunks = get_text_and_objects(docx_file)

    # Add the text data to the index
    for chunk_title, chunk_data in chunks.items():
        faiss_gpu.add({chunk_title: chunk_data["text"]})

    print("Vector database created successfully.")

    # Perform similarity search
    query_text = "Enter your query text here"
    results = faiss_gpu.query(query_text, k=5)  # Retrieve top 5 similar chunks

    # Print the results
    for score, chunk_index in results:
        chunk_title = list(chunks.keys())[chunk_index]
        chunk_data = chunks[chunk_title]
        print(f"Chunk Title: {chunk_title}")
        print(f"Similarity Score: {score}")
        print(f"Text Content: {chunk_data['text']}")
        print("Associated Tables:")
        for table_id, table in chunk_data["tables"].items():
            print(f"  Table {table_id}: {table.text}")
        print("Associated Images:")
        for image_id, image in chunk_data["images"].items():
            print(f"  Image {image_id}: {image.data}")
        print("-" * 50)
else:
    print(f"Invalid file path: {docx_file}")



# The keys are the block titles (Heading 1 text, i.e., Title 1, Title 2, etc.).
# The values are dictionaries containing three keys:

# "text": The text content associated with the block title.
# "tables": A dictionary where the keys are sequential integers representing table IDs, and the values are the actual docx.table.Table objects from the DOCX file.
# "images": A dictionary where the keys are sequential integers representing image IDs, and the values are the actual docx.shape.InlineShape objects from the DOCX file.
