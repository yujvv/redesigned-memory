# pip install requests
import requests

def translate_text(text, target_lang='EN', source_lang=None):
    auth_key = 'your_deepl_auth_key'  # 在这里替换成你的DeepL API密钥
    url = 'https://api-free.deepl.com/v2/translate'

    params = {
        'auth_key': auth_key,
        'text': text,
        'target_lang': target_lang
    }

    if source_lang:
        params['source_lang'] = source_lang

    response = requests.post(url, data=params)

    if response.status_code == 200:
        result = response.json()
        return result['translations'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    # 示例中文翻译
    chinese_text = "你好，世界！"
    translated_chinese = translate_text(chinese_text, target_lang='EN', source_lang='ZH')
    print(f"中文翻译成英文: {translated_chinese}")

    # 示例日语翻译
    japanese_text = "こんにちは、世界！"
    translated_japanese = translate_text(japanese_text, target_lang='EN', source_lang='JA')
    print(f"日语翻译成英文: {translated_japanese}")
