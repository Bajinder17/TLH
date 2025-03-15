import React, { useEffect, useState } from 'react';
import { useSupabase } from '../context/SupabaseContext';
import LoadingSpinner from '../components/LoadingSpinner';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const { getReports } = useSupabase();

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const data = await getReports();
        setReports(data || []);
      } catch (error) {
        console.error('Error fetching reports:', error);
        alert('Failed to load reports');
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, [getReports]);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  // Filter reports based on selected scan type
  const filteredReports = filter === 'all' 
    ? reports 
    : reports.filter(report => report.scan_type === filter);

  return (
    <div>
      <div className="card">
        <h2>Scan Reports</h2>
        <p>View history of all scans performed</p>
        
        <div style={{ marginBottom: '20px' }}>
          <label htmlFor="filter">Filter by scan type: </label>
          <select 
            id="filter" 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            style={{ padding: '8px', marginLeft: '10px' }}
          >
            <option value="all">All Reports</option>
            <option value="file">File Scans</option>
            <option value="url">URL Scans</option>
            <option value="port">Port Scans</option>
          </select>
        </div>
        
        {loading ? (
          <LoadingSpinner message="Loading reports..." />
        ) : filteredReports.length > 0 ? (
          <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
            {filteredReports.map((report) => (
              <div key={report.id} className="card" style={{ margin: '10px 0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                  <span><strong>Scan Type:</strong> {report.scan_type.toUpperCase()}</span>
                  <span><strong>Date:</strong> {formatDate(report.created_at)}</span>
                </div>
                
                {report.scan_type === 'file' && (
                  <div>
                    <p><strong>File:</strong> {report.scan_data.filename}</p>
                    <p><strong>Size:</strong> {Math.round(report.scan_data.size / 1024)} KB</p>
                    <p><strong>Status:</strong> 
                      <span className={`status-${report.scan_data.result.status === 'clean' ? 'safe' : 'malicious'}`}>
                        {report.scan_data.result.status === 'clean' ? 'Safe' : 'Malicious'}
                      </span>
                    </p>
                  </div>
                )}
                
                {report.scan_type === 'url' && (
                  <div>
                    <p><strong>URL:</strong> {report.scan_data.url}</p>
                    <p><strong>Status:</strong>
                      <span className={`status-${report.scan_data.result.status}`}>
                        {report.scan_data.result.status === 'safe' ? 'Safe' : 
                         report.scan_data.result.status === 'suspicious' ? 'Suspicious' : 'Malicious'}
                      </span>
                    </p>
                  </div>
                )}
                
                {report.scan_type === 'port' && (
                  <div>
                    <p><strong>Target:</strong> {report.scan_data.target}</p>
                    <p><strong>Port Range:</strong> {report.scan_data.port_range}</p>
                    <p><strong>Open Ports:</strong> {report.scan_data.result.open_ports?.length || 0}</p>
                  </div>
                )}
                
                <button 
                  onClick={() => window.open(`/report/${report.id}`, '_blank')}
                  style={{ marginTop: '10px' }}
                >
                  View Full Report
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p>No reports found. Start scanning to generate reports!</p>
        )}
      </div>
    </div>
  );
};

export default Reports;
