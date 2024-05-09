# 帮我构建一个python接口—— 读取一个本地的xlsx文件，其中有两列内容，第一列（A）中的每个格子的内容是图片，第二列（B）格子中的内容是对应的文字，我希望你可以将图片按照行序号命名并保存到本地，同时返回一个字典，key是行序号，value是对应的文字描述。


import openpyxl
from PIL import Image

def process_excel(filename):
    # 打开 Excel 文件
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active

    # 创建一个字典用于存储结果
    result_dict = {}

    # 循环处理每一行
    for row in sheet.iter_rows(min_row=2, max_col=2, values_only=True):
        image_cell, text_cell = row

        # 获取图片对象
        img = openpyxl.drawing.image.Image(image_cell)

        # 保存图片
        image_name = f"image_{sheet[('A' + str(sheet._current_row))].row}.png"
        img.anchor = 'A' + str(sheet._current_row)
        img.width = img.height = 64  # 调整图片大小
        img.image.save(image_name)

        # 将文字描述添加到字典
        result_dict[sheet[('A' + str(sheet._current_row))].row] = text_cell

    return result_dict

# 示例用法
excel_file = "test.xlsx"
result = process_excel(excel_file)
print(result)
