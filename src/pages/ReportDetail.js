import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { useSupabase } from '../context/SupabaseContext';
import LoadingSpinner from '../components/LoadingSpinner';

const ReportDetail = () => {
  const { reportId } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { supabase } = useSupabase();

  useEffect(() => {
    const fetchReport = async () => {
      try {
        // First try to get from Supabase
        const { data, error } = await supabase
          .from('reports')
          .select('*')
          .eq('id', reportId)
          .single();
          
        if (error) {
          throw error;
        }
        
        if (data) {
          setReport(data);
          setLoading(false);
          return;
        }
        
        // If not found in Supabase, try API
        const response = await axios.get(`/api/reports/${reportId}`);
        setReport(response.data);
      } catch (err) {
        console.error('Error fetching report:', err);
        setError('Failed to load report. It may not exist or has been deleted.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchReport();
  }, [reportId, supabase]);
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };
  
  if (loading) {
    return (
      <div className="card">
        <h2>Report Details</h2>
        <LoadingSpinner message="Loading report..." />
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="card">
        <h2>Error</h2>
        <p>{error}</p>
        <Link to="/reports">
          <button>Back to Reports</button>
        </Link>
      </div>
    );
  }
  
  if (!report) {
    return (
      <div className="card">
        <h2>Report Not Found</h2>
        <p>The requested report could not be found.</p>
        <Link to="/reports">
          <button>Back to Reports</button>
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>Report Details</h2>
          <Link to="/reports">
            <button>Back to Reports</button>
          </Link>
        </div>
        
        <div>
          <p><strong>Report ID:</strong> {report.id}</p>
          <p><strong>Scan Type:</strong> {report.scan_type.toUpperCase()}</p>
          <p><strong>Date:</strong> {formatDate(report.created_at)}</p>
        </div>
        
        {report.scan_type === 'file' && (
          <div className="result-container">
            <h3>File Scan Results</h3>
            <p><strong>File:</strong> {report.scan_data.filename}</p>
            <p><strong>Size:</strong> {Math.round(report.scan_data.size / 1024)} KB</p>
            <p><strong>Type:</strong> {report.scan_data.type}</p>
            <p><strong>Hash:</strong> {report.scan_data.hash}</p>
            <p><strong>Status:</strong> 
              <span className={`status-${report.scan_data.result.status === 'clean' ? 'safe' : 'malicious'}`}>
                {report.scan_data.result.status === 'clean' ? 'Safe' : 'Malicious'}
              </span>
            </p>
            {report.scan_data.result.detections && (
              <p><strong>Detections:</strong> {report.scan_data.result.detections}</p>
            )}
            {report.scan_data.result.engines && (
              <div>
                <p><strong>Engines:</strong></p>
                <ul>
                  <li>Total: {report.scan_data.result.engines.total}</li>
                  <li>Malicious: {report.scan_data.result.engines.malicious}</li>
                  <li>Suspicious: {report.scan_data.result.engines.suspicious}</li>
                </ul>
              </div>
            )}
            {report.scan_data.result.scan_date && (
              <p><strong>Scan Date:</strong> {formatDate(report.scan_data.result.scan_date * 1000)}</p>
            )}
          </div>
        )}
        
        {report.scan_type === 'url' && (
          <div className="result-container">
            <h3>URL Scan Results</h3>
            <p><strong>URL:</strong> {report.scan_data.url}</p>
            <p><strong>Status:</strong> 
              <span className={`status-${report.scan_data.result.status}`}>
                {report.scan_data.result.status === 'safe' ? 'Safe' : 
                 report.scan_data.result.status === 'suspicious' ? 'Suspicious' : 'Malicious'}
              </span>
            </p>
            {report.scan_data.result.source && (
              <p><strong>Source:</strong> {report.scan_data.result.source}</p>
            )}
            {report.scan_data.result.categories && report.scan_data.result.categories.length > 0 && (
              <div>
                <p><strong>Categories:</strong></p>
                <ul>
                  {report.scan_data.result.categories.map((category, index) => (
                    <li key={index}>{category}</li>
                  ))}
                </ul>
              </div>
            )}
            {report.scan_data.result.detections && (
              <p><strong>Detections:</strong> {report.scan_data.result.detections}</p>
            )}
            {report.scan_data.result.screenshot && (
              <div>
                <p><strong>Screenshot:</strong></p>
                <img 
                  src={report.scan_data.result.screenshot} 
                  alt="URL Screenshot" 
                  style={{ maxWidth: '100%', border: '1px solid #ddd' }}
                />
              </div>
            )}
          </div>
        )}
        
        {report.scan_type === 'port' && (
          <div className="result-container">
            <h3>Port Scan Results</h3>
            <p><strong>Target:</strong> {report.scan_data.target}</p>
            <p><strong>IP Address:</strong> {report.scan_data.result.target_ip}</p>
            <p><strong>Port Range:</strong> {report.scan_data.port_range}</p>
            <p><strong>Total Ports Scanned:</strong> {report.scan_data.result.total_ports_scanned}</p>
            <p><strong>Scan Date:</strong> {formatDate(report.scan_data.result.scan_date * 1000)}</p>
            
            {report.scan_data.result.open_ports && report.scan_data.result.open_ports.length > 0 ? (
              <div>
                <p><strong>Open Ports:</strong></p>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Port</th>
                      <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Service</th>
                    </tr>
                  </thead>
                  <tbody>
                    {report.scan_data.result.open_ports.map((port, index) => (
                      <tr key={index}>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{port.port}</td>
                        <td style={{ border: '1px solid #ddd', padding: '8px' }}>{port.service}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p>No open ports found in the specified range.</p>
            )}
          </div>
        )}
        
        {/* Raw JSON data section for debugging */}
        <div style={{ marginTop: '30px' }}>
          <details>
            <summary>Raw Report Data</summary>
            <pre style={{ 
              background: '#f5f5f5', 
              padding: '10px', 
              overflow: 'auto',
              maxHeight: '300px',
              fontSize: '12px'
            }}>
              {JSON.stringify(report, null, 2)}
            </pre>
          </details>
        </div>
      </div>
    </div>
  );
};

export default ReportDetail;
