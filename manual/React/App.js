import React, { useState } from 'react';
import VoiceInput from './VoiceInput';
import Conversation from './Conversation';

const App = () => {
  const [messages, setMessages] = useState([]);

  const handleSpeechEnd = async (audioBlob) => {
    const response = await sendToBackend(audioBlob);
    setMessages([...messages, response]);
  };

  const sendToBackend = async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav');

    const backendResponse = await fetch('http://localhost:5000/process', {
      method: 'POST',
      body: formData,
    });

    return await backendResponse.json();
  };

  return (
    <div>
      <VoiceInput onSpeechEnd={handleSpeechEnd} />
      <Conversation messages={messages} />
    </div>
  );
};

export default App;