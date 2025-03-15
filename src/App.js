import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import FileScanner from './pages/FileScanner';
import URLScanner from './pages/URLScanner';
import PortScanner from './pages/PortScanner';
import { SupabaseProvider } from './context/SupabaseContext';
import Footer from './components/Footer';

function App() {
  return (
    <SupabaseProvider>
      <Router>
        <div className="App">
          <Navbar />
          <main className="main-content">
            <div className="container">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/file-scan" element={<FileScanner />} />
                <Route path="/url-scan" element={<URLScanner />} />
                <Route path="/port-scan" element={<PortScanner />} />
              </Routes>
            </div>
          </main>
          <Footer />
        </div>
      </Router>
    </SupabaseProvider>
  );
}

export default App;
