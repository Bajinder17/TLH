from flask import Flask, jsonify, request
import os
import time
import random

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def catch_all(path):
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    # Add CORS headers to all responses
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    # Health check endpoint
    if path == '' or path == 'api/health':
        return jsonify({
            'status': 'healthy',
            'message': 'API is running in serverless mode'
        }), 200, headers
    
    # File scanner endpoint
    if path == 'api/scan-file':
        return jsonify({
            'status': 'clean',
            'message': 'File scan completed successfully',
            'detections': '0 / 68',
            'scan_date': int(time.time()),
            'source': 'Demo Scanner'
        }), 200, headers
    
    # URL scanner endpoint
    if path == 'api/scan-url':
        url = request.json.get('url', '') if request.is_json else ''
        is_malicious = any(x in url.lower() for x in ['malware', 'phishing', 'scam'])
        
        return jsonify({
            'status': 'malicious' if is_malicious else 'safe',
            'message': 'URL scan completed',
            'detections': '5 / 86' if is_malicious else '0 / 86',
            'scan_date': int(time.time()),
            'source': 'Demo Scanner'
        }), 200, headers
    
    # Port scanner endpoint
    if path == 'api/scan-ports':
        data = request.json if request.is_json else {}
        target = data.get('target', 'localhost')
        
        open_ports = []
        if random.random() > 0.5:  # Sometimes show open ports
            common_ports = [80, 443, 22, 25]
            for port in common_ports:
                if random.random() > 0.5:
                    open_ports.append({
                        'port': port,
                        'service': f"Demo Service on {port}"
                    })
        
        return jsonify({
            'status': 'completed',
            'target_ip': '192.168.1.1',
            'open_ports': open_ports,
            'total_ports_scanned': 1000,
            'scan_date': int(time.time()),
            'source': 'Demo Scanner'
        }), 200, headers
    
    # Default response for unknown endpoints
    return jsonify({
        'status': 'error',
        'message': f'Unknown endpoint: {path}'
    }), 404, headers

# Vercel handler
handler = app
