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
    return response

# Set a global timeout for VT API requests
SCAN_TIMEOUT = 100  # Seconds

@app.route('/api/scan-file', methods=['POST', 'OPTIONS'])
def api_scan_file():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'})
        
    try:
        print("Starting file scan request")
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
            
            # Check file size - limit to 32MB to avoid timeout issues
            file_size = os.path.getsize(file_path)
            if file_size > 32 * 1024 * 1024:
                return jsonify({
                    'status': 'error',
                    'message': 'File is too large. Maximum allowed size is 32MB.'
                }), 413
            
            try:
                # Generate file hash
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                
                print(f"File hash: {file_hash}")
                
                # Start a background thread for scanning large files
                if file_size > 10 * 1024 * 1024:  # 10MB
                    print("Large file detected, processing in background")
                    result = {
                        'status': 'pending',
                        'message': 'File is being processed in the background. This may take a few minutes.'
                    }
                    threading.Thread(target=scan_file_background, args=(file_path, file_hash, filename)).start()
                else:
                    # Scan file with timeout
                    scan_result = scan_file(file_path, file_hash)
                    
                    # Generate report ID but don't include in response
                    generate_report('file', {
                        'filename': filename,
                        'hash': file_hash,
                        'result': scan_result
                    })
                    
                    result = scan_result
                
                return jsonify(result)
                
            except Exception as e:
                print("Error in file scanning:", str(e))
                traceback.print_exc()
                return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500
            finally:
                # Clean up temp file
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        print("Unexpected error in file scanning API:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

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
        
        try:
            scan_result = scan_url(url)
            
            print(f"URL scan result: {scan_result}")
            
            # Generate report - this will still happen in the backend
            # but we won't return the report_id to the frontend
            report_id = generate_report('url', {
                'url': url,
                'result': scan_result
            })
            
            return jsonify(scan_result)
            
        except Exception as e:
            print("Error in URL scanning:", str(e))
            traceback.print_exc()
            return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500
    except Exception as e:
        print("Unexpected error in URL scanning API:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

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
        
        # Limit the port range to avoid timeout
        if ',' in port_range:
            port_count = len(port_range.split(','))
            if port_count > 100:
                return jsonify({
                    'status': 'error',
                    'message': 'Too many ports specified. Please limit to 100 ports maximum.'
                }), 400
        elif '-' in port_range:
            try:
                start, end = map(int, port_range.split('-'))
                if end - start > 1000:
                    return jsonify({
                        'status': 'error',
                        'message': 'Port range too large. Please limit to 1000 ports maximum.'
                    }), 400
            except:
                pass
        
        try:
            scan_result = scan_ports(target, port_range)
            
            print(f"Port scan result: {scan_result}")
            
            # Generate report - this will still happen in the backend
            # but we won't return the report_id to the frontend
            report_id = generate_report('port', {
                'target': target,
                'port_range': port_range,
                'result': scan_result
            })
            
            # Don't include report_id in response
            # scan_result['report_id'] = report_id
            return jsonify(scan_result)
            
        except Exception as e:
            print("Error in port scanning:", str(e))
            traceback.print_exc()
            return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500
    except Exception as e:
        print("Unexpected error in port scanning API:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

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

if __name__ == '__main__':
    # Increase timeout settings
    app.config['TIMEOUT'] = 300  # 5 minutes
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
