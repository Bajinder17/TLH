from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Simple mock data for responses
mock_data = {
    'file': {
        'status': 'clean',
        'message': 'File scan completed (serverless mode)',
        'detections': '0 / 68',
        'source': 'Serverless Mock'
    },
    'url': {
        'status': 'safe',
        'message': 'URL scan completed (serverless mode)',
        'detections': '0 / 86',
        'source': 'Serverless Mock'
    },
    'port': {
        'status': 'completed',
        'target_ip': '192.168.1.1',
        'open_ports': [],
        'total_ports_scanned': 1000,
        'source': 'Serverless Mock'
    }
}

@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def catch_all(path):
    """Handle all routes for a serverless function"""
    
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '86400'  # 24 hours
        }
        return ('', 204, headers)
    
    # Add CORS headers to all responses
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    try:
        # Health check endpoints
        if path == '' or path == 'api/health':
            return jsonify({
                'status': 'healthy',
                'message': 'ThreatLightHouse API is running (serverless)',
                'api_key_configured': bool(os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY', ''))
            }), 200, headers
        
        # File scanner endpoint
        if path == 'api/scan-file':
            return jsonify(mock_data['file']), 200, headers
        
        # URL scanner endpoint
        if path == 'api/scan-url':
            return jsonify(mock_data['url']), 200, headers
        
        # Port scanner endpoint
        if path == 'api/scan-ports':
            return jsonify(mock_data['port']), 200, headers
        
        # Default response for any other endpoint
        return jsonify({
            'status': 'healthy',
            'message': 'ThreatLightHouse API is running (serverless)',
            'path': path
        }), 200, headers
    except Exception as e:
        print(f"Error handling request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred processing your request',
            'error': str(e)
        }), 500, headers

# This is used by Vercel to call the Flask app
handler = app
