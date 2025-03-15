/**
 * API configuration for production and development environments
 */
const apiConfig = {
  // Base URLs
  baseUrl: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000',
  
  // API endpoints
  endpoints: {
    health: '/api/health',
    scanFile: '/api/scan-file',
    scanUrl: '/api/scan-url',
    scanPorts: '/api/scan-ports'
  },
  
  // Request configuration
  requestConfig: {
    timeout: 30000, // 30 seconds
    retries: 2,
    retryDelay: 1000 // 1 second
  }
};

export default apiConfig;
