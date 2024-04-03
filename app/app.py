import streamlit as st
from PIL import Image
import io
from api.faiss_api import Faiss_GPU


faiss_gpu = Faiss_GPU("my_index", "/demo/index")

class ImageTextUploader:
    def __init__(self):
        self.images = []
        self.captions = []
        if 'text_blocks' not in st.session_state:
            st.session_state.text_blocks = []
        if 'chunk_nums' not in st.session_state:
            st.session_state.chunk_nums = 1
        if 'dialogue_history' not in st.session_state:
            st.session_state.dialogue_history = []

    def upload_sidebar(self):
        st.sidebar.title("Conversations with Your Images and Text 💬")

        # Upload Images
        with st.sidebar.expander("Upload Images"):
            uploaded_files = st.file_uploader("Select an Image", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
            for i, file in enumerate(uploaded_files):
                caption = st.text_input(f"Enter the Annotations for Image {i+1}", key=f"caption_{i}")
                if file and caption:
                    self.images.append(file)
                    self.captions.append(caption)

        # Upload Text
        with st.sidebar.expander("Upload Text"):
            text_input_container = st.empty()
            text_input = text_input_container.text_area("Enter Text", height=200, max_chars=300)
            if st.button("Add Text"):
                if text_input:
                    st.session_state.text_blocks.append((st.session_state.chunk_nums, text_input))
                    st.session_state.chunk_nums += 1

    def display_content(self):
        col1, col2 = st.columns(2)

        # Display Images
        with col1:
            st.header("Images")
            for i, (file, caption) in enumerate(zip(self.images, self.captions), start=1):
                with st.expander(f"{i}. {caption}", expanded=True):
                    img = Image.open(io.BytesIO(file.read()))
                    st.image(img, use_column_width=True)

        # Display Text
        with col2:
            st.header("Text")
            for i, text in enumerate(st.session_state.text_blocks, start=1):
                with st.expander(f"{i}. 文本", expanded=True):
                    chunk_num, text_content = text
                    st.write(text_content)
                    if st.button(f"Delete {i}", key=f"delete_{i}"):
                        st.session_state.text_blocks.pop(i-1)
                        st.session_state.chunk_nums -= 1

    def chat_interface(self):
        st.header("UniConvo 💬")
        input_text = st.text_input("Enter Your Message")

        if st.button("Send"):
            st.session_state.dialogue_history.append(("User", input_text))
            # Add your logic to process the input text and generate a response
            response = "Response"
            st.session_state.dialogue_history.append(("💬", response))

        if st.button("Clear"):
            st.session_state.dialogue_history = []

        for sender, message in st.session_state.dialogue_history:
            st.markdown(f"**{sender}**: {message}")



def main():
    st.set_page_config(layout="wide")
    # --------------------
    uploader = ImageTextUploader()
    uploader.upload_sidebar()

    # Initialize the vector database


    # # Add some data
    # faiss_gpu.add({"apple": 0, "banana": 1, "orange": 2})

    # # Query for similar items

    # results = faiss_gpu.query("orange")
    # print(results)  # [(0.8, 0), (0.7, 1), (0.6, 2)]

    # # Delete an item
    # faiss_gpu.delete("apple")


    # Add image annotations and text to the vector database
    for caption in uploader.captions:
        # vector_db.add(caption)
        print("----------caption", caption)
    for chunk_num, text in st.session_state.text_blocks:
        # vector_db.add(text)
        print("----------text", text)
        print("----------chunk_num", chunk_num)


    # --------------------
    uploader.display_content()

    # def chat_interface():
    #     st.header("UniConvo 💬")
    #     input_text = st.text_input("Enter Your Message")

    #     if st.button("Send"):
    #         uploader.dialogue_history.append(("User", input_text))

    #         # Search the vector database
    #         results = vector_db.search(input_text, k=3)

    #         # Construct the prompt based on context reasoning
    #         context = []
    #         for result in results:
    #             text, distance = result
    #             if text in uploader.captions:
    #                 image_index = uploader.captions.index(text) + 1
    #                 context.append(f"Image {image_index}: {text}")
    #             elif (chunk_num, text) in uploader.text_blocks:
    #                 text_index = uploader.text_blocks.index((chunk_num, text)) + 1
    #                 context.append(f"Text {text_index}: {text}")
    #             else:
    #                 context.append(text)

    #         context_str = "\n".join(context)
    #         prompt = f"Given the context:\n\n{context_str}\n\nAnswer the following question: {input_text}"

    #         # Request the language model (you'll need to implement this part)
    #         # todo
    #         response = request_language_model(prompt)

    #         uploader.dialogue_history.append(("💬", response))

        # if st.button("Clear"):
        #     uploader.dialogue_history = []

        # for sender, message in uploader.dialogue_history:
        #     st.markdown(f"**{sender}**: {message}")

    # --------------------
    uploader.chat_interface()



# def main():
#     st.set_page_config(layout="wide")
#     uploader = ImageTextUploader()
#     uploader.upload_sidebar()
#     uploader.display_content()
#     uploader.chat_interface()



if __name__ == "__main__":
    main()