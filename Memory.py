from langchain.memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(temperature=0)

# 初始化 MessageHistory 对象
history = ChatMessageHistory()

# 给 MessageHistory 对象添加对话内容
history.add_ai_message("hello.")
history.add_user_message("where are u from?")

# 执行对话
ai_response = chat(history.messages)
print(ai_response)