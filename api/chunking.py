from typing import List, Tuple

class Chunking:
    def __init__(self):
        self.delimiters = ["\n\n", "\n", ""]

    def split_document_with_overlap(self, file_path: str, chunk_size: int, overlap_size: int) -> Tuple[List[str], List[str]]:
        chunks = []
        chunk_ids = []
        buffer = ""
        chunk_id = 1

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                buffer += line
                if len(buffer) >= chunk_size:
                    end_index = chunk_size

                    for delimiter in self.delimiters:
                        pos = buffer.rfind(delimiter, 0, end_index)
                        if pos != -1:
                            end_index = pos + len(delimiter)
                            break

                    chunk = buffer[:end_index]
                    chunks.append(chunk)
                    chunk_ids.append(f"id{chunk_id}")

                    buffer = buffer[end_index - overlap_size:]
                    chunk_id += 1

        # Handle the last remaining part if there's any
        if buffer:
            chunks.append(buffer)
            chunk_ids.append(f"id{chunk_id}")
            
        # 函数最终返回了两个列表，分别是 chunk_ids 和 chunks，分别代表了分割后的文本片段的唯一标识和内容。
        return chunk_ids, chunks  # Corrected the return statement here


if __name__ == "__main__":
    
    chunk = Chunking()
    example_docs = "example.txt"
    chunk_ids, split_data = chunk.split_document_with_overlap(example_docs, chunk_size=500, overlap_size=200)

    print("chunk_ids", chunk_ids, "split_data", split_data)

    # sentence_embeddings = model.encode(split_data)




# from langchain.text_splitter import CharacterTextSplitter
# from langchain.document_loaders import DirectoryLoader

# loader = DirectoryLoader('./', glob='hg8346m-olt.txt')
# documents = loader.load()

# text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=5)
# split_docs = text_splitter.split_documents(documents)

# print(split_docs)