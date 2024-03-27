import streamlit as st
from PIL import Image
import io

# Set up page layout
st.set_page_config(layout="wide")

# Create a container for uploading images and text
st.sidebar.title("Upload Images and Text")

# Image uploader
uploaded_images = st.sidebar.file_uploader("Choose images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

# Text uploader
uploaded_texts = st.sidebar.text_area("Enter text", height=200)

# Create containers for displaying images and text
col1, col2 = st.columns(2)

# Container for images
with col1:
    st.header("Images")
    if uploaded_images:
        for i, image in enumerate(uploaded_images):
            img = Image.open(io.BytesIO(image.read()))
            st.image(img, caption=f"Image {i+1}", use_column_width=True)

# Container for text
with col2:
    st.header("Text")
    if uploaded_texts:
        for i, text in enumerate(uploaded_texts.split("\n\n"), start=1):
            st.markdown(f"**Text {i}**")
            st.write(text)

# Container for dialogue
st.header("Dialogue")
input_text = st.text_input("Enter your message")
if st.button("Send"):
    # Add your logic for processing the input_text here
    st.write(f"You said: {input_text}")