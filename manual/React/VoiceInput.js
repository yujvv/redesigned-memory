import React, { useState } from 'react';
import { useSpeechRecognition } from 'react-speech-recognition';
import { FaMicrophoneAlt } from 'react-icons/fa';

const VoiceInput = ({ onSpeechEnd }) => {
  const [audioBlob, setAudioBlob] = useState(null);
  const { transcript, resetTranscript, listening, browserSupportsSpeechRecognition } = useSpeechRecognition();

  const startListening = () => {
    resetTranscript();
    window.SpeechRecognition.startListening({ continuous: true });
  };

  const stopListening = () => {
    window.SpeechRecognition.stopListening();
    onSpeechEnd(audioBlob, transcript);
  };

  const handleAudioData = (data) => {
    const blob = new Blob([data], { type: 'audio/wav' });
    setAudioBlob(blob);
  };

  if (!browserSupportsSpeechRecognition) {
    return <span>Your browser does not support speech recognition.</span>;
  }

  return (
    <div>
      <button onMouseDown={startListening} onMouseUp={stopListening} onTouchStart={startListening} onTouchEnd={stopListening}>
        <FaMicrophoneAlt />
      </button>
      {listening && <div>Listening: {transcript}</div>}
      <audio ref={(node) => node && node.captureStream().addEventListener('dataavailable', handleAudioData)} autoPlay={false} muted={true} />
    </div>
  );
};

export default VoiceInput;