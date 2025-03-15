import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="content-container">
      <div className="hero-section">
        <div className="container">
          <h1 className="hero-title">Secure Your Digital World</h1>
          <p className="hero-description">ThreatLightHouse provides advanced threat detection and security scanning tools in one place.</p>
          <Link to="/file-scan">
            <button className="primary-button">
              Start Scanning
              <span className="arrow">→</span>
            </button>
          </Link>
        </div>
      </div>
      
      <div className="container">
        <div className="section-title">
          <h2>Security Tools</h2>
          <p>Comprehensive scanning solutions for your security needs</p>
        </div>
        
        <div className="feature-grid">
          <div className="feature-box">
            <div className="feature-icon">📄</div>
            <h3>File Scanning</h3>
            <p>Upload and analyze files for viruses, malware, and other threats using advanced detection engines.</p>
            <Link to="/file-scan">
              <button>Scan Files</button>
            </Link>
          </div>
          
          <div className="feature-box">
            <div className="feature-icon">🔗</div>
            <h3>URL Scanning</h3>
            <p>Check if websites are safe to visit by analyzing them for phishing, malware, and suspicious content.</p>
            <Link to="/url-scan">
              <button>Scan URLs</button>
            </Link>
          </div>
          
          <div className="feature-box">
            <div className="feature-icon">🔌</div>
            <h3>Port Scanning</h3>
            <p>Identify open ports and potential security vulnerabilities in networks and servers.</p>
            <Link to="/port-scan">
              <button>Scan Ports</button>
            </Link>
          </div>
        </div>
        
        <div className="info-section">
          <div className="info-card">
            <h3>How It Works</h3>
            <ol>
              <li>Select the appropriate scanning tool for your needs</li>
              <li>Submit a file, URL, or target for scanning</li>
              <li>Our system analyzes the submission using multiple security engines</li>
              <li>Review detailed security report with threat information</li>
            </ol>
          </div>
          
          <div className="info-card">
            <h3>Why Choose ThreatLightHouse</h3>
            <ul>
              <li>Multiple security scanning tools in one platform</li>
              <li>Powered by industry-leading threat intelligence</li>
              <li>Fast and reliable scanning results</li>
              <li>User-friendly interface for all security needs</li>
            </ul>
          </div>
        </div>
      </div>
      
      <style jsx="true">{`
        .hero-section {
          background: linear-gradient(135deg, #4338ca, #3b82f6);
          color: white;
          padding: 4rem 0;
          margin-bottom: 3rem;
          text-align: center;
          border-radius: 0 0 10px 10px;
          box-shadow: var(--shadow);
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .hero-section .container {
          width: 100%;
          max-width: 100%;
          padding: 0;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        
        .hero-title {
          font-size: 2.5rem;
          margin-bottom: 1rem;
          font-weight: 800;
          text-align: center;
          margin-left: auto;
          margin-right: auto;
          width: 100%;
          max-width: 800px;
          display: block;
        }
        
        .hero-description {
          font-size: 1.25rem;
          max-width: 600px;
          margin: 0 auto 2rem;
          opacity: 0.9;
          text-align: center;
          width: 100%;
        }
        
        .primary-button {
          background-color: white;
          color: var(--primary-color);
          font-size: 1.125rem;
          padding: 0.75rem 2rem;
          transition: all 0.3s ease;
        }
        
        .primary-button:hover {
          background-color: rgba(255, 255, 255, 0.9);
          transform: translateY(-2px);
        }
        
        .primary-button .arrow {
          display: inline-block;
          margin-left: 0.5rem;
          transition: transform 0.3s ease;
        }
        
        .primary-button:hover .arrow {
          transform: translateX(4px);
        }
        
        .section-title {
          text-align: center;
          margin-bottom: 2.5rem;
        }
        
        .section-title h2 {
          font-size: 2rem;
          color: var(--text-color);
          margin-bottom: 0.5rem;
          font-weight: 700;
        }
        
        .section-title p {
          color: var(--text-light);
          font-size: 1.125rem;
          max-width: 600px;
          margin: 0 auto;
        }
        
        .feature-box {
          background: white;
          border-radius: var(--radius);
          padding: 1.25rem;
          box-shadow: var(--shadow-sm);
          transition: var(--transition);
          display: flex;
          flex-direction: column;
          height: auto;
          min-height: 200px;
        }
        
        .feature-box h3 {
          margin-top: 0;
          margin-bottom: 0.5rem;
          color: var(--primary-color);
          font-weight: 600;
        }
        
        .feature-box p {
          flex-grow: 1;
          color: var(--text-light);
          margin-bottom: 0.75rem;
          font-size: 0.95rem;
          line-height: 1.4;
        }
        
        .feature-icon {
          font-size: 1.75rem;
          margin-bottom: 0.75rem;
          color: var(--primary-color);
        }
        
        .info-section {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
          margin: 3rem 0;
        }
        
        .info-card {
          background-color: white;
          border-radius: var(--radius);
          padding: 1.5rem;
          box-shadow: var(--shadow-sm);
        }
        
        .info-card h3 {
          color: var(--primary-color);
          margin-top: 0;
          margin-bottom: 1rem;
          font-weight: 600;
        }
        
        .info-card ul, .info-card ol {
          padding-left: 1.25rem;
          margin-bottom: 0;
        }
        
        .info-card li {
          margin-bottom: 0.5rem;
          color: var(--text-light);
        }
        
        .info-card li:last-child {
          margin-bottom: 0;
        }
        
        @media (max-width: 768px) {
          .hero-section {
            padding: 3rem 0;
          }
          
          .hero-title {
            font-size: 2rem;
            text-align: center;
            padding: 0;
          }
          
          .hero-description {
            text-align: center;
            padding: 0 1rem;
            font-size: 1.1rem;
          }
          
          .info-section {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default Home;
