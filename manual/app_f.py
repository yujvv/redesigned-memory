from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import speech_recognition as sr

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400
    
    file = request.files['audio']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    recognizer = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='zh-CN')
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        text = f"Could not request results from Google Speech Recognition service; {e}"

    return jsonify({'recognized_text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
