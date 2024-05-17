import streamlit as st
import time
import os
from api.faiss_api import Faiss_GPU
from api.loader_docx import Loader
from api.chatglm import ChatGLMInterface
# import logging
# logging.getLogger('streamlit').setLevel(logging.ERROR)

# Function to build dictionary from content list
def build_dict(content_list):
    result_dict = {}
    title_dict = {}
    for item in content_list:
        result_dict[item["content"]] = item["index"]
        title_dict[item["content"]] = item["title"]
    # 输出的两个字典，key都是text chunking本身，value分别为index和title
    return result_dict, title_dict

# Function to initialize models
@st.cache_resource()
def initialize_models():
    loader = Loader()
    docx_file = 'demo.docx'
    content_list = loader.extract_content(docx_file)
    result_dict, title_dict = build_dict(content_list)
    faiss_gpu = Faiss_GPU("demo0", "./index")
    faiss_gpu.add(result_dict)
    language_model_interface = ChatGLMInterface()
    return faiss_gpu, result_dict, title_dict, language_model_interface

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
st.markdown("<h1>🔍 Car 🚗 Q&A Interface </h1>", unsafe_allow_html=True)

# Initialize the chat history
chat_history = []

# Initialize models
faiss_gpu, result_dict, title_dict, language_model_interface = initialize_models()

# Function to display images
# def display_images(image_title):
#     st.image("{image_title}.png", caption=image_title, use_column_width=True)
def display_images(image_title):
    image_path = f"{image_title}.png"
    if os.path.exists(image_path):
        st.image(image_path, caption=image_title, use_column_width=True)
    else:
        st.write(f"⛔️ No 📷 Image.")
        # You can display a default placeholder image here if you want
        # st.image("placeholder.png", caption="Placeholder", use_column_width=True)

# Add an input area
with st.form("input_form"):
    user_input = st.text_area("Enter your question:", height=200)
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Add the user input to the chat history
        chat_history.append(("User", user_input))

        # Process the user input and generate the output
        results = faiss_gpu.query_index(user_input, result_dict, title_dict)
        top = results[0][0]
        title = results[0][3]
        prompt = f"你好，你是我的车内助手。请基于背景，帮我温柔地回答问题。\nContext:{top}\nQ: {user_input}\nA:"
        output = language_model_interface.generate_response(prompt, False)

        score = results[0][2]
        hint = ""
        if score > 0.4:
            hint = "(知识来源于《" + title + "》章节)"
        else:
            hint = "(提供的背景中没有相关的知识)"
        bot = output + hint

        # Add a typing animation
        typing_animation = st.empty()
        for i in range(3):
            typing_animation.write(".")
            time.sleep(0.1)
        typing_animation.empty()

        display_images(title)

        # Add the output to the chat history
        chat_history.append(("Bot", bot))

        # Clear the input area
        user_input = ""

# Display the chat history
for sender, message in chat_history:
    if sender == "User":
        st.markdown(f"<div class='input-area'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='output-area'><strong>Bot:</strong> {message}</div>", unsafe_allow_html=True)
