import './TypingIndicator.css';

/**
 * Animated typing indicator to show when the AI is processing a response.
 */
const TypingIndicator = () => {
  return (
    <div className="typing-indicator-container">
      <div className="typing-bubble">
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
      </div>
      <span className="typing-text">Agent is thinking...</span>
    </div>
  );
};

export default TypingIndicator;
