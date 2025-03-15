# ThreatLightHouse

ThreatLightHouse is a comprehensive threat detection platform that allows users to scan files, URLs, and network ports for security threats.

## Features

- **File Scanning**: Upload and scan files for malware and viruses using VirusTotal API
- **URL Scanning**: Check if websites are malicious or contain threats using VirusTotal
- **Port Scanning**: Scan network ports for security vulnerabilities
- **Report Generation**: Save and view detailed reports of all scans

## Technology Stack

- Frontend: React
- Backend: Python with Flask
- Database: Supabase
- APIs: VirusTotal

## Setup Instructions

### Prerequisites

- Node.js v16+ and npm
- Python 3.8+
- API key for VirusTotal
- Supabase account and project (or you can use local JSON files as a fallback)

### Installation

1. Clone the repository
2. Install frontend dependencies:
   ```
   npm install
   ```
3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your API keys:
   ```
   REACT_APP_SUPABASE_URL=your_supabase_url
   REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
   REACT_APP_VIRUSTOTAL_API_KEY=your_virustotal_api_key
   ```

### Setting up Supabase

1. Create a new Supabase project
2. Create a `reports` table with the following structure:
   - `id` (UUID, primary key)
   - `scan_type` (text)
   - `scan_data` (jsonb)
   - `created_at` (timestamp with timezone)

### Running the Application

1. Start the React frontend:
   ```
   npm start
   ```
2. In another terminal, start the Python API server:
   ```
   npm run api
   ```
3. Access the application at `http://localhost:3000`

## Deployment

The application is configured for easy deployment to Vercel:

```
vercel
```

## API Documentation

### File Scan API

`POST /api/scan-file`
- Form data: `file` (The file to scan)
- Response: JSON with scan results

### URL Scan API

`POST /api/scan-url`
- JSON data: `{ "url": "https://example.com" }`
- Response: JSON with scan results

### Port Scan API

`POST /api/scan-ports`
- JSON data: `{ "target": "192.168.1.1", "port_range": "1-1000" }`
- Response: JSON with scan results

## License

MIT
