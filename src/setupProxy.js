const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // This proxy is only used in development
  if (process.env.NODE_ENV === 'development') {
    console.log('Setting up proxy middleware for /api');
    
    app.use(
      '/api',
      createProxyMiddleware({
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        pathRewrite: {
          '^/api': '/api' // Keep the /api prefix
        },
        onError: (err, req, res) => {
          console.error('Proxy error:', err);
          res.writeHead(500, {
            'Content-Type': 'application/json',
          });
          res.end(JSON.stringify({ 
            message: 'Proxy error connecting to API',
            error: err.message 
          }));
        },
      })
    );
  }
};
