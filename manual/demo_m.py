import streamlit as st

st.write("这是一个可以在手机端录音和播放声音的示例")

# 在 Streamlit 中直接嵌入 HTML 和 JavaScript 代码
javascript_code = """
<button id="recordButton">开始录音</button>
<audio id="audio" controls></audio>

<script>
var recordButton = document.getElementById('recordButton');
var audio = document.getElementById('audio');
var recording = false;
var mediaRecorder;

recordButton.addEventListener('click', function() {
  if (recording) {
    mediaRecorder.stop();
    recordButton.textContent = '开始录音';
    recording = false;
  } else {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(function(stream) {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        recordButton.textContent = '停止录音';
        recording = true;

        mediaRecorder.ondataavailable = function(e) {
          var audioBlob = new Blob([e.data], { 'type' : 'audio/wav' });
          audio.src = URL.createObjectURL(audioBlob);
        };
      })
      .catch(function(err) {
        console.log('getUserMedia 错误：', err);
      });
  }
});
</script>
"""

# 在 Streamlit 中嵌入 JavaScript 代码
st.write(javascript_code, unsafe_allow_html=True)

# Streamlit 应用本身在服务器端运行，它并不直接支持在手机端录音或播放声音。