# streamlit run app.py
import streamlit as st
from PIL import Image
import io


# 设置页面布局
st.set_page_config(layout="wide")

# 创建上传图片和文本的容器
st.sidebar.title("Conversations with Your Images and Text 💬")

# 图片和文本存储 
images = []
captions = []
# text_blocks = []
# chunk_nums = 1

if 'text_blocks' not in st.session_state:
    st.session_state.text_blocks = []
if 'chunk_nums' not in st.session_state:
    st.session_state.chunk_nums = 1
if 'dialogue_history' not in st.session_state:
    st.session_state.dialogue_history = []
# if 'text_blocks' not in st.session_state:
#     st.session_state.input_key = datetime.now().strftime("%Y%m%d%H%M%S")

# 上传图片和标题
with st.sidebar.expander("Upload Images"):
    uploaded_files = st.file_uploader("Select an Image", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
    for i, file in enumerate(uploaded_files):
        caption = st.text_input(f"Enter the Annotations for Image {i+1}", key=f"caption_{i}")
        if file and caption:
            images.append(file)
            captions.append(caption)

# 上传文本
with st.sidebar.expander("Upload Text"):
    # text_input = st.text_area("输入文本", height=200, max_chars=300)
    text_input_container = st.empty()
    text_input = text_input_container.text_area("Enter Text", height=200, max_chars=300)
    if st.button("Add Text"):
        if text_input:
            st.session_state.text_blocks.append((st.session_state.chunk_nums, text_input))
            # text_blocks.append((chunk_nums, text_input))
            st.session_state.chunk_nums += 1
            # text_input_container.empty()
            # text_input_container.text_area("输入文本", value="", height=200, max_chars=300)

        # text_input = ""  # 清空输入框
            # st.session_state.input_key = datetime.now().strftime("%Y%m%d%H%M%S")
        


# 主页面显示
col1, col2 = st.columns(2)

# 显示图片标题和预览
with col1:
    st.header("Images")
    for i, (file, caption) in enumerate(zip(images, captions), start=1):
        with st.expander(f"{i}. {caption}", expanded=True):
            img = Image.open(io.BytesIO(file.read()))
            st.image(img, use_column_width=True)

# 显示标题和文本
with col2:
    st.header("Text")
    for i, text in enumerate(st.session_state.text_blocks, start=1):
        with st.expander(f"{i}. 文本", expanded=True):
            st.write(text)
            if st.button(f"Delete {i}", key=f"delete_{i}"):
                st.session_state.text_blocks.pop(i-1)
                st.session_state.chunk_nums -= 1

# 对话部分
st.header("UniConvo 💬")
input_text = st.text_input("Enter Your Message")
# dialogue_history = []
if st.button("Send"):
    # 添加你处理输入文本的逻辑
    st.session_state.dialogue_history.append(("User", input_text))
    # 示例响应
    response = "Response"
    st.session_state.dialogue_history.append(("💬", response))

if st.button("Clear"):
    st.session_state.dialogue_history = []

for sender, message in st.session_state.dialogue_history:
    st.markdown(f"**{sender}**: {message}")


# if st.button("Send"):
#     # Add your logic for processing the input_text here
#     dialogue_history.append(("User", input_text))
    
#     # Function to process uploaded images and text
#     def process_uploads(images, texts, input_text):
#         # Your logic here
#         # ...
#         # ...
        
#         # Example response
#         response = "This is a sample response from the system."
#         return response
    
#     response = process_uploads(uploaded_images, uploaded_texts, input_text)
#     dialogue_history.append(("System", response))