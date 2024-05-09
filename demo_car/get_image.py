import docx
import os
import re

def get_pictures(word_path, result_path):
    """
    Extract images from Word document
    :param word_path: path to Word document
    :param result_path: path to save extracted images
    """
    try:
        doc = docx.Document(word_path)
        dict_rel = doc.part._rels
        image_dict = {}
        chunk_index = 1
        image_index = 1

        for rel in dict_rel:
            rel = dict_rel[rel]
            if "image" in rel.target_ref:
                if not os.path.exists(result_path):
                    os.makedirs(result_path)

                # Find the chunk index for the current image
                for run in doc.paragraphs:
                    if run.text.strip() == rel.target_part.blob[:10]:
                        chunk_index = run._p.get_sourceLine() + 1
                        print("------------", chunk_index)
                        break

                img_name = re.findall("/(.*)", rel.target_ref)[0]
                img_name = f'{chunk_index}-{image_index}.{img_name.split(".")[-1]}'

                with open(f'{result_path}/{img_name}', "wb") as f:
                    f.write(rel.target_part.blob)

                image_dict[chunk_index] = image_dict.get(chunk_index, [])
                image_dict[chunk_index].append(img_name)
                image_index += 1
    except Exception as e:
        print(f"Error: {e}")

# Example usage
word_path = "2test.docx"
result_path = "./images"
get_pictures(word_path, result_path)