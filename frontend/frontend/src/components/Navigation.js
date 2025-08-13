import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="top-navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <h1>🌍 Trade Optimization System</h1>
        </div>
        <div className="nav-links">
          <Link 
            to="/crm" 
            className={location.pathname === '/crm' ? 'nav-link active' : 'nav-link'}
          >
            📊 Sales CRM
          </Link>
          <Link 
            to="/dashboard" 
            className={location.pathname === '/dashboard' ? 'nav-link active' : 'nav-link'}
          >
            🎯 AI Dashboard
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
