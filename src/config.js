/**
 * Global application configuration
 */
const config = {
  // Application information
  appName: 'ThreatLightHouse',
  appVersion: '1.0.0',
  
  // Environment-specific configurations
  environment: process.env.NODE_ENV || 'development',
  
  // URL configurations
  urls: {
    baseUrl: process.env.NODE_ENV === 'production' 
      ? 'https://tlh-xi.vercel.app' 
      : 'http://localhost:3000',
    apiUrl: process.env.NODE_ENV === 'production' 
      ? 'https://tlh-xi.vercel.app/api' 
      : 'http://localhost:5000/api',
  },
  
  // Feature flags
  features: {
    useMockScannersInProduction: true, // Use mock scanners in production environment
    enableReporting: true,             // Enable report generation and storage
    enableDarkMode: false              // Dark mode feature flag (future)
  }
};

export default config;
