import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ProfitChart, CostChart, PerformanceChart } from './Charts';
import './SalesCRM.css';

const API_BASE_URL = 'http://localhost:8000/api';

const SalesCRM = () => {
  const [activeSection, setActiveSection] = useState('dealers');
  const [dealers, setDealers] = useState([]);
  const [countries, setCountries] = useState([]);
  const [tariffs, setTariffs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    country: '',
    product: '',
    performance: ''
  });
  const [manualData, setManualData] = useState('');
  const [profitData, setProfitData] = useState(null);
  const [costData, setCostData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch dealers data
      const dealersResponse = await axios.get(`${API_BASE_URL}/data/dealers`);
      setDealers(dealersResponse.data);

      // Fetch countries data
      const countriesResponse = await axios.get(`${API_BASE_URL}/data/countries`);
      setCountries(countriesResponse.data);

      // Fetch tariffs data
      const tariffsResponse = await axios.get(`${API_BASE_URL}/data/tariffs`);
      setTariffs(tariffsResponse.data);

      // Fetch profit and cost analytics
      const analyticsResponse = await axios.get(`${API_BASE_URL}/data/analytics`);
      setProfitData(analyticsResponse.data.profit_data);
      setCostData(analyticsResponse.data.cost_data);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      
      try {
        await axios.post(`${API_BASE_URL}/data/upload-csv`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        alert('File uploaded successfully!');
        fetchData(); // Refresh data
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('Error uploading file. Please try again.');
      }
    }
  };

  const handleManualDataSubmit = async () => {
    if (manualData.trim()) {
      try {
        await axios.post(`${API_BASE_URL}/data/manual-entry`, {
          data: manualData
        });
        alert('Data submitted successfully!');
        setManualData('');
        fetchData(); // Refresh data
      } catch (error) {
        console.error('Error submitting manual data:', error);
        alert('Error submitting data. Please try again.');
      }
    }
  };

  const filteredDealers = dealers.filter(dealer => {
    return (!filters.country || dealer.country === filters.country) &&
           (!filters.product || dealer.main_product === filters.product) &&
           (!filters.performance || dealer.performance_rating === filters.performance);
  });

  const getPerformanceColor = (performance) => {
    if (performance >= 80) return 'high';
    if (performance >= 60) return 'medium';
    return 'low';
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <h2>Loading Sales CRM...</h2>
      </div>
    );
  }

  return (
    <div className="sales-crm">
      {/* Sidebar Navigation */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h1>Sales CRM</h1>
        </div>
        <nav className="sidebar-nav">
          <button 
            className={`nav-item ${activeSection === 'dealers' ? 'active' : ''}`}
            onClick={() => setActiveSection('dealers')}
          >
            <span className="nav-icon">👥</span>
            Dealers
          </button>
          <button 
            className={`nav-item ${activeSection === 'tariffs' ? 'active' : ''}`}
            onClick={() => setActiveSection('tariffs')}
          >
            <span className="nav-icon">💰</span>
            Tariffs
          </button>
          <button 
            className={`nav-item ${activeSection === 'profit' ? 'active' : ''}`}
            onClick={() => setActiveSection('profit')}
          >
            <span className="nav-icon">📊</span>
            Profit
          </button>
          <button 
            className={`nav-item ${activeSection === 'costs' ? 'active' : ''}`}
            onClick={() => setActiveSection('costs')}
          >
            <span className="nav-icon">📈</span>
            Costs
          </button>
          <button 
            className={`nav-item ${activeSection === 'recommendations' ? 'active' : ''}`}
            onClick={() => setActiveSection('recommendations')}
          >
            <span className="nav-icon">💡</span>
            Recommendations
          </button>
        </nav>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {activeSection === 'dealers' && (
          <div className="content-section">
            {/* Dealer Database Section */}
            <div className="section-header">
              <h2>Dealer Database</h2>
              <div className="filters">
                <select 
                  value={filters.country} 
                  onChange={(e) => handleFilterChange('country', e.target.value)}
                  className="filter-select"
                >
                  <option value="">Country</option>
                  {countries.map(country => (
                    <option key={country.id} value={country.name}>{country.name}</option>
                  ))}
                </select>
                <select 
                  value={filters.product} 
                  onChange={(e) => handleFilterChange('product', e.target.value)}
                  className="filter-select"
                >
                  <option value="">Product</option>
                  <option value="Electronics">Electronics</option>
                  <option value="Textiles">Textiles</option>
                  <option value="Automotive">Automotive</option>
                  <option value="Agriculture">Agriculture</option>
                </select>
                <select 
                  value={filters.performance} 
                  onChange={(e) => handleFilterChange('performance', e.target.value)}
                  className="filter-select"
                >
                  <option value="">Performance</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>
            </div>

            <div className="dealers-table">
              <table>
                <thead>
                  <tr>
                    <th>Dealer</th>
                    <th>Country</th>
                    <th>Product</th>
                    <th>Performance</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredDealers.map(dealer => (
                    <tr key={dealer.id}>
                      <td>
                        <div className="dealer-info">
                          <strong>{dealer.name}</strong>
                          <small>{dealer.contact_email}</small>
                        </div>
                      </td>
                      <td>{dealer.country}</td>
                      <td>{dealer.main_product}</td>
                      <td>
                        <span className={`performance-badge ${getPerformanceColor(dealer.performance_rating)}`}>
                          {dealer.performance_rating}%
                        </span>
                      </td>
                      <td>
                        <button className="action-btn">View</button>
                        <button className="action-btn">Edit</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeSection === 'tariffs' && (
          <div className="content-section">
            {/* Country Tariff/Tax Dashboard */}
            <div className="section-header">
              <h2>Country Tariff/Tax Dashboard</h2>
            </div>

            <div className="tariffs-table">
              <table>
                <thead>
                  <tr>
                    <th>Country</th>
                    <th>Tariff</th>
                    <th>Tax</th>
                  </tr>
                </thead>
                <tbody>
                  {tariffs.map(tariff => (
                    <tr key={tariff.id}>
                      <td>{tariff.country}</td>
                      <td>{tariff.tariff_rate}%</td>
                      <td>{tariff.tax_rate}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {(activeSection === 'profit' || activeSection === 'costs') && (
          <div className="content-section">
            {/* Charts Section */}
            <div className="charts-grid">
              <div className="chart-card">
                <h3>Profit vs Time by Country</h3>
                <div className="chart-value">$1.2M</div>
                <div className="chart-meta">
                  <span>Last 12 Months</span>
                  <span className="trend positive">+15%</span>
                </div>
                <div className="chart-placeholder">
                  <ProfitChart data={profitData} />
                </div>
              </div>

              <div className="chart-card">
                <h3>Cost Breakdown per Product</h3>
                <div className="chart-value">$500K</div>
                <div className="chart-meta">
                  <span>Last 12 Months</span>
                  <span className="trend negative">-5%</span>
                </div>
                <div className="cost-breakdown">
                  <CostChart data={costData} />
                </div>
              </div>
            </div>

            {/* Dealer Comparison Charts */}
            <div className="section-header">
              <h2>Dealer Comparison Charts</h2>
            </div>
            <div className="comparison-grid">
              <div className="comparison-card">
                <h3>Dealer Performance</h3>
                <PerformanceChart dealers={dealers} />
              </div>

              <div className="comparison-card">
                <h3>Dealer Costs</h3>
                <div className="cost-comparison">
                  {dealers.slice(0, 5).map(dealer => (
                    <div key={dealer.id} className="cost-item">
                      <span>{dealer.name}</span>
                      <span className="cost-value">${dealer.avg_cost || 0}K</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeSection === 'recommendations' && (
          <div className="content-section">
            {/* Trade Recommendation Engine Output */}
            <div className="section-header">
              <h2>Trade Recommendation Engine Output</h2>
            </div>

            <div className="recommendations-grid">
              <div className="recommendation-card rec-1">
                <div className="rec-overlay">
                  <h3>Recommendation 1</h3>
                  <p>Increase sales in the USA by focusing on Product X with Dealer A.</p>
                </div>
              </div>
              <div className="recommendation-card rec-2">
                <div className="rec-overlay">
                  <h3>Recommendation 2</h3>
                  <p>Reduce costs in Canada by optimizing Product Y distribution with Dealer B.</p>
                </div>
              </div>
            </div>

            {/* Data Upload/Edit Section */}
            <div className="section-header">
              <h2>Data Upload/Edit</h2>
            </div>

            <div className="data-section">
              <div className="data-input">
                <label>Manual Data Entry</label>
                <input
                  type="text"
                  value={manualData}
                  onChange={(e) => setManualData(e.target.value)}
                  placeholder="Enter data here"
                  className="manual-input"
                />
                <button onClick={handleManualDataSubmit} className="submit-btn">
                  Submit Data
                </button>
              </div>

              <div className="data-upload">
                <label>Upload CSV File</label>
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileUpload}
                  className="file-input"
                  id="csv-upload"
                />
                <label htmlFor="csv-upload" className="upload-btn">
                  Upload CSV
                </label>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SalesCRM;
