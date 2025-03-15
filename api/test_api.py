import os
import requests
import json

def test_api_routes():
    """
    Simple test script to verify API routes are working.
    Can be run locally or in the Vercel deployment to check endpoints.
    """
    base_url = os.environ.get('API_BASE_URL', 'http://localhost:5000')
    
    endpoints = [
        {'url': '/api/health', 'method': 'GET', 'payload': None},
        {'url': '/', 'method': 'GET', 'payload': None}
    ]
    
    success = True
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint['url']}"
        method = endpoint['method']
        payload = endpoint['payload']
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=payload, timeout=10)
            else:
                print(f"Unsupported method: {method}")
                success = False
                continue
                
            if response.status_code in (200, 201):
                print(f"✅ {method} {url} - Success ({response.status_code})")
                print(f"   Response: {json.dumps(response.json(), indent=2)[:100]}...")
            else:
                print(f"❌ {method} {url} - Failed ({response.status_code})")
                print(f"   Response: {response.text[:100]}...")
                success = False
                
        except Exception as e:
            print(f"❌ {method} {url} - Error: {str(e)}")
            success = False
    
    return success

if __name__ == "__main__":
    print("Testing API endpoints...")
    if test_api_routes():
        print("All API tests passed!")
    else:
        print("Some API tests failed.")
