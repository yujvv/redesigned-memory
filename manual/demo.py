import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# 设置页面标题和头部
st.set_page_config(page_title="手机交互页面", page_icon=":iphone:", layout="centered")

# 在页面中显示标题
st.title("手机交互页面")

# 添加文本输入框，用于用户输入文本
user_input = st.text_input("请输入您的问题")

# 添加一个空的文本输出区域，用于显示用户说的话
user_speech_text = st.empty()

# 当用户输入文本并点击按钮时，触发回调函数
if st.button("提交"):
    # 在页面中显示用户输入的文本
    st.write("您的问题是：", user_input)
    
    # 语音识别
    st.write("请开始说话...")
    # 创建语音识别器
    r = sr.Recognizer()
    # 打开麦克风并开始录音
    with sr.Microphone() as source:
        audio_data = r.listen(source, timeout=5)  # 最长录音时间为5秒
    st.write("录音结束！")

    try:
        # 使用语音识别器识别录音内容
        text_output = r.recognize_google(audio_data, language="zh-CN")
        # 在页面中显示语音识别结果
        user_speech_text.write("您说的话是：{}".format(text_output))

        # 文本输出
        st.write("这里留给文本输出的空间")

        # 图片输出
        st.write("这里留给图片输出的空间")

        # 语音输出
        st.write("这里留给语音输出的空间")

        # TTS 文本到语音转换
        tts = gTTS(text_output, lang='zh-CN')
        # 保存语音文件
        tts.save("user_input.mp3")
        # 播放语音文件
        playsound("user_input.mp3")
    except sr.UnknownValueError:
        st.write("抱歉，无法理解您说的话！")
