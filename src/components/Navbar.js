import React, { useState, useEffect } from 'react';
import { Link, NavLink } from 'react-router-dom';

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);
  
  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <nav className={`App-header ${scrolled ? 'scrolled' : ''}`}>
      <div className="container">
        <div className="header">
          <Link to="/" className="logo-link">
            <h1>
              <span className="logo-text">ThreatLightHouse</span>
            </h1>
          </Link>
          
          <div className={`mobile-menu-button ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
            <span></span>
            <span></span>
            <span></span>
          </div>
          
          <div className={`nav-links ${menuOpen ? 'active' : ''}`}>
            <NavLink to="/" className={({ isActive }) => 
              `nav-link ${isActive ? 'active' : ''}`} onClick={() => setMenuOpen(false)}>
              <span className="nav-icon">🏠</span>
              <span className="nav-text">Home</span>
            </NavLink>
            <NavLink to="/file-scan" className={({ isActive }) => 
              `nav-link ${isActive ? 'active' : ''}`} onClick={() => setMenuOpen(false)}>
              <span className="nav-icon">📄</span>
              <span className="nav-text">File Scan</span>
            </NavLink>
            <NavLink to="/url-scan" className={({ isActive }) => 
              `nav-link ${isActive ? 'active' : ''}`} onClick={() => setMenuOpen(false)}>
              <span className="nav-icon">🔗</span>
              <span className="nav-text">URL Scan</span>
            </NavLink>
            <NavLink to="/port-scan" className={({ isActive }) => 
              `nav-link ${isActive ? 'active' : ''}`} onClick={() => setMenuOpen(false)}>
              <span className="nav-icon">🔌</span>
              <span className="nav-text">Port Scan</span>
            </NavLink>
          </div>
        </div>
      </div>
      
      <style jsx="true">{`
        .App-header {
          position: sticky;
          top: 0;
          z-index: 1000;
          transition: all 0.3s ease;
          padding: var(--spacing-md) 0;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        }
        
        .App-header.scrolled {
          padding: var(--spacing-sm) 0;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .logo-link {
          text-decoration: none;
          color: white;
          display: flex;
          align-items: center;
        }
        
        h1 {
          font-size: 1.75rem;
          display: flex;
          align-items: center;
          margin: 0;
          white-space: nowrap;
          font-weight: 700;
          letter-spacing: -0.02em;
        }
        
        .logo-text {
          background: linear-gradient(to right, #ffffff, rgba(255, 255, 255, 0.8));
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
        }
        
        .nav-links {
          display: flex;
          gap: var(--spacing-sm);
        }
        
        .nav-link {
          color: white;
          text-decoration: none;
          padding: var(--spacing-xs) var(--spacing-sm);
          border-radius: var(--radius);
          transition: var(--transition);
          font-weight: 500;
          position: relative;
          overflow: hidden;
          display: flex;
          align-items: center;
          gap: var(--spacing-xs);
        }
        
        .nav-icon {
          font-size: 1.1rem;
          transition: transform 0.2s ease;
        }
        
        .nav-link:hover .nav-icon {
          transform: scale(1.2);
        }
        
        .nav-link::before {
          content: '';
          position: absolute;
          bottom: 0;
          left: 0;
          width: 100%;
          height: 2px;
          background-color: white;
          transform: translateX(-100%);
          opacity: 0;
          transition: var(--transition);
        }
        
        .nav-link:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }
        
        .nav-link:hover::before {
          transform: translateX(0);
          opacity: 1;
        }
        
        .nav-link.active {
          background-color: rgba(255, 255, 255, 0.2);
          font-weight: 600;
        }
        
        .nav-link.active::before {
          transform: translateX(0);
          opacity: 1;
        }
        
        .mobile-menu-button {
          display: none;
          flex-direction: column;
          justify-content: space-between;
          width: 30px;
          height: 21px;
          cursor: pointer;
          z-index: 1010;
        }
        
        .mobile-menu-button span {
          display: block;
          height: 3px;
          width: 100%;
          background-color: white;
          border-radius: 3px;
          transition: all 0.3s ease;
        }
        
        .mobile-menu-button.active span:nth-child(1) {
          transform: translateY(9px) rotate(45deg);
        }
        
        .mobile-menu-button.active span:nth-child(2) {
          opacity: 0;
          transform: translateX(-20px);
        }
        
        .mobile-menu-button.active span:nth-child(3) {
          transform: translateY(-9px) rotate(-45deg);
        }
        
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
        
        @media (max-width: 768px) {
          .mobile-menu-button {
            display: flex;
          }
          
          .nav-links {
            position: fixed;
            top: 0;
            right: 0;
            width: 75%;
            max-width: 300px;
            height: 100vh;
            background: linear-gradient(to bottom, var(--primary-color), var(--secondary-color));
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            padding: calc(var(--spacing-xxl) + var(--spacing-md)) var(--spacing-xl) var(--spacing-xl);
            transform: translateX(100%);
            transition: transform 0.3s cubic-bezier(0.77, 0, 0.175, 1);
            z-index: 1000;
            box-shadow: -5px 0 25px rgba(0, 0, 0, 0.1);
          }
          
          .nav-links.active {
            transform: translateX(0);
          }
          
          .nav-link {
            margin: var(--spacing-xs) 0;
            font-size: 1.2rem;
            width: 100%;
            opacity: 0;
          }
          
          .nav-links.active .nav-link {
            animation: slideIn 0.4s forwards;
          }
          
          .nav-links.active .nav-link:nth-child(1) { animation-delay: 0.1s; }
          .nav-links.active .nav-link:nth-child(2) { animation-delay: 0.2s; }
          .nav-links.active .nav-link:nth-child(3) { animation-delay: 0.3s; }
          .nav-links.active .nav-link:nth-child(4) { animation-delay: 0.4s; }
          
          .App-header.scrolled h1 {
            font-size: 1.5rem;
          }
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
