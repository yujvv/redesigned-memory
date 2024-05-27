# python3 -m venv venv
# source venv/bin/activate
# pip install Flask
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/process-text', methods=['POST'])
def process_text():
    data = request.json
    user_text = data.get('text')

    # Placeholder for backend processing logic
    response = {
        'text': "This is a response from the backend.",
        'image': "https://via.placeholder.com/150",
        'audio': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
