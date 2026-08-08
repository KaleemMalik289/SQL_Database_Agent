import { useEffect, useRef } from 'react';
import ChatInput from '../components/Chat/ChatInput';
import TypewriterText from '../components/TypewriterText/TypewriterText';
import TypingIndicator from '../components/TypingIndicator/TypingIndicator';
import { useChat } from '../hooks/useChat';
import { Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './Chat.css';

const Chat = () => {
  const { messages, isLoading, sendMessage } = useChat();
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages or loading states appear
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="chat-workspace">
      {/* Scrollable chat history area */}
      <div className="chat-history-area">
        
        {messages.length === 0 ? (
          <div className="center-content">
            <TypewriterText text="SQL Database Agent" />
          </div>
        ) : (
          <div className="messages-container">
            {messages.map((msg) => (
              <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
                <div className="message-avatar">
                  {msg.sender === 'ai' ? <Bot size={24} /> : <User size={24} />}
                </div>
                <div className="message-content">
                  <div className="message-text">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                  
                  {/* Render Structured SQL if present */}
                  {msg.sql && (
                    <div className="message-sql-block">
                      <div className="sql-header">Generated SQL</div>
                      <pre><code>{msg.sql}</code></pre>
                    </div>
                  )}
                  
                  {/* Render Status if it's an error */}
                  {msg.status && msg.status !== 'success' && (
                    <div className="message-status-error">
                      Status: {msg.status.replace('_', ' ')}
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {/* Show Typing Indicator when waiting for API */}
            {isLoading && <TypingIndicator />}
            
            {/* Invisible div to scroll to */}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      {/* Chat Input Area fixed at bottom */}
      <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />
    </div>
  );
};

export default Chat;
