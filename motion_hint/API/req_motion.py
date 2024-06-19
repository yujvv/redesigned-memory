import requests

def main():
    url = 'http://127.0.0.1:5000/get_action'  # 修改为接口的实际URL

    # 准备要发送的数据
    query = "第一点，我希望你闭嘴。"
    payload = {'query': query}

    # 发送POST请求
    response = requests.post(url, json=payload)

    # 打印结果
    if response.status_code == 200:
        result = response.json()
        print("动作编号:", result.get('action_number'))
    else:
        print("请求失败:", response.status_code)

if __name__ == "__main__":
    main()
