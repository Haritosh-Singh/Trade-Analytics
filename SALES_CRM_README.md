# Sales CRM - Trade Optimization System

A comprehensive web-based Sales CRM system for the Trade Optimization Platform, featuring dealer management, tariff tracking, analytics, and AI-powered recommendations.

## 🌟 Features

### 📊 Sales CRM Dashboard
- **Dealer Database**: Complete dealer information with filtering by country, product, and performance
- **Country Tariff/Tax Dashboard**: Real-time tariff and tax rates for different countries
- **Analytics & Charts**: Interactive charts showing profit trends and cost breakdowns
- **Trade Recommendations**: AI-powered trade recommendations with visual insights
- **Data Management**: Manual data entry and CSV file upload capabilities

### 🎯 Key Components

#### 1. Dealer Management
- Filter dealers by country, product type, and performance rating
- View dealer contact information, performance metrics, and transaction history
- Performance ratings with color-coded indicators (High/Medium/Low)
- Export and edit dealer information

#### 2. Tariff & Tax Tracking
- Country-wise tariff rates and tax information
- Real-time updates on duty rates and additional taxes
- Historical tariff data and trends

#### 3. Interactive Analytics
- **Profit vs Time by Country**: Line chart showing profit trends over time
- **Cost Breakdown per Product**: Bar chart displaying cost distribution
- **Dealer Performance Comparison**: Horizontal bar charts comparing dealer metrics
- **Cost Analysis**: Detailed cost comparison between dealers

#### 4. Trade Recommendations Engine
- AI-generated trade recommendations with visual cards
- Specific actionable advice for increasing sales and reducing costs
- Market opportunity identification
- Risk assessment and mitigation strategies

#### 5. Data Upload & Management
- Manual data entry interface
- CSV file upload functionality
- Data validation and processing
- Real-time data synchronization

## 🚀 Getting Started

### Prerequisites
- Node.js 14+ and npm
- Python 3.8+ with virtual environment
- FastAPI backend running on port 8000

### Frontend Setup
```bash
cd frontend/frontend
npm install
npm start
```

### Backend Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pandas python-multipart

# Start backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the Application
- **Sales CRM**: http://localhost:3000/crm
- **AI Dashboard**: http://localhost:3000/dashboard
- **API Documentation**: http://localhost:8000/docs

## 📈 API Endpoints

### Dealer Management
- `GET /api/data/dealers` - Get all dealers with performance metrics
- `GET /api/data/dealers?country_id=1` - Filter dealers by country

### Country & Tariff Data
- `GET /api/data/countries` - Get all countries
- `GET /api/data/tariffs` - Get tariff and tax information

### Analytics
- `GET /api/data/analytics` - Get profit and cost analytics data
- `GET /api/data/dashboard-summary` - Get comprehensive dashboard metrics

### Data Management
- `POST /api/data/upload-csv` - Upload CSV file
- `POST /api/data/manual-entry` - Submit manual data entry

## 🎨 UI Components

### Navigation
- Top navigation bar with route switching
- Sidebar navigation within CRM
- Active state indicators
- Responsive design for mobile

### Charts & Visualizations
- Chart.js integration for interactive charts
- Line charts for trend analysis
- Bar charts for comparisons
- Custom SVG visualizations for specific metrics

### Tables & Filters
- Sortable and filterable data tables
- Multi-select dropdown filters
- Performance indicator badges
- Action buttons for detailed views

### Cards & Layouts
- Information cards with metrics
- Recommendation cards with visual backgrounds
- Grid layouts for organized content
- Responsive flexbox design

## 💻 Technical Stack

### Frontend
- **React 19**: Component-based UI framework
- **Chart.js & React-Chartjs-2**: Interactive charts and graphs
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing
- **CSS3**: Modern styling with flexbox and grid

### Backend
- **FastAPI**: High-performance Python web framework
- **Pandas**: Data manipulation and analysis
- **Uvicorn**: ASGI server for FastAPI
- **Python-multipart**: File upload support

### Data
- **CSV Files**: Structured data storage in `/data/processed/`
- **Real-time Processing**: Dynamic data aggregation and calculations
- **JSON APIs**: RESTful data exchange format

## 📊 Data Sources

The system uses several CSV data files:
- `dealers.csv` - Dealer information and contact details
- `countries.csv` - Country data with economic indicators
- `country_tariffs.csv` - Tariff and tax rates by country
- `trade_transactions.csv` - Historical transaction data
- `products.csv` - Product catalog and categories

## 🔧 Configuration

### Environment Variables
```bash
# Frontend
REACT_APP_API_BASE_URL=http://localhost:8000/api

# Backend
DATA_PATH=/path/to/data/processed
CORS_ORIGINS=http://localhost:3000
```

### API Configuration
The backend automatically detects the data directory and provides CORS support for the frontend.

## 🎯 Future Enhancements

### Planned Features
1. **Real-time Dashboard**: WebSocket integration for live updates
2. **Advanced Filtering**: Multi-dimensional data filtering
3. **Export Functionality**: PDF and Excel export capabilities
4. **User Authentication**: Role-based access control
5. **Notification System**: Alerts for important events
6. **Mobile App**: React Native mobile application
7. **Advanced Analytics**: Machine learning insights and predictions

### Performance Optimizations
1. **Data Caching**: Redis integration for faster queries
2. **Pagination**: Large dataset handling with pagination
3. **Lazy Loading**: Component-based lazy loading
4. **CDN Integration**: Static asset optimization

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Errors**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/api/data/countries
   ```

2. **Chart Rendering Issues**
   ```bash
   # Reinstall chart dependencies
   npm install chart.js react-chartjs-2
   ```

3. **Data Loading Errors**
   - Verify CSV files exist in `/data/processed/`
   - Check file permissions and format

4. **File Upload Errors**
   ```bash
   # Install multipart support
   pip install python-multipart
   ```

## 📄 License

This project is part of the Trade Optimization System and follows the same licensing terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📞 Support

For technical support and feature requests, please open an issue in the repository or contact the development team.

---

**Built with ❤️ for efficient international trade management**
