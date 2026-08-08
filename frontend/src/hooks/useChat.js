import { useState, useCallback } from 'react';
import chatService from '../services/chatService';

/**
 * Custom hook to abstract chat state and API communication away from UI components.
 */
export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (text) => {
    // 1. Validate Input
    if (!text || text.trim() === '') return;

    const userMessage = {
      id: Date.now().toString(),
      sender: 'user',
      content: text.trim(),
      timestamp: new Date().toISOString()
    };

    // 2. Append User Message & Set Loading State
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // 3. Call Axios Service
      const response = await chatService.sendMessage(userMessage.content);
      
      // 4. Process AI Response
      if (response && response.success) {
        const aiMessage = {
          id: (Date.now() + 1).toString(),
          sender: 'ai',
          content: response.data?.summary || "Query executed.",
          sql: response.data?.generated_sql || null,
          result: response.data?.result || null,
          status: response.data?.status || "success",
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error(response.message || "Failed to parse response.");
      }
    } catch (err) {
      // 5. Handle Errors cleanly
      setError(err.message);
      
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        content: `Error: ${err.message}`,
        status: 'error',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      // 6. Reset Loading State
      setIsLoading(false);
    }
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage
  };
};
