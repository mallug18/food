 import axios from 'axios';

// This code reads the VITE_API_URL from your Netlify settings.
// If it's not found, it falls back to your local server.
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const apiClient = axios.create({
  baseURL: baseURL,
});

export default apiClient;
