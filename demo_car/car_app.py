import streamlit as st
import time
from api.faiss_api import Faiss_GPU
from api.loader_docx import Loader
from api.chatglm import ChatGLMInterface

def build_dict(content_list):
    result_dict = {}
    for item in content_list:
        result_dict[item["content"]] = item["index"]
    return result_dict

# Set the page configuration
st.set_page_config(
    page_title="Q&A Interface",
    page_icon=":question:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Add some CSS styles
css = """
<style>
h1 {
    font-family: 'Helvetica Neue', sans-serif;
    font-weight: bold;
    color: #333333;
}
.input-area {
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.output-area {
    padding: 20px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Add a header
st.markdown("<h1>🔍 Car Q&A Interface 🚗</h1>", unsafe_allow_html=True)

# Initialize the chat history
chat_history = []

# Load the necessary components
loader = Loader()
docx_file = 'M9.docx'
content_list = loader.extract_content(docx_file)
result_dict = build_dict(content_list)
faiss_gpu = Faiss_GPU("M9", "./demo")
faiss_gpu.add(result_dict)
language_model_interface = ChatGLMInterface()

# Add an input area
with st.form("input_form"):
    user_input = st.text_area("Enter your question:", height=200)
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Add the user input to the chat history
        chat_history.append(("User", user_input))

        # Process the user input and generate the output
        results = faiss_gpu.query_index(user_input, result_dict)
        top = results[0][0]
        prompt = f"你好，你是我的车内助手。请基于背景，帮我温柔地回答问题。\nContext:{top}\nQ: {user_input}\nA:"
        output = language_model_interface.generate_response(prompt, False)

        # Add a typing animation
        typing_animation = st.empty()
        for i in range(3):
            typing_animation.write(".")
            time.sleep(0.5)
        typing_animation.empty()

        # Add the output to the chat history
        chat_history.append(("Bot", output))

        # Clear the input area
        user_input = ""

# Display the chat history
for sender, message in chat_history:
    if sender == "User":
        st.markdown(f"<div class='input-area'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='output-area'><strong>Bot:</strong> {message}</div>", unsafe_allow_html=True)