from flask import Flask, request, jsonify
import os
import sys
import traceback
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import tempfile
from flask_cors import CORS
import hashlib
import threading

from file_scanner import scan_file
from url_scanner import scan_url
from port_scanner import scan_ports
from report_generator import generate_report, get_report, get_all_reports

# Add this import at the top with other imports
from mock_scanner import mock_file_scan, mock_url_scan, mock_port_scan

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable verbose CORS for debugging
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Print environment info for debugging
print(f"API Key set: {'Yes' if os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY') else 'No'}")
print(f"Working directory: {os.getcwd()}")

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'exe', 'dll', 'zip', 'rar'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    # Add headers to allow cross-origin requests
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    
    # Additional headers to help with Vercel deployment
    response.headers.add('Cache-Control', 'no-cache, no-store, must-revalidate')
    response.headers.add('Pragma', 'no-cache')
    response.headers.add('Expires', '0')
    return response

# Set a global timeout for VT API requests
SCAN_TIMEOUT = 100  # Seconds

@app.route('/api/scan-file', methods=['POST', 'OPTIONS'])
def api_scan_file():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
        
    try:
        print("Starting file scan request")
        
        # IMPORTANT: Set this to False to always try real scanner first
        is_vercel = False
        print(f"Using real scanner for file scan")
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        print(f"Received file: {file.filename}")
        
        if file and allowed_file(file.filename):
            # Save to temporary file
            temp_dir = tempfile.gettempdir()
            filename = secure_filename(file.filename)
            file_path = os.path.join(temp_dir, filename)
            file.save(file_path)
            
            try:
                # Generate file hash
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                
                # Always try real scanner first
                print("Using real scanner for file")
                scan_result = scan_file(file_path, file_hash)
                
                # Generate report
                generate_report('file', {
                    'filename': filename,
                    'hash': file_hash,
                    'size': os.path.getsize(file_path),
                    'result': scan_result
                })
                
                return jsonify(scan_result)
                
            except Exception as e:
                print("Error in file scanning:", str(e))
                traceback.print_exc()
                
                # Only use mock as a last resort
                print("Using mock scanner as fallback")
                fallback_result = mock_file_scan(file_path, file_hash)
                return jsonify(fallback_result)
            finally:
                # Clean up temp file
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        pass
        
        return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        print("Unexpected error in file scanning API:", str(e))
        traceback.print_exc()
        
        # Return fallback data when everything else fails
        return jsonify({
            'status': 'error',
            'message': f'Error in scan service: {str(e)}',
            'source': 'Error Handler'
        })

@app.route('/api/scan-url', methods=['POST', 'OPTIONS'])
def api_scan_url():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
        
    try:
        print("Starting URL scan request")
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
        
        url = data['url']
        print(f"URL to scan: {url}")
        
        # IMPORTANT: Always use real scanner
        print("Using real URL scanner")
        
        try:
            # Always use real scanner first
            scan_result = scan_url(url)
            
            # Generate report
            generate_report('url', {
                'url': url,
                'result': scan_result
            })
            
            return jsonify(scan_result)
        except Exception as e:
            print(f"Real URL scanner failed: {str(e)}")
            traceback.print_exc()
            
            # Only use mock as fallback
            print("Using mock URL scanner as fallback")
            fallback_result = mock_url_scan(url)
            return jsonify(fallback_result)
            
    except Exception as e:
        print("Unexpected error in URL scanning API:", str(e))
        traceback.print_exc()
        
        # Return fallback data
        url = request.get_json().get('url', 'unknown')
        fallback_result = mock_url_scan(url)
        return jsonify(fallback_result)

@app.route('/api/scan-ports', methods=['POST', 'OPTIONS'])
def api_scan_ports():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
        
    try:
        print("Starting port scan request")
        data = request.get_json()
        
        if not data or 'target' not in data:
            return jsonify({'error': 'No target provided'}), 400
        
        target = data['target']
        port_range = data.get('port_range', '1-1000')
        
        print(f"Target: {target}, Port range: {port_range}")
        
        # IMPORTANT: Always use real scanner
        print("Using real port scanner")
        
        try:
            # Always use real scanner first
            scan_result = scan_ports(target, port_range)
            
            # Generate report
            generate_report('port', {
                'target': target,
                'port_range': port_range,
                'result': scan_result
            })
            
            return jsonify(scan_result)
        except Exception as e:
            print(f"Real port scanner failed: {str(e)}")
            traceback.print_exc()
            
            # Fall back to mock scanner if real scanner fails
            print("Using mock port scanner as fallback")
            scan_result = mock_port_scan(target, port_range)
            
            # Generate report
            generate_report('port', {
                'target': target,
                'port_range': port_range,
                'result': scan_result
            })
            
            return jsonify(scan_result)
            
    except Exception as e:
        print("Unexpected error in port scanning API:", str(e))
        traceback.print_exc()
        
        # Return fallback data
        if 'target' in request.get_json():
            target = request.get_json().get('target')
            port_range = request.get_json().get('port_range', '1-1000')
            fallback_result = mock_port_scan(target, port_range)
            return jsonify(fallback_result)
        
        return jsonify({
            'status': 'error',
            'message': 'Could not process port scan request',
            'source': 'Error Handler'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple endpoint to check if API is running"""
    api_key = os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY', '')
    return jsonify({
        'status': 'healthy',
        'api_key_configured': bool(api_key),
        'api_key_length': len(api_key) if api_key else 0
    })

# Comment out or disable report-related endpoints
# @app.route('/api/reports/<report_id>', methods=['GET'])
# def api_get_report(report_id):
#     """Get a specific report by ID"""
#     try:
#         report = get_report(report_id)
#         if not report:
#             return jsonify({'error': 'Report not found'}), 404
#         return jsonify(report)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/reports', methods=['GET'])
# def api_get_reports():
#     """Get all reports"""
#     try:
#         reports = get_all_reports()
#         return jsonify(reports)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# New helper function for background processing
def scan_file_background(file_path, file_hash, filename):
    try:
        scan_result = scan_file(file_path, file_hash)
        
        # Generate report
        generate_report('file', {
            'filename': filename,
            'hash': file_hash,
            'result': scan_result
        })
        
        print(f"Background scan completed for {filename}")
        
    except Exception as e:
        print(f"Error in background scan: {str(e)}")
        traceback.print_exc()
    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)

# Add a specific route for Vercel health check
@app.route('/', methods=['GET'])
def root():
    """Root endpoint for health checks"""
    return jsonify({
        'status': 'healthy',
        'message': 'ThreatLightHouse API is running'
    })

if __name__ == '__main__':
    # Increase timeout settings
    app.config['TIMEOUT'] = 300  # 5 minutes
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
