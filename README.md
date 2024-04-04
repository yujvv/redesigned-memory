# redesigned-memory
RAG框架涉及到多种模型，以及很多个步骤。为了更好地进行差异化的设计，应当将该框架各部分进行解耦，以便对于特定任务进行定制化设计，并在后续更好的跟进领域的发展。


进入代码目录`test/`。

### 步骤 1：准备数据

在项目目录中，确保将 PDF 文件放置在 `test/data` 目录下。

### 步骤 2：创建索引

运行 `create_index.py` 脚本以创建本地的 Faiss 向量数据库。该数据库将用于检索 PDF 文档。

```bash
python create_index.py
```
### 步骤 3：启动接口

在项目目录中，运行 flask.py 脚本以初始化接口。确保修改脚本中的 IP 地址为本机的 IP 地址。

```bash
python flask.py
```

### 步骤 4：调用接口进行问答
示例代码 main_flask.py 提供了一个基于 Flask 接口的问答示例。可以参考该文件来了解如何调用接口进行问答。

pdf.ai
https://zilliz.com.cn/use-cases/llm-retrieval-augmented-generation
https://chat.openai.com/share/26aba92f-4d70-43d1-bf1e-1504948b664b
