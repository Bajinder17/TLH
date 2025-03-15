import React from 'react';

const LoadingSpinner = ({ message = 'Loading...', fullScreen = false }) => {
  return (
    <div className={`loading-spinner ${fullScreen ? 'fullscreen' : ''}`}>
      <div className="spinner-wrapper">
        <svg className="spinner-svg" viewBox="0 0 50 50">
          <circle
            className="spinner-path"
            cx="25"
            cy="25"
            r="20"
            fill="none"
            strokeWidth="4"
          ></circle>
        </svg>
        <div className="spinner-inner-circle"></div>
      </div>
      <p className="spinner-message">{message}</p>
      
      <style jsx="true">{`
        .loading-spinner {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: var(--spacing-xl);
          min-height: 150px;
        }
        
        .loading-spinner.fullscreen {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(5px);
          z-index: 9999;
          min-height: 100vh;
        }
        
        .spinner-wrapper {
          position: relative;
          width: 64px;
          height: 64px;
          margin-bottom: var(--spacing-lg);
          animation: scaleIn 0.4s var(--bounce) forwards;
        }
        
        .spinner-svg {
          animation: rotate 2s linear infinite;
          width: 100%;
          height: 100%;
        }
        
        .spinner-path {
          stroke: var(--primary-color);
          stroke-linecap: round;
          animation: dash 1.5s ease-in-out infinite;
          stroke-dasharray: 90, 150;
          stroke-dashoffset: -35;
        }
        
        .spinner-inner-circle {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 45%;
          height: 45%;
          background-color: var(--primary-light);
          border-radius: 50%;
          animation: pulse 2s infinite;
        }
        
        .spinner-message {
          margin-top: var(--spacing-sm);
          color: var(--primary-color);
          font-weight: 500;
          animation: fadeIn 1s ease forwards, pulse 2s infinite;
          font-size: 1rem;
          letter-spacing: 0.01em;
          text-align: center;
          max-width: 300px;
        }
        
        @keyframes rotate {
          100% { transform: rotate(360deg); }
        }
        
        @keyframes dash {
          0% {
            stroke-dasharray: 1, 150;
            stroke-dashoffset: 0;
          }
          50% {
            stroke-dasharray: 90, 150;
            stroke-dashoffset: -35;
          }
          100% {
            stroke-dasharray: 90, 150;
            stroke-dashoffset: -124;
          }
        }
        
        @keyframes scaleIn {
          from {
            transform: scale(0.5);
            opacity: 0;
          }
          to {
            transform: scale(1);
            opacity: 1;
          }
        }
        
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }
        
        @keyframes pulse {
          0% {
            transform: translate(-50%, -50%) scale(0.95);
            opacity: 0.7;
          }
          50% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
          }
          100% {
            transform: translate(-50%, -50%) scale(0.95);
            opacity: 0.7;
          }
        }
      `}</style>
    </div>
  );
};

export default LoadingSpinner;
