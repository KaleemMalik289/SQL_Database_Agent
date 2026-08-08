import axios from 'axios';

// Create a singleton Axios instance
// This ensures all requests share the same configuration (Base URL, Timeout, Headers)
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 30000, // 30 seconds (LLMs can be slow)
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response Interceptor for centralized error normalization
api.interceptors.response.use(
  (response) => {
    // If the HTTP request succeeds, just return the data payload
    return response.data;
  },
  (error) => {
    // Standardize error formats for the frontend
    console.error("API Communication Error:", error);
    
    const normalizedError = {
      success: false,
      message: 'An unexpected error occurred.',
      details: null
    };

    if (error.response) {
      // The server responded with a status code outside the 2xx range
      normalizedError.message = error.response.data?.message || `Server Error (${error.response.status})`;
      normalizedError.details = error.response.data?.error || null;
    } else if (error.request) {
      // The request was made but no response was received
      normalizedError.message = 'Unable to reach the server. Please check your connection.';
    } else {
      // Something happened in setting up the request
      normalizedError.message = error.message;
    }

    return Promise.reject(normalizedError);
  }
);

export default api;
