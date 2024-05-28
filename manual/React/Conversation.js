import React from 'react';
import { FaVolumeUp, FaImage } from 'react-icons/fa';

const Conversation = ({ messages }) => {
  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>
          {msg.text && <p>{msg.text}</p>}
          {msg.image && (
            <div>
              <FaImage /> <img src={msg.image} alt="Response" />
            </div>
          )}
          {msg.audio && (
            <div>
              <FaVolumeUp /> <audio src={msg.audio} controls></audio>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default Conversation;