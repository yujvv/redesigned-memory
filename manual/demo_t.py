import streamlit as st
import streamlit.components.v1 as components

# HTML and JavaScript for recording and playing audio
html_code = """
<!DOCTYPE html>
<html>
<head>
  <title>Audio Recorder</title>
</head>
<body>
  <h2>Record Audio</h2>
  <button id="recordButton">Start Recording</button>
  <button id="stopButton" disabled>Stop Recording</button>
  <button id="playButton" disabled>Play Recording</button>
  <p id="status"></p>
  <audio id="audioPlayback" controls></audio>

  <script>
    let mediaRecorder;
    let audioChunks = [];

    async function startRecording() {
      try {
        let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
          audioChunks.push(event.data);
        };

        mediaRecorder.start();
        document.getElementById('status').innerText = 'Recording...';
        document.getElementById('recordButton').disabled = true;
        document.getElementById('stopButton').disabled = false;
        document.getElementById('playButton').disabled = true;

        console.log('Recording started');
      } catch (err) {
        console.error('Error accessing media devices.', err);
        document.getElementById('status').innerText = 'Error accessing media devices: ' + err;
      }
    }

    function stopRecording() {
      mediaRecorder.stop();
      document.getElementById('status').innerText = 'Stopped';
      document.getElementById('recordButton').disabled = false;
      document.getElementById('stopButton').disabled = true;
      console.log('Recording stopped');

      mediaRecorder.onstop = () => {
        let audioBlob = new Blob(audioChunks, { 'type' : 'audio/wav' });
        audioChunks = [];

        let audioUrl = URL.createObjectURL(audioBlob);
        let audio = document.getElementById('audioPlayback');
        audio.src = audioUrl;
        audio.load();
        document.getElementById('playButton').disabled = false;

        let formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        fetch('/upload_audio', {
          method: 'POST',
          body: formData
        }).then(response => response.text())
          .then(text => {
            document.getElementById('status').innerText = `Audio uploaded. Recognized text: ${text}`;
          });

        console.log('Audio uploaded');
      };
    }

    document.getElementById('recordButton').onclick = startRecording;
    document.getElementById('stopButton').onclick = stopRecording;

    document.getElementById('playButton').onclick = () => {
      let audio = document.getElementById('audioPlayback');
      audio.play().catch(error => {
        document.getElementById('status').innerText = `Playback failed: ${error}`;
        console.error('Playback failed', error);
      });
    };
  </script>
</body>
</html>
"""

components.html(html_code)
