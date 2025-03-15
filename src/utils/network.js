/**
 * Network utility functions for API requests
 */
import axios from 'axios';

/**
 * Get the base API URL depending on environment
 * @returns {string} Base API URL
 */
export const getApiBaseUrl = () => {
  const isVercel = window.location.hostname.includes('vercel.app');
  return isVercel ? `${window.location.origin}/api` : '/api';
};

/**
 * Make an API request with retry functionality
 * @param {string} endpoint - API endpoint path (without /api prefix)
 * @param {Object} options - Request options
 * @returns {Promise<Object>} Response data
 */
export const apiRequest = async (endpoint, options = {}) => {
  const {
    method = 'GET',
    data = null,
    retries = 2,
    timeout = 15000,
    headers = {}
  } = options;
  
  // Ensure endpoint starts with a slash
  const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${path}`;
  
  console.log(`Making ${method} request to ${url}`);
  
  // Try the primary request
  try {
    const response = await axios({
      method,
      url,
      data,
      timeout,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    });
    
    return response.data;
  } catch (error) {
    console.error(`Primary request failed: ${error.message}`);
    
    // Try with retries if specified
    if (retries > 0) {
      console.log(`Retrying... (${retries} attempts left)`);
      
      // Try with explicit Vercel URL if on Vercel
      const isVercel = window.location.hostname.includes('vercel.app');
      if (isVercel) {
        try {
          const vercelUrl = `https://tlh-xi.vercel.app/api${path}`;
          console.log(`Trying explicit Vercel URL: ${vercelUrl}`);
          
          const response = await axios({
            method,
            url: vercelUrl,
            data,
            timeout,
            headers: {
              'Content-Type': 'application/json',
              ...headers
            }
          });
          
          return response.data;
        } catch (vercelError) {
          console.error(`Explicit Vercel URL failed: ${vercelError.message}`);
        }
      }
      
      // Recursive retry with one fewer retry attempt
      return apiRequest(endpoint, {
        ...options,
        retries: retries - 1
      });
    }
    
    // If all retries failed, throw the error
    throw error;
  }
};

export default {
  getApiBaseUrl,
  apiRequest
};
