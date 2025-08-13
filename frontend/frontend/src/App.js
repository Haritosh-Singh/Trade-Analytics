import React from 'react';
import './App.css';
import TradeDashboard from './components/TradeDashboard';
import SalesCRM from './components/SalesCRM';
import Navigation from './components/Navigation';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<Navigate to="/crm" replace />} />
          <Route path="/dashboard" element={<TradeDashboard />} />
          <Route path="/crm" element={<SalesCRM />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
