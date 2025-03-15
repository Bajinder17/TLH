import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const year = new Date().getFullYear();
  
  return (
    <footer className="app-footer">
      <div className="footer-wave">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
          <path fill="#1f2937" fillOpacity="1" d="M0,192L48,186.7C96,181,192,171,288,176C384,181,480,203,576,197.3C672,192,768,160,864,165.3C960,171,1056,213,1152,218.7C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>
      </div>
      
      <div className="footer-content-wrapper">
        <div className="container">
          <div className="footer-content">
            <div className="footer-branding">
              <div className="footer-logo">
                <span className="footer-logo-icon">🔦</span>
                <h3>ThreatLightHouse</h3>
              </div>
              <p>Advanced threat detection platform for identifying security risks</p>
            </div>
            
            <div className="footer-nav">
              <div className="footer-links">
                <Link to="/">Home</Link>
                <Link to="/file-scan">File Scanner</Link>
                <Link to="/url-scan">URL Scanner</Link>
                <Link to="/port-scan">Port Scanner</Link>
              </div>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>&copy; {year} ThreatLightHouse. All rights reserved.</p>
          </div>
        </div>
      </div>
      
      <style jsx="true">{`
        .app-footer {
          position: relative;
          margin-top: 3rem;
          color: #fff;
        }
        
        .footer-wave {
          position: absolute;
          top: -60px;
          left: 0;
          width: 100%;
          height: 60px;
          overflow: hidden;
          line-height: 0;
          transform: rotate(180deg);
        }
        
        .footer-wave svg {
          position: relative;
          display: block;
          width: calc(100% + 1.3px);
          height: 60px;
          transform: rotateY(180deg);
        }
        
        .footer-content-wrapper {
          background-color: #1f2937;
          padding: 1.5rem 0 1rem;
          position: relative;
          z-index: 1;
        }
        
        .footer-content {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
          align-items: center;
          margin-bottom: 1rem;
        }
        
        .footer-branding {
          animation: fadeIn 0.8s ease-out;
        }
        
        .footer-logo {
          display: flex;
          align-items: center;
          margin-bottom: 0.5rem;
        }
        
        .footer-logo-icon {
          font-size: 1.25rem;
          margin-right: 0.5rem;
          filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.3));
        }
        
        .footer-branding h3 {
          font-size: 1.25rem;
          margin: 0;
          background: linear-gradient(to right, #fff, #94a3b8);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          font-weight: 600;
        }
        
        .footer-branding p {
          color: #94a3b8;
          font-size: 0.85rem;
          line-height: 1.5;
          margin: 0;
        }
        
        .footer-links {
          display: flex;
          justify-content: center;
          gap: 1.5rem;
          align-items: center;
          height: 100%;
        }
        
        .footer-links a {
          color: #e5e7eb;
          text-decoration: none;
          transition: all 0.2s ease;
          font-size: 0.9rem;
          position: relative;
          padding-bottom: 2px;
        }
        
        .footer-links a::after {
          content: '';
          position: absolute;
          width: 100%;
          height: 1px;
          bottom: 0;
          left: 0;
          background-color: var(--primary-color);
          transform: scaleX(0);
          transform-origin: bottom right;
          transition: transform 0.3s ease;
        }
        
        .footer-links a:hover {
          color: white;
        }
        
        .footer-links a:hover::after {
          transform: scaleX(1);
          transform-origin: bottom left;
        }
        
        .footer-bottom {
          border-top: 1px solid rgba(255, 255, 255, 0.1);
          padding-top: 1rem;
          color: #94a3b8;
          font-size: 0.8rem;
          text-align: center;
        }
        
        .footer-bottom p {
          margin: 0;
        }
        
        @media (max-width: 768px) {
          .footer-content {
            grid-template-columns: 1fr;
            gap: 1rem;
            text-align: center;
          }
          
          .footer-logo {
            justify-content: center;
          }
          
          .footer-links {
            flex-wrap: wrap;
          }
        }
        
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </footer>
  );
};

export default Footer;
