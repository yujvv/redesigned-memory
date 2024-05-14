from docx import Document

def read_docx(filename):
    # the object to open the doc
    doc = Document(filename)
    # Iterate through each paragraph
    for paragraph in doc.paragraphs:
        # Continuous text with the same format
        for run in paragraph.runs:
            font_size = run.font.size
            font_name = run.font.name
            text = run.text
            if font_size:
                if font_size.pt == 24 and (font_name == '等线 Light' or font_name == '等线'):
                    print("Font Size: 三号")
                    print("Font Name:", font_name)
                    # Remove first and last white space characters
                    print("Text:", text.strip())
                elif font_size.pt == 18:
                    print("Font Size: 小二")
                    print("Font Name:", font_name)
                    print("Text:", text.strip())
                elif font_size.pt == 22:
                    print("Font Size: 二号")
                    print("Font Name:", font_name)
                    print("Text:", text.strip())

# 替换为你的docx文件路径
filename = "your_docx_file.docx"
read_docx(filename)
