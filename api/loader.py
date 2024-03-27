import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def main(input_file, output_file):
    if input_file.lower().endswith('.pdf'):
        text = extract_text_from_pdf(input_file)
    elif input_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = extract_text_from_image(input_file)
    else:
        print("Unsupported file format.")
        return

    save_text_to_file(text, output_file)
    print("Text extracted and saved to", output_file)

if __name__ == "__main__":
    input_file_path = input("PDF或PNG文件的路径：")
    output_file_path = "temp.txt"
    main(input_file_path, output_file_path)
