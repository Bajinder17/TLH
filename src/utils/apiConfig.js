/**
 * API configuration for production and development environments
 */
const apiConfig = {
  // Base URLs - always include the full domain for production
  baseUrl: process.env.NODE_ENV === 'production' 
    ? 'https://tlh-xi.vercel.app' 
    : 'http://localhost:5000',
  
  // API endpoints - using relative paths for better compatibility
  endpoints: {
    health: '/api/health',
    scanFile: '/api/scan-file',
    scanUrl: '/api/scan-url',
    scanPorts: '/api/scan-ports'
  },
  
  // Request configuration with increased reliability
  requestConfig: {
    timeout: 45000, // 45 seconds - increased for better reliability
    retries: 3,     // Increase retry count for better reliability
    retryDelay: 1500 // 1.5 seconds between retries
  }
};

export default apiConfig;
