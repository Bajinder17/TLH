import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LoadingSpinner from '../components/LoadingSpinner';

const PortScanner = () => {
  const [target, setTarget] = useState('');
  const [portRange, setPortRange] = useState('1-1000');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [animate, setAnimate] = useState(false);
  const [portRangeValid, setPortRangeValid] = useState(true);

  useEffect(() => {
    setAnimate(true);
  }, []);
  
  // Validate port range input
  useEffect(() => {
    const validatePortRange = () => {
      if (!portRange) return true;
      
      const pattern = /^(\d+(-\d+)?)(,\d+(-\d+)?)*$/;
      return pattern.test(portRange);
    };
    
    setPortRangeValid(validatePortRange());
  }, [portRange]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!target) {
      alert('Please enter an IP address or hostname');
      return;
    }
    
    if (!portRangeValid) {
      alert('Please enter a valid port range (e.g., "1-1000" or "80,443,8080")');
      return;
    }
    
    setLoading(true);
    setResult(null);
    
    try {
      console.log('Starting port scan for:', target, 'Range:', portRange);
      
      // Always use the API for scanning
      const apiUrl = '/api/scan-ports';
      console.log('Sending request to:', apiUrl);
      
      const response = await axios.post(apiUrl, {
        target,
        port_range: portRange
      }, {
        timeout: 180000, // 3 minutes
        // Add retry logic for reliability
        retry: 1,
        retryDelay: 1000
      });
      
      console.log('Received response:', response.data);
      setResult(response.data);
      
    } catch (error) {
      console.error('Error scanning ports:', error);
      setResult({
        status: 'error',
        message: error.code === 'ECONNABORTED' 
          ? 'Request timed out. Try scanning fewer ports or a smaller port range.'
          : `Error scanning ports: ${error.message}`
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`scanner-page ${animate ? 'animate-in' : ''}`}>
      <div className="page-header">
        <h1 className="animated-title">Port Scanner</h1>
        <p className="animated-subtitle">Scan network ports for open services and vulnerabilities</p>
      </div>
      
      <div className="port-scanner-container">
        <div className="card scan-card">
          <form onSubmit={handleSubmit}>
            <div className="input-row">
              <div className="form-group">
                <label htmlFor="target">
                  <div className="label-icon">🖥️</div>
                  <span>IP Address or Hostname</span>
                </label>
                <div className="input-container">
                  <input 
                    type="text" 
                    id="target" 
                    value={target} 
                    onChange={(e) => setTarget(e.target.value)} 
                    placeholder="192.168.1.1 or example.com" 
                    required 
                    disabled={loading}
                    className="animated-input"
                  />
                  <div className="input-focus-border"></div>
                </div>
                <small>Enter the IP address or domain name to scan</small>
              </div>
            </div>
            
            <div className="input-row">
              <div className="form-group">
                <label htmlFor="port-range">
                  <div className="label-icon">🔌</div>
                  <span>Port Range</span>
                </label>
                <div className={`input-container ${!portRangeValid ? 'error' : ''}`}>
                  <input 
                    type="text" 
                    id="port-range" 
                    value={portRange} 
                    onChange={(e) => setPortRange(e.target.value)} 
                    placeholder="1-1000" 
                    disabled={loading}
                    className="animated-input"
                  />
                  <div className="input-focus-border"></div>
                </div>
                <small>Format: start-end (e.g., 1-1000) or individual ports separated by commas (e.g., 22,80,443)</small>
                {!portRangeValid && <div className="error-message">Please enter a valid port range format</div>}
              </div>
            </div>
            
            <div className="port-format-helper">
              <div className="port-preset-title">Common Port Ranges:</div>
              <div className="port-presets">
                <button type="button" className="port-preset" onClick={() => setPortRange('1-1000')}>
                  Common (1-1000)
                </button>
                <button type="button" className="port-preset" onClick={() => setPortRange('1-65535')}>
                  All (1-65535)
                </button>
                <button type="button" className="port-preset" onClick={() => setPortRange('21-23,25,80,443,3306,3389')}>
                  Popular Services
                </button>
              </div>
            </div>
            
            <div className="scan-actions">
              <button type="submit" className="scan-button" disabled={loading || !portRangeValid}>
                {loading ? (
                  <>
                    <span className="button-icon scanning"></span>
                    <span>Scanning...</span>
                  </>
                ) : (
                  <>
                    <span className="button-icon">🔍</span>
                    <span>Scan Ports</span>
                  </>
                )}
              </button>
            </div>
          </form>
          
          {loading && (
            <LoadingSpinner message="Scanning ports, this may take a few minutes..." />
          )}
          
          {result && (
            <div ref={(el) => {if (el) el.scrollIntoView({ behavior: 'smooth' })}} className="scan-result">
              <div className="result-header">
                <h3>Scan Results</h3>
                <div className="scan-target-info">
                  <div className="scan-target-ip">
                    <span className="info-label">IP:</span>
                    <span className="info-value">{result.target_ip}</span>
                  </div>
                  <div className="scan-target-host">
                    <span className="info-label">Target:</span>
                    <span className="info-value">{target}</span>
                  </div>
                </div>
              </div>
              
              <div className="scan-details">
                <div className="scan-info-row">
                  <div className="scan-info-item">
                    <div className="info-item-label">Port Range:</div>
                    <div className="info-item-value">{portRange}</div>
                  </div>
                  
                  <div className="scan-info-item">
                    <div className="info-item-label">Ports Scanned:</div>
                    <div className="info-item-value">{result.total_ports_scanned}</div>
                  </div>
                  
                  <div className="scan-info-item">
                    <div className="info-item-label">Open Ports:</div>
                    <div className="info-item-value highlight">
                      {result.open_ports?.length || 0}
                    </div>
                  </div>
                </div>
                
                {result.open_ports && result.open_ports.length > 0 ? (
                  <div className="open-ports-container">
                    <div className="open-ports-header">
                      <div className="port-column">Port</div>
                      <div className="service-column">Service</div>
                    </div>
                    <div className="open-ports-list">
                      {result.open_ports.map((port, index) => (
                        <div key={index} className="open-port-item" style={{animationDelay: `${index * 0.1}s`}}>
                          <div className="port-column">{port.port}</div>
                          <div className="service-column">{port.service}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="no-open-ports">
                    <div className="icon">🔒</div>
                    <p>No open ports found in the specified range.</p>
                  </div>
                )}
                
                {result.message && (
                  <div className="result-message">
                    <div className="message-icon">ℹ️</div>
                    <p>{result.message}</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
        
        <div className="info-sidebar">
          <div className="card info-card">
            <h3>About Port Scanning</h3>
            <p>Port scanning helps identify open network services that could potentially be vulnerable to attacks.</p>
            
            <div className="features-list">
              <div className="feature-item">
                <div className="feature-icon">🔍</div>
                <div className="feature-info">
                  <h4>Network Discovery</h4>
                  <p>Find which ports are open and accessible</p>
                </div>
              </div>
              
              <div className="feature-item">
                <div className="feature-icon">⚠️</div>
                <div className="feature-info">
                  <h4>Security Assessment</h4>
                  <p>Identify potential security vulnerabilities</p>
                </div>
              </div>
              
              <div className="feature-item">
                <div className="feature-icon">🔧</div>
                <div className="feature-info">
                  <h4>Service Detection</h4>
                  <p>Determine running services on target system</p>
                </div>
              </div>
            </div>
            
            <div className="port-info-panel">
              <h4>Common Ports</h4>
              <div className="common-ports">
                <div className="common-port">
                  <span className="port-number">21</span>
                  <span className="port-service">FTP</span>
                </div>
                <div className="common-port">
                  <span className="port-number">22</span>
                  <span className="port-service">SSH</span>
                </div>
                <div className="common-port">
                  <span className="port-number">80</span>
                  <span className="port-service">HTTP</span>
                </div>
                <div className="common-port">
                  <span className="port-number">443</span>
                  <span className="port-service">HTTPS</span>
                </div>
                <div className="common-port">
                  <span className="port-number">3306</span>
                  <span className="port-service">MySQL</span>
                </div>
                <div className="common-port">
                  <span className="port-number">3389</span>
                  <span className="port-service">RDP</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <style jsx="true">{`
        .scanner-page {
          opacity: 0;
          transform: translateY(20px);
        }
        
        .scanner-page.animate-in {
          animation: fadeIn 0.5s forwards, slideUp 0.5s forwards;
        }
        
        .page-header {
          margin-bottom: var(--spacing-xl);
          text-align: center;
        }
        
        .animated-title {
          font-size: 2.5rem;
          color: var(--text-color);
          margin-bottom: 0.5rem;
          opacity: 0;
          animation: fadeIn 0.5s 0.3s forwards, slideUp 0.5s 0.3s forwards;
        }
        
        .animated-subtitle {
          color: var(--text-light);
          font-size: 1.125rem;
          opacity: 0;
          animation: fadeIn 0.5s 0.5s forwards, slideUp 0.5s 0.5s forwards;
        }
        
        .port-scanner-container {
          display: grid;
          grid-template-columns: 2fr 1fr;
          gap: var(--spacing-lg);
        }
        
        .scan-card {
          padding: var(--spacing-xl);
          opacity: 0;
          animation: fadeIn 0.5s 0.7s forwards, slideUp 0.5s 0.7s forwards;
        }
        
        .input-row {
          margin-bottom: var(--spacing-lg);
        }
        
        .form-group {
          width: 100%;
        }
        
        .form-group label {
          display: flex;
          align-items: center;
          margin-bottom: 0.5rem;
          font-weight: 600;
          color: var(--text-color);
        }
        
        .label-icon {
          margin-right: var(--spacing-xs);
          font-size: 1.2rem;
        }
        
        .input-container {
          position: relative;
          margin-bottom: var(--spacing-xs);
        }
        
        .input-container.error .animated-input {
          border-color: var(--danger-color);
        }
        
        .animated-input {
          width: 100%;
          padding: 0.75rem 1rem;
          border: 1px solid var(--border-color);
          border-radius: var(--radius);
          font-size: 1rem;
          transition: border-color 0.2s, box-shadow 0.2s;
          background-color: white;
        }
        
        .animated-input:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        .input-focus-border {
          position: absolute;
          bottom: 0;
          left: 50%;
          width: 0;
          height: 2px;
          background-color: var(--primary-color);
          transition: width 0.3s, left 0.3s;
          border-radius: 1px;
        }
        
        .animated-input:focus ~ .input-focus-border {
          width: 100%;
          left: 0;
        }
        
        .form-group small {
          display: block;
          color: var(--text-light);
          font-size: 0.875rem;
          margin-top: 0.25rem;
        }
        
        .error-message {
          color: var(--danger-color);
          font-size: 0.875rem;
          margin-top: 0.5rem;
          display: flex;
          align-items: center;
          animation: fadeIn 0.3s;
        }
        
        .error-message::before {
          content: "⚠️";
          margin-right: 0.5rem;
          font-size: 0.875rem;
        }
        
        .port-format-helper {
          margin-bottom: var(--spacing-xl);
          padding: var(--spacing-md);
          background-color: rgba(243, 244, 246, 0.5);
          border-radius: var(--radius);
          border: 1px solid var(--border-color);
        }
        
        .port-preset-title {
          font-weight: 500;
          margin-bottom: var(--spacing-sm);
          font-size: 0.875rem;
          color: var(--text-light);
        }
        
        .port-presets {
          display: flex;
          flex-wrap: wrap;
          gap: var(--spacing-xs);
        }
        
        .port-preset {
          background-color: rgba(255, 255, 255, 0.5);
          border: 1px solid var(--border-color);
          color: var(--text-color);
          font-size: 0.75rem;
          padding: 0.25rem 0.75rem;
          border-radius: var(--radius-full);
          cursor: pointer;
          transition: all 0.2s;
        }
        
        .port-preset:hover {
          background-color: var(--primary-light);
          border-color: var(--primary-color);
          color: var(--primary-color);
          transform: translateY(-1px);
        }
        
        .scan-actions {
          display: flex;
          justify-content: center;
        }
        
        .scan-button {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: var(--spacing-xs);
          padding: var(--spacing-sm) var(--spacing-xl);
          background-color: var(--primary-color);
          color: white;
          border: none;
          border-radius: var(--radius);
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          min-width: 180px;
        }
        
        .scan-button:hover:not(:disabled) {
          background-color: var(--primary-hover);
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        
        .scan-button:disabled {
          background-color: var(--text-light);
          cursor: not-allowed;
        }
        
        .button-icon {
          display: inline-block;
          transition: transform 0.3s;
        }
        
        .button-icon.scanning {
          width: 16px;
          height: 16px;
          border: 2px solid rgba(255, 255, 255, 0.5);
          border-radius: 50%;
          border-top-color: white;
          animation: spin 1s linear infinite;
        }
        
        .scan-result {
          margin-top: 2.5rem;
          border-radius: var(--radius);
          overflow: hidden;
          border: 1px solid var(--border-color);
          box-shadow: var(--shadow);
          animation: fadeIn 0.5s, slideUp 0.5s;
        }
        
        .result-header {
          background-color: #f9fafb;
          padding: 1.25rem 1.5rem;
          border-bottom: 1px solid var(--border-color);
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        
        .result-header h3 {
          margin: 0;
          color: var(--text-color);
        }
        
        .scan-target-info {
          display: flex;
          flex-wrap: wrap;
          gap: 1.5rem;
        }
        
        .scan-target-ip, .scan-target-host {
          display: flex;
          align-items: baseline;
          gap: 0.5rem;
        }
        
        .info-label {
          color: var(--text-light);
          font-size: 0.875rem;
          font-weight: 500;
        }
        
        .info-value {
          color: var(--text-color);
          font-family: monospace;
          font-size: 0.95rem;
        }
        
        .scan-details {
          padding: 1.5rem;
        }
        
        .scan-info-row {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 1rem;
          margin-bottom: 1.5rem;
        }
        
        .scan-info-item {
          padding: 1rem;
          background-color: rgba(243, 244, 246, 0.5);
          border-radius: var(--radius);
          border: 1px solid var(--border-color);
        }
        
        .info-item-label {
          font-size: 0.75rem;
          color: var(--text-light);
          margin-bottom: 0.25rem;
        }
        
        .info-item-value {
          font-size: 1.125rem;
          font-weight: 600;
          color: var(--text-color);
        }
        
        .info-item-value.highlight {
          color: var(--primary-color);
        }
        
        .open-ports-container {
          border: 1px solid var(--border-color);
          border-radius: var(--radius);
          overflow: hidden;
        }
        
        .open-ports-header {
          display: grid;
          grid-template-columns: 1fr 2fr;
          background-color: #f9fafb;
          padding: 0.75rem 1rem;
          font-weight: 600;
          color: var(--text-color);
          border-bottom: 1px solid var(--border-color);
        }
        
        .open-ports-list {
          max-height: 300px;
          overflow-y: auto;
        }
        
        .open-port-item {
          display: grid;
          grid-template-columns: 1fr 2fr;
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--border-color);
          background-color: white;
          transition: background-color 0.2s;
          animation: fadeIn 0.5s forwards, slideUp 0.3s forwards;
        }
        
        .open-port-item:last-child {
          border-bottom: none;
        }
        
        .open-port-item:hover {
          background-color: var(--primary-light);
        }
        
        .port-column {
          font-family: monospace;
          font-weight: 500;
        }
        
        .no-open-ports {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          text-align: center;
          color: var(--text-light);
          animation: fadeIn 0.5s;
        }
        
        .no-open-ports .icon {
          font-size: 2.5rem;
          margin-bottom: 1rem;
          animation: pulse 2s infinite;
        }
        
        .result-message {
          display: flex;
          align-items: flex-start;
          margin-top: 1.5rem;
          padding: 1rem;
          background-color: rgba(243, 244, 246, 0.7);
          border-radius: var (--radius);
          border-left: 3px solid var(--text-light);
          animation: fadeIn 0.5s 0.3s forwards;
          opacity: 0;
        }
        
        .message-icon {
          margin-right: 0.75rem;
          font-size: 1.25rem;
        }
        
        .result-message p {
          margin: 0;
          color: var (--text-color);
        }
        
        .port-info-panel {
          margin-top: 2rem;
          background-color: rgba(243, 244, 246, 0.5);
          border-radius: var(--radius);
          padding: 1.25rem;
          border: 1px solid var(--border-color);
        }
        
        .port-info-panel h4 {
          margin-top: 0;
          margin-bottom: 1rem;
          font-size: 1rem;
          color: var(--text-color);
        }
        
        .common-ports {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
          gap: 0.75rem;
        }
        
        .common-port {
          display: flex;
          justify-content: space-between;
          padding: 0.5rem 0.75rem;
          background-color: white;
          border-radius: var(--radius);
          border: 1px solid var(--border-color);
          font-size: 0.875rem;
        }
        
        .port-number {
          font-weight: 600;
          color: var (--primary-color);
        }
        
        .port-service {
          color: var(--text-color);
        }
        
        @media (max-width: 992px) {
          .port-scanner-container {
            grid-template-columns: 1fr;
          }
          
          .scan-target-info {
            flex-direction: column;
            gap: 0.5rem;
          }
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default PortScanner;
