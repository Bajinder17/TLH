from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'healthy',
        'message': 'ThreatLightHouse API is running in Vercel'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    api_key = os.environ.get('REACT_APP_VIRUSTOTAL_API_KEY', '')
    return jsonify({
        'status': 'healthy',
        'api_key_configured': bool(api_key),
        'api_key_length': len(api_key) if api_key else 0
    })

# Mock endpoints for Vercel deployment
@app.route('/api/scan-file', methods=['POST'])
def mock_scan_file():
    return jsonify({
        'status': 'clean',
        'message': 'File scan completed successfully (demo mode)',
        'detections': '0 / 68',
        'source': 'Vercel Mock Scanner'
    })

@app.route('/api/scan-url', methods=['POST'])
def mock_scan_url():
    return jsonify({
        'status': 'safe',
        'message': 'URL scan completed successfully (demo mode)',
        'detections': '0 / 86',
        'source': 'Vercel Mock Scanner'
    })

@app.route('/api/scan-ports', methods=['POST'])
def mock_scan_ports():
    return jsonify({
        'status': 'completed',
        'message': 'Port scan completed successfully (demo mode)',
        'open_ports': [],
        'target_ip': '192.168.1.1',
        'total_ports_scanned': 1000,
        'source': 'Vercel Mock Scanner'
    })

if __name__ == '__main__':
    app.run(debug=True)
