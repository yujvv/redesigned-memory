from flask import Flask, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    # 获取前端发送的音频数据
    audio_data = request.form.get('audio')
    
    # 模拟在手机端进行ASR
    text = simulate_asr(audio_data)
    
    # 处理文本,生成回复
    response = handle_text(text)
    
    return jsonify(response)

def simulate_asr(audio_data):
    # 模拟ASR过程,实际应该使用真实的ASR服务
    return "This is a simulated transcription."

def handle_text(text):
    # 模拟处理文本,生成回复
    response = {
        'text': f"你说的是: {text}",
        'image': "https://via.placeholder.com/200",
        'audio': "https://example.com/response.mp3"
    }
    return response

if __name__ == '__main__':
    app.run(debug=True)