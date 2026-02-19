import React from 'react';
import { CheckCircle, AlertCircle } from 'lucide-react';
import './Message.css';

function Message({ message }) {
  const isSuccess = message.type === 'success';

  return (
    <div className={`message message-${message.type}`}>
      <div className="message-content">
        {isSuccess ? (
          <CheckCircle className="message-icon" />
        ) : (
          <AlertCircle className="message-icon" />
        )}
        <p>{message.text}</p>
      </div>
    </div>
  );
}

export default Message;
