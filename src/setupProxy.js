const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  console.log('Setting up proxy middleware for /api');
  
  // This proxy is only used in development
  // In production, API requests will be handled by Vercel serverless functions
  if (process.env.NODE_ENV === 'development') {
    app.use(
      '/api',
      createProxyMiddleware({
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        logLevel: 'debug',
        onError: (err, req, res) => {
          console.error('Proxy error:', err);
          res.writeHead(500, {
            'Content-Type': 'application/json',
          });
          res.end(JSON.stringify({ message: 'Proxy error connecting to API', error: err.message }));
        },
      })
    );
  }
};
