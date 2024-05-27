import React, { useState } from 'react';
import { Container, Button } from 'react-bootstrap';
import { ReactMic } from 'react-mic';
import './App.css';

const App = () => {
  const [conversations, setConversations] = useState([]);
  const [record, setRecord] = useState(false);

  const startRecording = () => {
    setRecord(true);
  };

  const stopRecording = () => {
    setRecord(false);
  };

  const onData = (recordedBlob) => {
    // handle real-time data if needed
  };

  const onStop = (recordedBlob) => {
    // Perform ASR using Web Speech API
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onresult = async (event) => {
      const text = event.results[0][0].transcript;
      const response = await fetch('http://localhost:5000/api/process-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      });
      const result = await response.json();
      setConversations([...conversations, result]);
    };
    recognition.onerror = (event) => {
      console.error(event.error);
    };
    recognition.start();
  };

  return (
    <Container className="mt-5">
      <h1 className="text-center">Voice Interaction App</h1>
      <div className="voice-input text-center my-3">
        <Button 
          variant="primary" 
          onMouseDown={startRecording}
          onMouseUp={stopRecording}
        >
          Hold to Talk
        </Button>
        <ReactMic
          record={record}
          className="sound-wave"
          onStop={onStop}
          onData={onData}
          mimeType="audio/wav"
          strokeColor="#000000"
          backgroundColor="#FF4081" />
      </div>
      <div className="conversations">
        {conversations.map((conv, index) => (
          <div key={index} className="conversation">
            <p>{conv.text}</p>
            {conv.image && <img src={conv.image} alt="response" />}
            {conv.audio && <audio controls src={conv.audio}></audio>}
          </div>
        ))}
      </div>
    </Container>
  );
};

export default App;
