/**
 * Helper functions for VirusTotal API integration
 */
import axios from 'axios';

// VirusTotal API base URL
const VT_API_URL = 'https://www.virustotal.com/api/v3';

/**
 * Check if VirusTotal API key is configured
 * @returns {boolean}
 */
export const isVirusTotalConfigured = () => {
  return Boolean(process.env.REACT_APP_VIRUSTOTAL_API_KEY);
};

/**
 * Get headers for VirusTotal API requests
 * @returns {Object} Headers object
 */
export const getVirusTotalHeaders = () => {
  return {
    'x-apikey': process.env.REACT_APP_VIRUSTOTAL_API_KEY,
    'Content-Type': 'application/json'
  };
};

/**
 * Scan a URL using VirusTotal API
 * @param {string} url - URL to scan
 * @returns {Promise<Object>} Scan results
 */
export const scanUrl = async (url) => {
  if (!isVirusTotalConfigured()) {
    throw new Error('VirusTotal API key not configured');
  }
  
  // Prepare URL for scanning
  const formData = new URLSearchParams();
  formData.append('url', url);
  
  try {
    // Submit URL for analysis
    const submitResponse = await axios.post(
      `${VT_API_URL}/urls`,
      formData,
      { headers: getVirusTotalHeaders() }
    );
    
    if (submitResponse.data && submitResponse.data.data) {
      const analysisId = submitResponse.data.data.id;
      
      // Wait for analysis to complete
      for (let attempt = 0; attempt < 5; attempt++) {
        // Wait before checking analysis status
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Check analysis status
        const analysisResponse = await axios.get(
          `${VT_API_URL}/analyses/${analysisId}`,
          { headers: getVirusTotalHeaders() }
        );
        
        const status = analysisResponse.data.data.attributes.status;
        
        if (status === 'completed') {
          // Process and return results
          const stats = analysisResponse.data.data.attributes.stats;
          const malicious = stats.malicious || 0;
          const suspicious = stats.suspicious || 0;
          const total = Object.values(stats).reduce((sum, val) => sum + val, 0);
          
          return {
            status: malicious > 0 ? 'malicious' : suspicious > 0 ? 'suspicious' : 'safe',
            detections: `${malicious + suspicious} / ${total}`,
            scan_date: Math.floor(Date.now() / 1000),
            source: 'VirusTotal API'
          };
        }
      }
      
      // If analysis is taking too long
      return {
        status: 'pending',
        message: 'Analysis is still in progress',
        scan_date: Math.floor(Date.now() / 1000),
        source: 'VirusTotal API (Partial)'
      };
    }
  } catch (error) {
    console.error('VirusTotal API error:', error);
    throw error;
  }
};

/**
 * Check a file hash against VirusTotal
 * @param {string} hash - SHA-256 file hash
 * @returns {Promise<Object>} Scan results
 */
export const checkFileHash = async (hash) => {
  if (!isVirusTotalConfigured()) {
    throw new Error('VirusTotal API key not configured');
  }
  
  try {
    const response = await axios.get(
      `${VT_API_URL}/files/${hash}`,
      { headers: getVirusTotalHeaders() }
    );
    
    if (response.data && response.data.data) {
      const attributes = response.data.data.attributes;
      const stats = attributes.last_analysis_stats;
      
      const malicious = stats.malicious || 0;
      const suspicious = stats.suspicious || 0;
      const total = Object.values(stats).reduce((sum, val) => sum + val, 0);
      
      return {
        status: malicious > 0 ? 'malicious' : suspicious > 0 ? 'suspicious' : 'clean',
        detections: `${malicious + suspicious} / ${total}`,
        scan_date: attributes.last_analysis_date,
        source: 'VirusTotal API'
      };
    }
  } catch (error) {
    if (error.response && error.response.status === 404) {
      // File not found in VirusTotal database
      return null;
    }
    console.error('VirusTotal API error:', error);
    throw error;
  }
};

export default {
  isVirusTotalConfigured,
  scanUrl,
  checkFileHash
};
