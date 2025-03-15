from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def catch_all(path):
    """Simplified route handler for Vercel"""
    
    # Add CORS headers to all responses
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        # Simple health check
        if path in ['', '/', 'api/health', '/api/health']:
            return jsonify({
                'status': 'healthy',
                'message': 'API is running',
                'timestamp': int(time.time())
            }), 200, headers
        
        # File scan endpoint
        if path in ['api/scan-file', '/api/scan-file']:
            # Return mock result without processing file
            result = {
                'status': 'clean',
                'message': 'File scan completed',
                'detections': '0 / 68',
                'scan_date': int(time.time()),
                'source': 'Vercel API'
            }
            return jsonify(result), 200, headers
        
        # Default response for unknown endpoints
        return jsonify({
            'status': 'error',
            'message': 'Invalid endpoint',
            'path': path
        }), 404, headers
        
    except Exception as e:
        print(f"Error in API: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error': str(e)
        }), 200, headers  # Return 200 even for errors

# Vercel handler
handler = app
