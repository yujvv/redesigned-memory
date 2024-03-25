from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader

loader = DirectoryLoader('./', glob='hg8346m-olt.txt')
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=5)
split_docs = text_splitter.split_documents(documents)

print(split_docs)

# 输出的 split_docs 是一个列表，其中包含多个 Document 对象。每个 Document 对象代表一个切割后的文档片段，具有以下属性：

# page_content: 文档片段的内容，即切割后的文本。
# metadata: 元数据，提供了关于文档的额外信息，这里包括了文档的来源。