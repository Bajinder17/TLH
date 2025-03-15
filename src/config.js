// API configuration
const config = {
  // Base URL for API endpoints
  apiUrl: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000',
  
  // Feature flags
  features: {
    useRealScanners: process.env.NODE_ENV === 'development'
  }
};

export default config;
