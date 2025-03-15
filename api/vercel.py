import os
import sys
from flask import Flask

# Simple Flask app for Vercel
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return {
        'status': 'healthy',
        'message': 'ThreatLightHouse API is running',
        'path': path
    }

# This handler is used by Vercel
handler = app
