/**
 * Utility functions for client-side fallbacks when API calls fail
 */

// Generate file scan fallback result
export const generateFileScanFallback = (fileName) => {
  const fileExt = fileName.split('.').pop().toLowerCase();
  const riskyExts = ['exe', 'dll', 'bat', 'ps1', 'vbs', 'js'];
  
  // Determine mock status based on file extension
  const isMalicious = riskyExts.includes(fileExt) && Math.random() < 0.3;
  
  return {
    status: isMalicious ? 'malicious' : 'clean',
    message: 'File scan completed using client-side simulation',
    detections: isMalicious ? `${Math.floor(Math.random() * 15) + 3} / 68` : '0 / 68',
    scan_date: Math.floor(Date.now() / 1000),
    source: 'Client Fallback'
  };
};

// Generate URL scan fallback result
export const generateUrlScanFallback = (url) => {
  const maliciousPatterns = ['malware', 'phishing', 'hack', 'virus', 'exploit'];
  const suspiciousPatterns = ['free', 'prize', 'winner', 'casino', 'download'];
  
  let status = 'safe';
  let detections = '0 / 86';
  
  if (maliciousPatterns.some(pattern => url.toLowerCase().includes(pattern))) {
    status = 'malicious';
    detections = `${Math.floor(Math.random() * 15) + 5} / 86`;
  } else if (suspiciousPatterns.some(pattern => url.toLowerCase().includes(pattern))) {
    status = 'suspicious';
    detections = `${Math.floor(Math.random() * 5) + 1} / 86`;
  }
  
  return {
    status,
    message: 'URL scan completed using client-side simulation',
    detections,
    scan_date: Math.floor(Date.now() / 1000),
    source: 'Client Fallback'
  };
};

// Generate port scan fallback result
export const generatePortScanFallback = (target, portRange) => {
  // Common ports and services
  const commonPorts = [
    { port: 21, service: 'FTP' },
    { port: 22, service: 'SSH' },
    { port: 25, service: 'SMTP' },
    { port: 80, service: 'HTTP' },
    { port: 443, service: 'HTTPS' },
    { port: 3306, service: 'MySQL' },
    { port: 8080, service: 'HTTP-Alt' }
  ];
  
  // Generate a stable mock IP based on the hostname
  let ip = target;
  if (!/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(target)) {
    let hash = 0;
    for (let i = 0; i < target.length; i++) {
      hash = ((hash << 5) - hash) + target.charCodeAt(i);
      hash |= 0;
    }
    
    ip = [
      Math.abs(hash % 255) + 1,
      Math.abs((hash >> 8) % 255) + 1,
      Math.abs((hash >> 16) % 255) + 1,
      Math.abs((hash >> 24) % 255) + 1
    ].join('.');
  }
  
  // Determine number of open ports (deterministic but "random")
  let seed = 0;
  for (let i = 0; i < target.length; i++) {
    seed = ((seed << 5) - seed) + target.charCodeAt(i);
    seed |= 0;
  }
  
  const numOpenPorts = (Math.abs(seed) % 5) + 1; // 1-5 open ports
  const shuffledPorts = [...commonPorts].sort(() => 0.5 - Math.random());
  const openPorts = shuffledPorts.slice(0, numOpenPorts);
  
  return {
    status: 'completed',
    target_ip: ip,
    open_ports: openPorts,
    total_ports_scanned: 1000,
    scan_date: Math.floor(Date.now() / 1000),
    source: 'Client Fallback'
  };
};

// Check if we're in the production environment
export const isProduction = () => {
  return process.env.NODE_ENV === 'production';
};
