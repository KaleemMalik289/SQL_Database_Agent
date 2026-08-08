import apiClient from './api';

const databaseService = {
  /**
   * Fetches the dynamic database schema from the FastAPI backend.
   * @returns {Promise<Object>} The schema response data containing tables and columns.
   */
  getSchema: async () => {
    try {
      const response = await apiClient.get('/database/schema');
      return response; // The api.js interceptor already unwraps response.data
    } catch (error) {
      console.error("Database Service Error:", error);
      throw error;
    }
  }
};

export default databaseService;
