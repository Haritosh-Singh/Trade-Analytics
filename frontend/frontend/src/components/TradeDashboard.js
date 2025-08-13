import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TradeDashboard.css';

const API_BASE_URL = 'http://localhost:8000/api';

const TradeDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [predictionData, setPredictionData] = useState(null);
  const [predictionForm, setPredictionForm] = useState({
    dealer_id: '',
    product_id: '',
    destination_country_id: '',
    quantity: '',
    transport_mode: 'sea'
  });

  // Fetch dashboard data
  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/data/dashboard-summary`);
      setDashboardData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const handlePredictionSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE_URL}/predictions/predict-trade`, {
        ...predictionForm,
        dealer_id: parseInt(predictionForm.dealer_id),
        product_id: parseInt(predictionForm.product_id),
        destination_country_id: parseInt(predictionForm.destination_country_id),
        quantity: parseInt(predictionForm.quantity)
      });
      setPredictionData(response.data);
    } catch (error) {
      console.error('Error making prediction:', error);
      alert('Error making prediction. Please check your inputs.');
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <h2>Loading Trade Analytics Dashboard...</h2>
      </div>
    );
  }

  return (
    <div className="trade-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>🌍 AI-Powered Import-Export Optimization</h1>
          <p>India's Intelligent Trade Analytics Platform</p>
        </div>
        <div className="header-stats">
          <div className="stat-card">
            <span className="stat-value">{dashboardData?.summary?.total_transactions || 0}</span>
            <span className="stat-label">Total Trades</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{dashboardData?.summary?.avg_profit_margin || 0}%</span>
            <span className="stat-label">Avg Profit</span>
          </div>
          <div className="stat-card">
            <span className="stat-value">{formatCurrency(dashboardData?.summary?.total_trade_value || 0)}</span>
            <span className="stat-label">Trade Value</span>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="dashboard-nav">
        <button 
          className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`nav-tab ${activeTab === 'predictions' ? 'active' : ''}`}
          onClick={() => setActiveTab('predictions')}
        >
          🎯 AI Predictions
        </button>
        <button 
          className={`nav-tab ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📈 Analytics
        </button>
        <button 
          className={`nav-tab ${activeTab === 'dealers' ? 'active' : ''}`}
          onClick={() => setActiveTab('dealers')}
        >
          🏭 Dealers
        </button>
      </nav>

      {/* Main Content */}
      <main className="dashboard-main">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            {/* Key Metrics */}
            <section className="metrics-section">
              <h2>📈 Key Performance Metrics</h2>
              <div className="metrics-grid">
                <div className="metric-card">
                  <h3>Active Dealers</h3>
                  <div className="metric-value">{dashboardData?.summary?.active_dealers || 0}</div>
                  <div className="metric-trend positive">↗ Growing</div>
                </div>
                <div className="metric-card">
                  <h3>Countries Served</h3>
                  <div className="metric-value">{dashboardData?.summary?.countries_served || 0}</div>
                  <div className="metric-trend stable">→ Stable</div>
                </div>
                <div className="metric-card">
                  <h3>Products Available</h3>
                  <div className="metric-value">{dashboardData?.summary?.products_available || 0}</div>
                  <div className="metric-trend positive">↗ Expanding</div>
                </div>
                <div className="metric-card">
                  <h3>Monthly Growth</h3>
                  <div className="metric-value">{dashboardData?.trends?.monthly_growth || 0}%</div>
                  <div className="metric-trend positive">↗ Strong</div>
                </div>
              </div>
            </section>

            {/* Top Countries */}
            <section className="countries-section">
              <h2>🏆 Top Performing Countries</h2>
              <div className="countries-grid">
                {dashboardData?.top_countries?.map((country, index) => (
                  <div key={index} className="country-card">
                    <div className="country-rank">#{index + 1}</div>
                    <div className="country-info">
                      <h3>{country.country}</h3>
                      <div className="country-stats">
                        <span>{country.transactions} transactions</span>
                        <span>{country.avg_profit}% avg profit</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Recent Transactions */}
            <section className="transactions-section">
              <h2>📋 Recent Trade Transactions</h2>
              <div className="transactions-table">
                <table>
                  <thead>
                    <tr>
                      <th>Transaction ID</th>
                      <th>Dealer</th>
                      <th>Country</th>
                      <th>Profit Margin</th>
                      <th>Status</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dashboardData?.recent_transactions?.map((transaction, index) => (
                      <tr key={index}>
                        <td>{transaction.transaction_id}</td>
                        <td>{transaction.dealer}</td>
                        <td>{transaction.country}</td>
                        <td className={transaction.profit_margin > 15 ? 'profit-high' : transaction.profit_margin > 10 ? 'profit-medium' : 'profit-low'}>
                          {transaction.profit_margin}%
                        </td>
                        <td>
                          <span className={`status ${transaction.status}`}>
                            {transaction.status}
                          </span>
                        </td>
                        <td>{new Date(transaction.order_date).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </div>
        )}

        {activeTab === 'predictions' && (
          <div className="predictions-tab">
            <div className="predictions-layout">
              <div className="prediction-form-section">
                <h2>🎯 AI Trade Prediction</h2>
                <form onSubmit={handlePredictionSubmit} className="prediction-form">
                  <div className="form-group">
                    <label>Dealer ID:</label>
                    <input
                      type="number"
                      value={predictionForm.dealer_id}
                      onChange={(e) => setPredictionForm({...predictionForm, dealer_id: e.target.value})}
                      min="1"
                      max="30"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Product ID:</label>
                    <input
                      type="number"
                      value={predictionForm.product_id}
                      onChange={(e) => setPredictionForm({...predictionForm, product_id: e.target.value})}
                      min="1"
                      max="50"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Destination Country ID:</label>
                    <input
                      type="number"
                      value={predictionForm.destination_country_id}
                      onChange={(e) => setPredictionForm({...predictionForm, destination_country_id: e.target.value})}
                      min="2"
                      max="10"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Quantity:</label>
                    <input
                      type="number"
                      value={predictionForm.quantity}
                      onChange={(e) => setPredictionForm({...predictionForm, quantity: e.target.value})}
                      min="1"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Transport Mode:</label>
                    <select
                      value={predictionForm.transport_mode}
                      onChange={(e) => setPredictionForm({...predictionForm, transport_mode: e.target.value})}
                    >
                      <option value="sea">Sea Freight</option>
                      <option value="air">Air Freight</option>
                      <option value="road">Road Transport</option>
                      <option value="rail">Rail Transport</option>
                    </select>
                  </div>
                  <button type="submit" className="predict-button">
                    🔮 Predict Trade Outcome
                  </button>
                </form>
              </div>

              {predictionData && (
                <div className="prediction-results-section">
                  <h2>📊 Prediction Results</h2>
                  <div className="prediction-results">
                    <div className="result-card main-prediction">
                      <h3>Profit Prediction</h3>
                      <div className="prediction-value">
                        {predictionData.predicted_profit_margin.toFixed(2)}%
                      </div>
                      <div className="confidence">
                        Confidence: {(predictionData.confidence_score * 100).toFixed(1)}%
                      </div>
                    </div>
                    
                    <div className="result-card">
                      <h3>Delivery Time</h3>
                      <div className="prediction-value">
                        {predictionData.predicted_delivery_days} days
                      </div>
                    </div>
                    
                    <div className="result-card">
                      <h3>Total Cost</h3>
                      <div className="prediction-value">
                        {formatCurrency(predictionData.total_cost_estimate)}
                      </div>
                    </div>
                    
                    <div className="result-card recommendation">
                      <h3>AI Recommendation</h3>
                      <div className="recommendation-text">
                        {predictionData.recommendation}
                      </div>
                    </div>
                    
                    <div className="result-card risk-analysis">
                      <h3>Risk Analysis</h3>
                      <div className="risk-factors">
                        {Object.entries(predictionData.risk_factors).map(([factor, value]) => (
                          <div key={factor} className="risk-item">
                            <span>{factor.replace('_', ' ')}</span>
                            <div className="risk-bar">
                              <div 
                                className="risk-fill" 
                                style={{width: `${value * 100}%`}}
                              ></div>
                            </div>
                            <span>{(value * 100).toFixed(1)}%</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="analytics-tab">
            <h2>📈 Advanced Trade Analytics</h2>
            <div className="analytics-grid">
              <div className="analytics-card">
                <h3>Profit Trend Analysis</h3>
                <div className="chart-placeholder">
                  <p>📊 Profit margins trending upward by 12.5% this quarter</p>
                  <div className="trend-indicator positive">↗ +12.5%</div>
                </div>
              </div>
              
              <div className="analytics-card">
                <h3>Country Performance</h3>
                <div className="chart-placeholder">
                  <p>🌍 Top 3 countries generating 65% of total revenue</p>
                  <div className="performance-list">
                    {dashboardData?.top_countries?.slice(0, 3).map((country, index) => (
                      <div key={index} className="performance-item">
                        <span>{country.country}</span>
                        <span>{country.avg_profit}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              
              <div className="analytics-card">
                <h3>Delivery Performance</h3>
                <div className="chart-placeholder">
                  <p>🚛 Average delivery time: 40.8 days</p>
                  <div className="delivery-stats">
                    <div>On-time delivery: 85%</div>
                    <div>Delayed shipments: 15%</div>
                  </div>
                </div>
              </div>
              
              <div className="analytics-card">
                <h3>Risk Assessment</h3>
                <div className="chart-placeholder">
                  <p>⚠️ Overall trade risk: Low-Medium</p>
                  <div className="risk-summary">
                    <div className="risk-low">Low Risk: 60%</div>
                    <div className="risk-medium">Medium Risk: 35%</div>
                    <div className="risk-high">High Risk: 5%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'dealers' && (
          <div className="dealers-tab">
            <h2>🏭 Dealer Performance Dashboard</h2>
            <div className="dealers-grid">
              {dashboardData?.dealer_performance?.map((dealer, index) => (
                <div key={index} className="dealer-card">
                  <div className="dealer-header">
                    <h3>{dealer.name}</h3>
                    <span className="dealer-country">{dealer.country}</span>
                  </div>
                  <div className="dealer-metrics">
                    <div className="dealer-metric">
                      <span>Avg Profit:</span>
                      <span className={dealer.avg_profit > 15 ? 'profit-high' : dealer.avg_profit > 10 ? 'profit-medium' : 'profit-low'}>
                        {dealer.avg_profit}%
                      </span>
                    </div>
                    <div className="dealer-metric">
                      <span>Transactions:</span>
                      <span>{dealer.transactions}</span>
                    </div>
                    <div className="dealer-metric">
                      <span>Rating:</span>
                      <span className="rating">{'⭐'.repeat(Math.floor(dealer.rating))}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default TradeDashboard;
