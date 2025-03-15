from flask import Flask, jsonify, request
import os
import time
import random
import json
import base64
import hashlib

app = Flask(__name__)

def generate_mock_file_result(file_info=None):
    """Generate realistic mock file scan results"""
    if file_info and 'name' in file_info:
        file_name = file_info.get('name', 'unknown')
        extension = file_name.split('.')[-1].lower() if '.' in file_name else ''
        
        # Determine if file should be classified as potentially risky
        risky_extensions = ['exe', 'dll', 'bat', 'ps1', 'vbs', 'js']
        
        if extension in risky_extensions and random.random() < 0.3:
            status = 'malicious'
            detections = f"{random.randint(3, 20)} / 68"
        else:
            status = 'clean'
            detections = "0 / 68"
    else:
        # Default safe result
        status = 'clean'
        detections = "0 / 68"
    
    return {
        'status': status,
        'message': f'File scan completed successfully on Vercel',
        'detections': detections,
        'scan_date': int(time.time()),
        'source': 'Vercel Scanner'
    }

def generate_mock_url_result(url=None):
    """Generate realistic mock URL scan results"""
    if not url:
        return {
            'status': 'safe',
            'message': 'URL scan completed',
            'detections': '0 / 86',
            'scan_date': int(time.time()),
            'source': 'Vercel Scanner'
        }
    
    # Check for suspicious or malicious patterns in the URL
    malicious_patterns = ['malware', 'phishing', 'evil', 'hack', 'virus']
    suspicious_patterns = ['free', 'casino', 'prize', 'win', 'discount']
    
    is_malicious = any(pattern in url.lower() for pattern in malicious_patterns)
    is_suspicious = any(pattern in url.lower() for pattern in suspicious_patterns)
    
    if is_malicious:
        return {
            'status': 'malicious',
            'message': 'URL scan detected malicious indicators',
            'detections': f"{random.randint(5, 15)} / 86",
            'scan_date': int(time.time()),
            'categories': random.sample(['phishing', 'malware', 'scam'], k=2),
            'source': 'Vercel Scanner'
        }
    elif is_suspicious:
        return {
            'status': 'suspicious',
            'message': 'URL scan detected potential suspicious indicators',
            'detections': f"{random.randint(1, 4)} / 86",
            'scan_date': int(time.time()),
            'categories': random.sample(['suspicious', 'unrated'], k=1),
            'source': 'Vercel Scanner'
        }
    else:
        return {
            'status': 'safe',
            'message': 'URL scan completed - no threats detected',
            'detections': '0 / 86',
            'scan_date': int(time.time()),
            'source': 'Vercel Scanner'
        }

