/**
 * Client-side fallback functions for when API calls fail
 */

/**
 * Generate a client-side file scan result
 * @param {Object} fileInfo - Information about the file being scanned
 * @returns {Object} A mock scan result
 */
export const generateFileScanFallback = (fileInfo = {}) => {
  // eslint-disable-next-line no-unused-vars
  const { name = 'unknown', size = 0, type = '' } = fileInfo;
  
  // Determine if the file might be risky based on extension
  const extension = name.split('.').pop().toLowerCase();
  const riskyExtensions = ['exe', 'dll', 'bat', 'ps1', 'vbs', 'js'];
  
  // Generate a hash-like value from the filename for consistent results
  const hashCode = name.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0);
    return a & a;
  }, 0);
  
  // Use the hash to determine if this file should be marked malicious (for demo)
  const isMalicious = riskyExtensions.includes(extension) && (Math.abs(hashCode) % 10 < 3);
  
  return {
    status: isMalicious ? 'malicious' : 'clean',
    message: 'File scan completed using client-side simulation',
    detections: isMalicious ? `${Math.abs(hashCode) % 15 + 3} / 68` : '0 / 68',
    scan_date: Math.floor(Date.now() / 1000),
    source: 'Client Fallback'
  };
};

/**
 * Generate a client-side URL scan result
 * @param {string} url - The URL being scanned
 * @returns {Object} A mock scan result
 */
export const generateUrlScanFallback = (url = '') => {
  // Malicious patterns for demo purposes
  const maliciousPatterns = ['malware', 'phishing', 'evil', 'hack', 'virus'];
  const suspiciousPatterns = ['free', 'casino', 'prize', 'win', 'discount'];
  
  const isMalicious = maliciousPatterns.some(pattern => url.toLowerCase().includes(pattern));
  const isSuspicious = suspiciousPatterns.some(pattern => url.toLowerCase().includes(pattern));
  
  let status = 'safe';
  let detections = '0 / 86';
  let categories = [];
  
  if (isMalicious) {
    status = 'malicious';
    detections = `${Math.floor(Math.random() * 15) + 5} / 86`;
    categories = ['malicious', 'phishing'];
  } else if (isSuspicious) {
    status = 'suspicious';
    detections = `${Math.floor(Math.random() * 5) + 1} / 86`;
    categories = ['suspicious'];
  }
  
  return {
    status,
    message: 'URL scan completed using client-side simulation',
    detections,
    categories,
    scan_date: Math.floor(Date.now() / 1000),
    source: 'Client Fallback'
  };
};

/**
 * Generate a client-side port scan result
 * @param {string} target - The target IP or hostname
 * @param {string} portRange - The range of ports to scan
 * @returns {Object} A mock scan result
 */
export const generatePortScanFallback = (target = '', portRange = '1-1000') => {
  // Common ports for demo
  const commonPorts = [
    { port: 80, service: 'HTTP' },
    { port: 443, service: 'HTTPS' },
    { port: 22, service: 'SSH' },
    { port: 21, service: 'FTP' },
    { port: 25, service: 'SMTP' },
    { port: 3306, service: 'MySQL' }
  ];
  
  // Get consistent results for the same target
  const hashCode = target.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0);
    return a & a;
  }, 0);
  
  // Select 1-3 ports based on the target hash
  const numPorts = (Math.abs(hashCode) % 3) + 1;
  const selectedPorts = commonPorts.slice(0, numPorts);
  
  return {
    status: 'completed',
    target_ip: `192.168.${Math.abs(hashCode) % 255}.${Math.abs(hashCode) % 255}`,
    open_ports: selectedPorts,
    total_ports_scanned: parseInt(portRange.split('-')[1]) || 1000,
    scan_date: Math.floor(Date.now() / 1000),
    source: 'Client Fallback'
  };
};
