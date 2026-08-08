import api from './api';

/**
 * Chat Service
 * Isolates all Chat-related API calls from UI components.
 */
const chatService = {
  /**
   * Sends a user message to the AI Agent.
   * @param {string} message - The natural language question.
   * @param {string} sessionId - The current session identifier.
   * @returns {Promise<Object>} - The standardized APIResponse from the backend.
   */
  sendMessage: async (message, sessionId = "default-session") => {
    try {
      const payload = {
        message: message,
        session_id: sessionId
      };
      // The response interceptor in api.js extracts response.data for us
      const response = await api.post('/chat', payload);
      return response;
    } catch (error) {
      // The error is already normalized by the interceptor, re-throw it to the hook
      throw error;
    }
  },

  /**
   * Pings the health endpoint to check backend connectivity.
   */
  checkHealth: async () => {
    return await api.get('/health');
  }
};

export default chatService;
