from docx import Document
from docx.shared import Inches
import base64

# 定义全局变量用于保存当前的index
global_index = 0

def extract_content(docx_file):
    global global_index  # 声明使用全局变量

    doc = Document(docx_file)
    content_list = []
    image_dict = {}
    table_dict = {}

    current_chunk = []
    current_subheading = ""

    for paragraph in doc.paragraphs:
        if paragraph.text.startswith('###') and paragraph.style.font.size >= Inches(0.3):
            if current_chunk:
                # 使用全局index
                content_list.append({"index": global_index, "content": "\n".join(current_chunk)})
                current_chunk = []
                global_index += 1  # 每次添加chunk时递增全局index

            # current_subheading = paragraph.text.strip('### ')

        elif paragraph.text and paragraph.style.font.size >= Inches(0.2):
            if current_chunk:
                # 使用全局index
                content_list.append({"index": global_index, "content": "\n".join(current_chunk)})
                current_chunk = []
                global_index += 1  # 每次添加chunk时递增全局index

            current_chunk.append(paragraph.text)

        elif paragraph.text:
            current_chunk.append(paragraph.text)

        # for run in paragraph.runs:
        #     if run.element.tag.endswith('}r'):
        #         # 处理图片
        #         pic_element = run.element.find('.//*/{http://schemas.openxmlformats.org/drawingml/2006/picture}pic')
        #         if pic_element is not None:
        #             image_data = None
        #             for item in run.element.findall('.//*/{http://schemas.openxmlformats.org/drawingml/2006/picture}blip'):
        #                 embed_id = item.attrib["{%s}embed" % item.nsmap['r']]
        #                 for rel in doc.part.rels:
        #                     if rel.rId == embed_id:
        #                         image_data = rel.target_part.blob
        #                         break
        #             if image_data:
        #                 image_dict.setdefault(global_index, []).append(base64.b64encode(image_data).decode('utf-8'))

        #     # 处理表格
        #     elif run.element.tag.endswith('}tbl'):
        #         table_dict[global_index] = [cell.text for cell in paragraph.cells]

        for run in paragraph.runs:
            if run.element.tag.endswith('}r'):
                # 处理图片
                pic_element = run.element.find('.//*/{http://schemas.openxmlformats.org/drawingml/2006/picture}pic')
                if pic_element is not None:
                    image_dict[global_index] = image_dict.get(global_index, [])
                    image_dict[global_index].append(run._r)

            # 处理表格
            elif run.element.tag.endswith('}tbl'):
                table_dict[global_index] = table_dict.get(global_index, [])
                table_dict[global_index].append(run.element.xml)


    if current_chunk:
        content_list.append({"index": global_index, "content": "\n".join(current_chunk)})
        global_index += 1  # 每次添加chunk时递增全局index

    return content_list, image_dict, table_dict

if __name__ == '__main__':
    docx_file = '2test.docx'
    content_list, image_dict, table_dict = extract_content(docx_file)

    print("Content List:")
    for i, chunk in enumerate(content_list):
        print(f"Chunk {i + 1}:\n{chunk}\n")
        print("----------")

    print("Image Dictionary:")
    print(image_dict)
    print("\nTable Dictionary:")
    print(table_dict)