import { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Mic } from 'lucide-react';
import './ChatInput.css';

const ChatInput = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSend = () => {
    if (message.trim() && !isLoading) {
      onSendMessage?.(message.trim());
      setMessage('');
      // Reset height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  return (
    <div className="chat-input-wrapper">
      <div className="chat-input-container">
        <textarea
          ref={textareaRef}
          className="chat-input-textarea"
          placeholder="Ask a question about your database..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          rows={1}
        />
        
        <div className="chat-input-actions">
          <div className="action-buttons-left">
            <button className="icon-btn" title="Attach File (Coming Soon)" disabled={isLoading}>
              <Paperclip size={20} />
            </button>
            <button className="icon-btn" title="Voice Input (Coming Soon)" disabled={isLoading}>
              <Mic size={20} />
            </button>
          </div>

          <div className="input-footer">
            {message.length > 0 && (
              <span className="char-counter">{message.length} chars</span>
            )}
            <button 
              className="send-btn" 
              onClick={handleSend}
              disabled={!message.trim() || isLoading}
              title="Send Message"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