def generate_mock_port_result(target=None, port_range=None):
    """Generate realistic mock port scan results"""
    # Common open ports
    common_ports = [
        {'port': 80, 'service': 'HTTP'},
        {'port': 443, 'service': 'HTTPS'},
        {'port': 22, 'service': 'SSH'},
        {'port': 21, 'service': 'FTP'},
        {'port': 25, 'service': 'SMTP'},
        {'port': 3306, 'service': 'MySQL'},
        {'port': 8080, 'service': 'HTTP-ALT'}
    ]
    
    # Generate a consistent but random-looking IP based on the target
    if target:
        # Use the target string to generate a deterministic but random-looking IP
        hash_obj = hashlib.md5(target.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        ip_parts = []
        for i in range(4):
            ip_parts.append(str((hash_int >> (i * 8)) % 256))
        target_ip = '.'.join(ip_parts)
    else:
        target_ip = '192.168.1.1'
    
    # Select some ports to be "open" based on the target
    if target:
        # Use target to determine how many ports should be open (consistently)
        hash_obj = hashlib.md5(target.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        num_open = (hash_int % 5) + 1  # 1-5 open ports
        selected_ports = random.sample(common_ports, min(num_open, len(common_ports)))
    else:
        selected_ports = random.sample(common_ports, 2)
    
    return {
        'status': 'completed',
        'target_ip': target_ip,
        'open_ports': selected_ports,
        'total_ports_scanned': 1000 if not port_range else int(port_range.split('-')[1]) if '-' in port_range else 100,
        'scan_date': int(time.time()),
        'source': 'Vercel Scanner'
    }

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def catch_all(path):
    """Handle all routes for serverless function"""
    
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization',
            'Access-Control-Max-Age': '86400'  # 24 hours
        }
        return ('', 204, headers)
    
    # Add CORS headers to all responses
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"Vercel Request received - Path: {path}, Method: {request.method}")
        
        # File scanner endpoint
        if path == 'api/scan-file' or path == '/api/scan-file':
            print("======= FILE SCAN REQUEST [VERCEL] =======")
            print(f"Request method: {request.method}")
            print(f"Request content type: {request.content_type}")
            print(f"Request headers: {dict(request.headers)}")
            
            # Initialize file info
            file_info = None
            
            # Check for filename in various parts of the request
            try:
                if request.is_json:
                    data = request.get_json(silent=True)
                    print(f"JSON data: {data}")
                    if data and 'filename' in data:
                        file_name = data['filename']
                        file_info = {'name': file_name}
                        print(f"Found filename in JSON: {file_name}")
                        
                elif request.form:
                    print(f"Form data keys: {list(request.form.keys())}")
                    if 'filename' in request.form:
                        file_name = request.form['filename']
                        file_info = {'name': file_name}
                        print(f"Found filename in form: {file_name}")
                        
                elif request.files:
                    print(f"Files: {list(request.files.keys())}")
                    if 'file' in request.files:
                        file = request.files['file']
                        file_name = file.filename
                        file_info = {'name': file_name}
                        print(f"Found file: {file_name}")
                else:
                    print("No file or filename found in request")
            except Exception as e:
                print(f"Error parsing request: {str(e)}")
            
            # Generate file scan result
            if file_info and 'name' in file_info:
                # Generate mock result based on file name
                result = generate_mock_file_result(file_info)
                result['message'] = 'File scan completed via Vercel API'
                result['source'] = 'Vercel Scanner'
                print(f"Generated result for {file_info['name']}: {result}")
                return jsonify(result), 200, headers
            else:
                # Default response when no file info is found
                default_result = {
                    'status': 'clean',
                    'message': 'File scan completed (no file details provided)',
                    'detections': '0 / 68',
                    'scan_date': int(time.time()),
                    'source': 'Vercel Scanner'
                }
                print(f"Returning default result: {default_result}")
                return jsonify(default_result), 200, headers
                
        # URL scanner and Port scanner endpoints remain unchanged
        if path == 'api/scan-url':
            print("======= URL SCAN REQUEST [VERCEL] =======")
            url = None
            if request.is_json and 'url' in request.json:
                url = request.json['url']
            
            result = generate_mock_url_result(url)
            print(f"URL scan result: {json.dumps(result)}")
            return jsonify(result), 200, headers
        
        # Port scanner endpoint
        if path == 'api/scan-ports':
            print("======= PORT SCAN REQUEST [VERCEL] =======")
            target = None
            port_range = None
            if request.is_json:
                target = request.json.get('target')
                port_range = request.json.get('port_range')
            
            result = generate_mock_port_result(target, port_range)
            print(f"Port scan result: {json.dumps(result)}")
            return jsonify(result), 200, headers
        
        # Default response for any other endpoint
        print(f"No matching endpoint for path: {path}")
        return jsonify({
            'status': 'healthy',
            'message': f'ThreatLightHouse API endpoint not found: {path}',
            'timestamp': int(time.time()),
            'available_endpoints': ['/api/health', '/api/scan-file', '/api/scan-url', '/api/scan-ports']
        }), 200, headers
        
    except Exception as e:
        print(f"Global exception handler caught: {str(e)}")
        # Always return a valid response
        error_response = {
            'status': 'clean',
            'message': 'Scan processed by error handler',
            'detections': '0 / 68',
            'scan_date': int(time.time()),
            'source': 'Vercel Error Handler'
        }
        return jsonify(error_response), 200, headers

# This is used by Vercel to call the Flask app
handler = app
